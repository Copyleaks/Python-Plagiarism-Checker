'''
 The MIT License(MIT)
 
 Copyright(c) 2016 Copyleaks LTD (https://copyleaks.com)
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
'''

import logging
import threading

import requests
from requests.adapters import HTTPAdapter

from copyleaks.exceptions.command_error import CommandError
from copyleaks.exceptions.rate_limit_error import RateLimitError
from copyleaks.exceptions.under_maintenance_error import UnderMaintenanceError

logger = logging.getLogger('copyleaks')
logger.addHandler(logging.NullHandler())

try:
    from urllib3.util.retry import Retry
except ImportError:  # pragma: no cover
    Retry = None


def _connect_only_retry():
    """
    Retry only connection errors, which happen before the request reaches the server.
    Read errors and error statuses are never retried, so a request that may have been processed
    (and charged) is never sent twice.
    """
    if Retry is None:
        return 0
    kwargs = dict(total=2, connect=2, read=0, status=0, backoff_factor=0.5, raise_on_status=False)
    try:
        return Retry(other=0, **kwargs)
    except TypeError:  # urllib3 older than 1.26 has no `other`
        return Retry(**kwargs)


class CopyleaksHttpClient:
    """
    The HTTP transport shared by every Copyleaks SDK call.

    All calls go through one `requests.Session`, so connections (TCP and TLS) are kept alive and reused.
    Every call has a timeout. The default is `DEFAULT_TIMEOUT`; change it with `set_timeout`, or pass
    `timeout=` to a single call.
    """

    DEFAULT_TIMEOUT = (10, 180)
    """(connect, read) timeout in seconds used when no other timeout is configured."""

    _lock = threading.Lock()
    _session = None
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
                session = cls._session
        return session

    @classmethod
    def set_session(cls, session):
        """
        Use your own `requests.Session` (for example with your own proxies, retries or pool sizes).
        Pass None to go back to the SDK's default session.
        """
        if session is not None and not callable(getattr(session, 'request', None)):
            raise TypeError('session must be a requests.Session or None')
        with cls._lock:
            cls._session = session

    @classmethod
    def get_timeout(cls):
        return cls._timeout

    @classmethod
    def set_timeout(cls, timeout):
        """
        Set the default timeout of every call.

        Parameters:
            timeout: seconds as a number, a (connect, read) tuple, or None for no timeout.
        """
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
    def request(cls, method, url, headers=None, data=None, files=None, timeout=None):
        """
        Send a request and return the `requests.Response` of a successful (2xx) call.

        Raises:
            `RateLimitError`: HTTP 429.
            `UnderMaintenanceError`: HTTP 503.
            `CommandError`: any other non-2xx status.
            `requests.exceptions.Timeout`: the connect or read timeout expired.
            `requests.exceptions.ConnectionError`: the server could not be reached.
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
