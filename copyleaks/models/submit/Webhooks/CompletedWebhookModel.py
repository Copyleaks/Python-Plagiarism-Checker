from typing import Optional
from pydantic import Field
from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionResponseModel import CopyleaksAiTextDetectionResponseModel
from copyleaks.models.constants.CopyleaksAlertCodes import CopyleaksAlertCodes
from .HelperModels.BaseModels.StatusWebhookModel import StatusWebhookModel
from .HelperModels.CompletedModels.NotificationsModel import NotificationsModel
from .HelperModels.CompletedModels.ReferencesValidationModel import ReferencesValidationModel
from .HelperModels.CompletedModels.ResultsModel import ResultsModel
from .HelperModels.CompletedModels.ScannedDocumentModel import ScannedDocumentModel
from .HelperModels.NotificationsModels.AlertsModel import AlertsModel


class CompletedWebhookModel(StatusWebhookModel):
    """Webhook of a completed scan. Parse it with `CompletedWebhookModel(**request.json)`."""
    __positional_fields__ = ('results', 'notifications', 'scanned_document', 'status')

    results: Optional[ResultsModel] = Field(
        default=None,
        description="All the results that were found, and their aggregated score.",
        alias="results"
    )

    notifications: Optional[NotificationsModel] = Field(
        default=None,
        description="Scan alerts that were detected in the scan.",
        alias="notifications"
    )

    scanned_document: Optional[ScannedDocumentModel] = Field(
        default=None,
        description="General information about the scanned document.",
        alias="scannedDocument"
    )

    references_validation: Optional[ReferencesValidationModel] = Field(
        default=None,
        description="Citation Checker summary. Sent when `references.validate` was enabled for the scan.",
        alias="referencesValidation"
    )

    def get_ai_detection_alert(self) -> Optional[AlertsModel]:
        """The first `suspected-ai-text` alert, or None."""
        notifications = self.notifications
        alerts = notifications.alerts if isinstance(notifications, NotificationsModel) else []
        for alert in alerts:
            if alert.code == CopyleaksAlertCodes.SUSPECTED_AI_TEXT:
                return alert
        return None

    def get_ai_detection_result(self) -> Optional[CopyleaksAiTextDetectionResponseModel]:
        """
        `get_ai_detection_alert().get_ai_detection_result()`, or None when there is no such alert.
        See `AlertsModel.get_ai_detection_result`.
        """
        alert = self.get_ai_detection_alert()
        return alert.get_ai_detection_result() if alert is not None else None
