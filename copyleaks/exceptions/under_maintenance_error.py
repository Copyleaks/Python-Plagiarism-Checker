from copyleaks.exceptions.command_error import _describe_response
from copyleaks.exceptions.rate_limit_error import _parse_retry_after


class UnderMaintenanceError(Exception):
    """
    Copyleaks servers are under maintenance (HTTP 503): retry later with exponential backoff, see `retry_after`.
    `get_response()` returns the `requests.Response`.
    """

    def __init__(self, response=None):
        super().__init__(*(() if response is None else (response,)))
        self._response = response

    def get_response(self):
        return self._response

    @property
    def status_code(self):
        return getattr(self._response, 'status_code', None)

    @property
    def retry_after(self):
        """Seconds to wait before retrying, from the `Retry-After` response header, or None."""
        return _parse_retry_after(self._response)

    def __str__(self):
        return _describe_response(self._response) if self._response is not None else 'Under maintenance'
