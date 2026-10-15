from typing import Optional
from pydantic import AliasChoices, Field

from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel


class TaskModel(CopyleaksWebhookBaseModel):
    """An export task of the export completed webhook."""
    __positional_fields__ = ('endpoint', 'is_healthy', 'http_status_code')

    endpoint: Optional[str] = Field(
        default=None,
        description="The endpoint address of the export task. `endpont=` is accepted too.",
        alias="endpoint",
        validation_alias=AliasChoices("endpoint", "endpont")
    )

    is_healthy: Optional[bool] = Field(
        default=None,
        description="Whether the task was completed without internal errors on the Copyleaks side.",
        alias="isHealthy"
    )

    http_status_code: Optional[int] = Field(
        default=None,
        description="The status code reported by your server. None when `is_healthy` is False.",
        alias="httpStatusCode"
    )
