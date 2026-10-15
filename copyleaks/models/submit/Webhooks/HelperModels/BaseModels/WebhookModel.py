from typing import Optional
from pydantic import Field

from copyleaks.models.submit.Webhooks.HelperModels.BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel


class WebhookModel(CopyleaksWebhookBaseModel):
    __positional_fields__ = ('developer_payload',)

    developer_payload: Optional[str] = Field(
        default=None,
        description="The developer payload that was provided in the submit method.",
        alias="developerPayload"
    )
