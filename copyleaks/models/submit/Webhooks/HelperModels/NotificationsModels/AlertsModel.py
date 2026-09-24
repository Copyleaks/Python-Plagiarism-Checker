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
from pydantic import BaseModel, Field

from copyleaks.models.AiDetection.Responses.CopyleaksAiDetectionResponseModel import CopyleaksAiDetectionResponseModel
from copyleaks.models.constants.CopyleaksAlertCodes import CopyleaksAlertCodes

class AlertsModel(BaseModel):
    """
    A scan alert from `notifications.alerts` of the completed webhook.
    """

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
        alias="helpLink"
    )

    severity: Optional[int] = Field(
        default=None,
        description="Specifies the importance of the scan alert, from 0 (lowest) to 4 (highest).",
        alias="severity"
    )

    additional_data: Optional[str] = Field(
        default=None,
        description="Additional data about the scan alert. Supplied as a json string.",
        alias="additionalData"
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
        Initializes an Alerts object.
        Accepts the snake_case arguments (positional or keyword) and the camelCase
        webhook keys `helpLink` and `additionalData`, so `AlertsModel(**alert_json)` works.
        """
        kwargs.setdefault("helpLink", help_link)
        kwargs.setdefault("additionalData", additional_data)
        super().__init__(category=category, code=code, title=title, message=message,
                         severity=severity, **kwargs)

    def get_ai_detection_result(self) -> Optional[CopyleaksAiDetectionResponseModel]:
        """
        Decodes the `additional_data` of a `suspected-ai-text` alert into the AI text detection result.
        Trailing NUL characters and whitespace are removed before parsing; `additional_data` itself is not changed.

        Returns:
            `CopyleaksAiDetectionResponseModel`, or None when the alert code is not
            `CopyleaksAlertCodes.SUSPECTED_AI_TEXT` or `additional_data` is empty or missing.

        Raises:
            `pydantic.ValidationError`: `additional_data` is not valid JSON or does not match the model.
        """
        if self.code != CopyleaksAlertCodes.SUSPECTED_AI_TEXT:
            return None
        data = self.additional_data or ""
        end = len(data)
        while end > 0 and (data[end - 1] == "\x00" or data[end - 1].isspace()):
            end -= 1
        if end == 0:
            return None
        return CopyleaksAiDetectionResponseModel.model_validate_json(data[:end])
