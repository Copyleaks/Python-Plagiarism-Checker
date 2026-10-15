from typing import Any, Optional
from pydantic import ConfigDict, Field, TypeAdapter

from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionResponseModel import CopyleaksAiTextDetectionResponseModel
from copyleaks.models.constants.CopyleaksAlertCodes import CopyleaksAlertCodes
from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel

# Padding stripped from the end of `additionalData` before parsing: NUL and ASCII whitespace.
_TRAILING_PADDING = frozenset("\x00\t\n\x0b\x0c\r ")

# Plain JSON values first, so JSON that is not an object gives None; malformed JSON raises a
# pydantic.ValidationError titled like the result model.
_JSON_ADAPTER = TypeAdapter(Any, config=ConfigDict(title=CopyleaksAiTextDetectionResponseModel.__name__))

class AlertsModel(CopyleaksWebhookBaseModel):
    """A scan alert from `notifications.alerts` of the completed webhook."""

    category: Optional[int] = Field(
        default=None,
        description="Scan alert category. 2 = AI content detection.",
        alias="category"
    )

    code: Optional[str] = Field(
        default=None,
        description="Scan alert code. The code is unique for each scan alert. See `CopyleaksAlertCodes`.",
        alias="code"
    )

    title: Optional[str] = Field(
        default=None,
        description="Scan alert human-readable title.",
        alias="title"
    )

    message: Optional[str] = Field(
        default=None,
        description="Provides human-readable information about the scan alert.",
        alias="message"
    )

    help_link: Optional[str] = Field(
        default=None,
        description="Url to a resource describing the specific scan alert. Not sent for every alert.",
        alias="helpLink",
        serialization_alias="helpLink"
    )

    severity: Optional[int] = Field(
        default=None,
        description="Specifies the importance of the scan alert, from 0 (lowest) to 4 (highest).",
        alias="severity"
    )

    additional_data: Optional[str] = Field(
        default=None,
        description="Additional data about the scan alert. Supplied as a json string.",
        alias="additionalData",
        serialization_alias="additionalData"
    )

    def __init__(self,
                 category: Optional[int] = None,
                 code: Optional[str] = None,
                 title: Optional[str] = None,
                 message: Optional[str] = None,
                 help_link: Optional[str] = None,
                 severity: Optional[int] = None,
                 additional_data: Optional[str] = None,
                 **kwargs: Any):
        """
        Accepts the snake_case arguments, positional or keyword, and the camelCase keys `helpLink` and `additionalData`,
        so `AlertsModel(**alert_json)` works.
        """
        kwargs.setdefault("helpLink", help_link)
        kwargs.setdefault("additionalData", additional_data)
        super().__init__(category=category, code=code, title=title, message=message,
                         severity=severity, **kwargs)

    def get_ai_detection_result(self) -> Optional[CopyleaksAiTextDetectionResponseModel]:
        """
        Decode the `additional_data` of a `suspected-ai-text` alert, ignoring trailing NUL and ASCII whitespace.
        Returns a `CopyleaksAiTextDetectionResponseModel`, or None for another alert code, no data, or JSON that is
        not an object. Raises `pydantic.ValidationError` for invalid JSON or a field of the wrong type.
        """
        if self.code != CopyleaksAlertCodes.SUSPECTED_AI_TEXT:
            return None
        data = self.additional_data or ""
        end = len(data)
        while end > 0 and data[end - 1] in _TRAILING_PADDING:
            end -= 1
        if end == 0:
            return None
        decoded = _JSON_ADAPTER.validate_json(data[:end])
        if not isinstance(decoded, dict):
            return None
        return CopyleaksAiTextDetectionResponseModel.model_validate(decoded)
