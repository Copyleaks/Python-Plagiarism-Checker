from typing import List
from pydantic import Field, field_validator

from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel
from ..NotificationsModels.AlertsModel import AlertsModel


class NotificationsModel(CopyleaksWebhookBaseModel):
    """A list of scan alerts that were detected in the scan."""
    __positional_fields__ = ('alerts',)

    alerts: List[AlertsModel] = Field(
        default_factory=list,
        description="Scan alerts that were detected in the scan.",
        alias="alerts"
    )

    @field_validator('alerts', mode='before')
    @classmethod
    def alerts_drop_none(cls, v):
        """Skip null alert entries, so one null entry does not fail the whole webhook."""
        if v is None:
            return []
        if isinstance(v, (list, tuple)):
            return [alert for alert in v if alert is not None]
        return v
