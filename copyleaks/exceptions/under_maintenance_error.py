from copyleaks.exceptions.command_error import _ResponseError


class UnderMaintenanceError(_ResponseError):
    """
    Copyleaks servers are under maintenance (HTTP 503): retry later with exponential backoff, see `retry_after`.
    `get_response()` returns the `requests.Response`. Not a `CommandError`, as in 5.x.
    """

    _message_without_response = 'Under maintenance'
