from typing import List, Optional
from pydantic import Field, field_validator

from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel, none_to_empty_list


class ErrorDetailModel(CopyleaksWebhookBaseModel):
    """A parameter that caused the error."""
    __positional_fields__ = ('param', 'message')

    param: Optional[str] = Field(
        default=None,
        description="The parameter name that caused the error.",
        alias="param"
    )

    message: Optional[str] = Field(
        default=None,
        description="A message describing the issue with this parameter.",
        alias="message"
    )


class ErrorModel(CopyleaksWebhookBaseModel):
    """The error of the error webhook, and of a failed AI Image or AI Video Detection webhook."""
    __positional_fields__ = ('code', 'message')

    type: Optional[str] = Field(
        default=None,
        description="The error type, for example \"invalid_request_error\" or \"payment_error\".",
        alias="type"
    )

    id: Optional[str] = Field(
        default=None,
        description="The machine-readable error identifier, for example \"insufficient_credits\".",
        alias="id"
    )

    code: Optional[int] = Field(
        default=None,
        description="Error code that represents the reason for failure.",
        alias="code"
    )

    message: Optional[str] = Field(
        default=None,
        description="Human-readable error message that describes the reason for failure.",
        alias="message"
    )

    url: Optional[str] = Field(
        default=None,
        description="A URL to the documentation page of this error.",
        alias="url"
    )

    details: List[ErrorDetailModel] = Field(
        default_factory=list,
        description="The parameters that caused the error.",
        alias="details"
    )

    @field_validator('details', mode='before')
    @classmethod
    def details_none_to_empty(cls, v):
        return none_to_empty_list(v)
