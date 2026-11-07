import re

from copyleaks.models.submit.Webhooks.HelperModels.ErrorModels.ErrorModel import ErrorDetailModel

_INTEGER = re.compile(r'\s*[+-]?[0-9]+\s*')


def _describe_response(response):
    """A short `HTTP <status>: <body>` text for an error response. Never includes request headers."""
    status = getattr(response, 'status_code', None)
    if status is None:
        if isinstance(response, (bytes, bytearray)):
            return response.decode('utf-8', 'replace')[:500]
        return '' if response is None else str(response)[:500]
    try:
        body = (response.text or '').strip()
    except Exception:
        body = ''
    return f"HTTP {status}: {body[:500]}" if body else f"HTTP {status}"


def _parse_retry_after(response):
    """The `Retry-After` header in seconds, or None when it is missing or is not a number of seconds."""
    headers = getattr(response, 'headers', None)
    if not headers:
        return None
    try:
        value = headers.get('Retry-After')
    except Exception:
        return None
    if value is None:
        return None
    try:
        seconds = float(str(value).strip())
    except ValueError:
        return None
    return seconds if seconds >= 0 else None


def _error_object(response):
    """
    The `error` object of a JSON error body, `{"error": {"type", "id", "code", "message", "url", "details"}}`.
    An empty dict when the body is not a JSON object with an `error` object. Never raises.
    """
    if getattr(response, 'status_code', None) is None:
        return {}
    try:
        body = response.json()
    except Exception:
        return {}
    error = body.get('error') if isinstance(body, dict) else None
    return error if isinstance(error, dict) else {}


def _string_or_none(value):
    return value if isinstance(value, str) else None


class _ResponseError(Exception):
    """Base of the errors that carry the `requests.Response` of a failed call (or None)."""

    _message_without_response = ''

    def __init__(self, response=None):
        super().__init__(*(() if response is None else (response,)))
        self._response = response

    def get_response(self):
        return self._response

    @property
    def status_code(self):
        """The HTTP status code of the response, or None."""
        return getattr(self._response, 'status_code', None)

    @property
    def retry_after(self):
        """Seconds to wait before retrying, from the `Retry-After` response header, or None."""
        return _parse_retry_after(self._response)

    @property
    def error_type(self):
        """`error.type` of the response body, such as "invalid_request_error" (see `CopyleaksErrorTypes`), or None."""
        return _string_or_none(_error_object(self._response).get('type'))

    @property
    def error_id(self):
        """`error.id` of the response body, a machine-readable identifier such as "missing_parameter", or None."""
        return _string_or_none(_error_object(self._response).get('id'))

    @property
    def error_code(self):
        """`error.code` of the response body as an int (a numeric string is converted), or None."""
        code = _error_object(self._response).get('code')
        if isinstance(code, int) and not isinstance(code, bool):
            return code
        if isinstance(code, str) and _INTEGER.fullmatch(code):
            try:
                return int(code)
            except ValueError:  # more digits than Python's int string conversion limit
                return None
        return None

    @property
    def error_message(self):
        """`error.message` of the response body, a readable description of the error, or None."""
        return _string_or_none(_error_object(self._response).get('message'))

    @property
    def error_url(self):
        """`error.url` of the response body, the documentation page of the error, or None."""
        return _string_or_none(_error_object(self._response).get('url'))

    @property
    def error_details(self):
        """
        `error.details` of the response body: the request parameters that caused the error, as a list of
        `ErrorDetailModel` (`param`, `message`). An empty list when the body has no details.
        """
        details = _error_object(self._response).get('details')
        if not isinstance(details, list):
            return []
        return [ErrorDetailModel(param=_string_or_none(detail.get('param')),
                                 message=_string_or_none(detail.get('message')))
                for detail in details if isinstance(detail, dict)]

    def __str__(self):
        if self._response is None and self._message_without_response:
            return self._message_without_response
        return _describe_response(self._response)


class CommandError(_ResponseError):
    """The server rejected the request. `get_response()` returns the `requests.Response`."""
