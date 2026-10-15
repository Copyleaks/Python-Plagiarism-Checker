import logging
import os
import threading

import requests
from pydantic import BaseModel
from requests.adapters import HTTPAdapter

from copyleaks.exceptions.command_error import CommandError
from copyleaks.exceptions.rate_limit_error import RateLimitError
from copyleaks.exceptions.under_maintenance_error import UnderMaintenanceError
from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper

logger = logging.getLogger('copyleaks')
logger.addHandler(logging.NullHandler())

try:
    from urllib3.util.retry import Retry
except ImportError:  # pragma: no cover
    Retry = None

_NO_AUTH = object()


def _connect_only_retry():
    """
    Retry only connection errors, which happen before the request reaches the server, so a request that may have been
    processed (and charged) is never sent twice. `read=False` (not 0) re-raises a read timeout as `ReadTimeout`.
    """
    if Retry is None:
        return 0
    kwargs = dict(total=2, connect=2, read=False, status=0, backoff_factor=0.5, raise_on_status=False)
    try:
        return Retry(other=0, **kwargs)
    except TypeError:  # urllib3 older than 1.26 has no `other`
        return Retry(**kwargs)


class CopyleaksHttpClient:
    """HTTP transport of every SDK call: one keep-alive `requests.Session`, and a timeout on every call."""

    DEFAULT_TIMEOUT = (10, 180)
    """(connect, read) timeout in seconds used when no other timeout is configured."""

    _lock = threading.Lock()
    _session = None
    _owns_session = False
    _timeout = DEFAULT_TIMEOUT

    @classmethod
    def _create_session(cls):
        session = requests.Session()
        adapter = HTTPAdapter(pool_connections=10, pool_maxsize=32, max_retries=_connect_only_retry())
        session.mount('https://', adapter)
        session.mount('http://', adapter)
        return session

    @classmethod
    def get_session(cls):
        """The `requests.Session` used for all calls. Created on first use."""
        session = cls._session
        if session is None:
            with cls._lock:
                if cls._session is None:
                    cls._session = cls._create_session()
                    cls._owns_session = True
                session = cls._session
        return session

    @classmethod
    def set_session(cls, session):
        """Use your own `requests.Session`, or None for the SDK's default session."""
        if session is not None and not callable(getattr(session, 'request', None)):
            raise TypeError('session must be a requests.Session or None')
        with cls._lock:
            cls._session = session
            cls._owns_session = False

    @classmethod
    def _after_fork_in_child(cls):
        # A forked child must not share the parent's pooled connections, so the SDK's own session is created
        # again on first use. A session passed to `set_session` is kept. The lock may have been held by another
        # thread of the parent at fork time, so it is replaced.
        cls._lock = threading.Lock()
        if cls._owns_session:
            cls._session = None
            cls._owns_session = False

    @classmethod
    def get_timeout(cls):
        return cls._timeout

    @classmethod
    def set_timeout(cls, timeout):
        cls._validate_timeout(timeout)
        cls._timeout = timeout

    @staticmethod
    def _validate_timeout(timeout):
        if timeout is None:
            return
        values = timeout if isinstance(timeout, tuple) else (timeout,)
        if isinstance(timeout, tuple) and len(timeout) != 2:
            raise ValueError('timeout must be a number of seconds or a (connect, read) tuple')
        for value in values:
            if value is None:
                continue
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
                raise ValueError('timeout values must be positive numbers of seconds')

    @classmethod
    def send(cls, method, url, auth_token=_NO_AUTH, json=None, form=None, files=None, content_type=None,
             timeout=None, response_model=None, verify=None):
        """
        Send an API call. Returns `response_model` parsed from the JSON body, or the `requests.Response` without one.
        A given `auth_token` (even None) is checked with `verify` (default `CopyleaksClientHelper.verify_auth_token`),
        then sent as a Bearer token. `json` (a request object or pydantic
        model) is sent as compact JSON with a JSON `content_type`; `form` and `files` as multipart.
        Errors as in `request`.
        """
        if auth_token is _NO_AUTH:
            auth_token = None
        else:
            (verify or CopyleaksClientHelper.verify_auth_token)(auth_token)
        data = form
        if json is not None:
            content_type = content_type or 'application/json'
            if isinstance(json, BaseModel):
                data = CopyleaksClientHelper.model_to_json_bytes(json)
            else:
                data = CopyleaksClientHelper.to_json_bytes(json)
        headers = CopyleaksClientHelper.headers(auth_token, content_type)
        response = cls.request(method, url, headers=headers, data=data, files=files, timeout=timeout)
        if response_model is None:
            return response
        return response_model.model_validate(response.json())

    @classmethod
    def request(cls, method, url, headers=None, data=None, files=None, timeout=None):
        """
        Send a request and return the 2xx `requests.Response`. Raises `RateLimitError` on HTTP 429,
        `UnderMaintenanceError` on 503, `CommandError` on any other error status.
        """
        if timeout is None:
            timeout = cls._timeout
        else:
            cls._validate_timeout(timeout)
        response = cls.get_session().request(method, url, headers=headers, data=data, files=files, timeout=timeout)
        return cls.check_response(response)

    @staticmethod
    def check_response(response):
        if response.ok:
            return response
        status = response.status_code
        if logger.isEnabledFor(logging.DEBUG):
            try:
                body = (response.text or '')[:1000]
            except Exception:
                body = ''
            logger.debug('Copyleaks API call failed: HTTP %s %s', status, body)
        if status == 429:
            raise RateLimitError(response)
        if status == 503:
            raise UnderMaintenanceError(response)
        raise CommandError(response)


if hasattr(os, 'register_at_fork'):  # not available on Windows
    os.register_at_fork(after_in_child=CopyleaksHttpClient._after_fork_in_child)
