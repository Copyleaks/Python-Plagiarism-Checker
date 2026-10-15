from typing import Optional
from pydantic import Field

from copyleaks.models.submit.Webhooks.HelperModels.BaseModels.WebhookModel import WebhookModel


class StatusWebhookModel(WebhookModel):
    __positional_fields__ = ('status',)

    status: Optional[int] = Field(
        default=None,
        description="The current status of the scan: 0 = Success, 1 = Error, 2 = CreditsChecked, 3 = Indexed.",
        alias="status"
    )
