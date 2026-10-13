'''
 The MIT License(MIT)

 Copyright(c) 2016 Copyleaks LTD (https://copyleaks.com)

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
'''

from typing import Any, Optional
from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionResponseModel import CopyleaksAiTextDetectionResponseModel
from copyleaks.models.constants.CopyleaksAlertCodes import CopyleaksAlertCodes
from .HelperModels.BaseModels.StatusWebhookModel import StatusWebhookModel
from .HelperModels.CompletedModels.NotificationsModel import NotificationsModel
from .HelperModels.CompletedModels.ResultsModel import ResultsModel
from .HelperModels.CompletedModels.ScannedDocumentModel import ScannedDocumentModel
from .HelperModels.NotificationsModels.AlertsModel import AlertsModel

class CompletedWebhookModel(StatusWebhookModel):
    """
    Represents a webhook payload for a completed scan, including results,
    notifications, and document info. Inherits from StatusWebhook.
    """
    results: Optional[ResultsModel] = None
    notifications: Optional[NotificationsModel] = None
    scanned_document: Optional[ScannedDocumentModel] = None

    def __init__(self,
                 results: Optional[ResultsModel] = None,
                 notifications: Optional[NotificationsModel] = None,
                 scanned_document: Optional[ScannedDocumentModel] = None,
                 status: Optional[int] = None,
                 **kwargs: Any):
        """
        Initializes a CompletedWebhook object.
        A `notifications` dictionary, as in `CompletedWebhookModel(**request.json)`,
        is converted to a `NotificationsModel` with typed `AlertsModel` alerts.
        """
        super().__init__(status=status, **kwargs)
        self.results = results
        self.notifications = NotificationsModel.model_validate(notifications) if isinstance(notifications, dict) else notifications
        self.scanned_document = scanned_document

    def get_ai_detection_alert(self) -> Optional[AlertsModel]:
        """
        Returns the first `suspected-ai-text` alert of the scan.

        Returns:
            `AlertsModel`. Returns None when the completed webhook contains no suspected-ai-text alert.
        """
        notifications = self.notifications
        alerts = notifications.alerts if isinstance(notifications, NotificationsModel) else []
        for alert in alerts:
            if alert.code == CopyleaksAlertCodes.SUSPECTED_AI_TEXT:
                return alert
        return None

    def get_ai_detection_result(self) -> Optional[CopyleaksAiTextDetectionResponseModel]:
        """
        Returns the decoded AI text detection result of the `suspected-ai-text` alert,
        the same as `get_ai_detection_alert().get_ai_detection_result()`.

        Returns:
            `CopyleaksAiTextDetectionResponseModel`, or None when there is no `suspected-ai-text` alert,
            or its additional data is empty or is valid JSON that is not an object.
            Use `get_ai_detection_alert()` to tell these cases apart.

        Raises:
            `pydantic.ValidationError`: the alert's additional data is not valid JSON, or a field has a type
            the model cannot accept.
        """
        alert = self.get_ai_detection_alert()
        return alert.get_ai_detection_result() if alert is not None else None
