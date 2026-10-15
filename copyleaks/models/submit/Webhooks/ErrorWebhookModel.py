from typing import Optional
from pydantic import Field
from .HelperModels.BaseModels.StatusWebhookModel import StatusWebhookModel
from .HelperModels.ErrorModels.ErrorModel import ErrorModel


class ErrorWebhookModel(StatusWebhookModel):
    """Scan error webhook. Parse it with `ErrorWebhookModel(**request.json)`."""
    __positional_fields__ = ('error', 'status')

    error: Optional[ErrorModel] = Field(
        default=None,
        description="The reason for the failure.",
        alias="error"
    )
