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

    def __str__(self):
        if self._response is None and self._message_without_response:
            return self._message_without_response
        return _describe_response(self._response)


class CommandError(_ResponseError):
    """The server rejected the request. `get_response()` returns the `requests.Response`."""
