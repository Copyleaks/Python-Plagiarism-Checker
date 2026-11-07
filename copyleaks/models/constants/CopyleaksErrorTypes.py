class CopyleaksErrorTypes:
    """
    The documented values of `error.type` in an API error response (`CommandError.error_type`, `ErrorModel.type`).
    The field stays a plain string, so a type added later by the API is kept as sent.
    """
    INVALID_REQUEST_ERROR = "invalid_request_error"
    """Invalid request format, missing parameters or malformed data."""

    AUTHENTICATION_ERROR = "authentication_error"
    """Authentication failed, for example invalid credentials or a disabled account."""

    PAYMENT_ERROR = "payment_error"
    """A payment problem, for example insufficient credits or an expired subscription."""

    API_ERROR = "api_error"
    """A server-side error, for example an internal error, overload or a timeout."""
