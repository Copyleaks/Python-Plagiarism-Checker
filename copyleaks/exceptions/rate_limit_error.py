from copyleaks.exceptions.command_error import CommandError, _describe_response


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


class RateLimitError(CommandError):
    """Too many requests (HTTP 429): wait before calling again, see `retry_after`. A `CommandError`."""

    def __init__(self, response=None):
        super().__init__(response)

    @property
    def retry_after(self):
        """Seconds to wait before retrying, from the `Retry-After` response header, or None."""
        return _parse_retry_after(self.get_response())

    def __str__(self):
        response = self.get_response()
        return _describe_response(response) if response is not None else 'Too many requests'
