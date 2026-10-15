from copyleaks.exceptions.command_error import CommandError


class RateLimitError(CommandError):
    """Too many requests (HTTP 429): wait before calling again, see `retry_after`. A `CommandError`."""

    _message_without_response = 'Too many requests'
