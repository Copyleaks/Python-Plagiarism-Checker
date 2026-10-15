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


class CommandError(Exception):
    """The server rejected the request. `get_response()` returns the `requests.Response`."""

    def __init__(self, response):
        super().__init__(response)
        self.__set_response(response)

    def get_response(self):
        return self.__x

    def __set_response(self, x):
        self.__x = x

    @property
    def status_code(self):
        """The HTTP status code of the response, or None."""
        return getattr(self.__x, 'status_code', None)

    def __str__(self):
        return _describe_response(self.__x)
