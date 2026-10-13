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

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

from copyleaks.helpers.copyleaks_dict_access_mixin import CopyleaksDictAccessMixin
from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionExplainModel import CopyleaksAiTextDetectionExplainModel
from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionResultModel import CopyleaksAiTextDetectionResultModel
from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionScannedDocumentModel import CopyleaksAiTextDetectionScannedDocumentModel
from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionSummaryModel import CopyleaksAiTextDetectionSummaryModel


class CopyleaksAiTextDetectionResponseModel(CopyleaksDictAccessMixin, BaseModel):
    """
    Result of Copyleaks AI text detection.
    This is the response of `AiDetectionClient.submit_natural_language`,
    and the decoded `additionalData` of the `suspected-ai-text` alert in the completed webhook.
    Unknown fields are ignored, missing fields are None, and a missing or null list is empty.
    Serialize with `model_dump(by_alias=True)` to get the camelCase webhook keys back.
    """

    # Lets pydantic versions older than 2.10 accept the `model_version` field name without a warning.
    model_config = ConfigDict(protected_namespaces=())

    model_version: Optional[str] = Field(
        default=None,
        description="The version of the AI detection model used for the analysis.",
        alias="modelVersion",
        serialization_alias="modelVersion"
    )

    results: List[CopyleaksAiTextDetectionResultModel] = Field(
        default_factory=list,
        description="Classified sections of the scanned text.",
        alias="results"
    )

    summary: Optional[CopyleaksAiTextDetectionSummaryModel] = Field(
        default=None,
        description="Human and AI portions of the scanned text.",
        alias="summary"
    )

    translation_provider: Optional[int] = Field(
        default=None,
        description="Machine translation provider used before the detection. 0 = the text was not translated.",
        alias="translationProvider",
        serialization_alias="translationProvider"
    )

    translation: Optional[str] = Field(
        default=None,
        description="The machine-translated English text. Present only when the text was translated.",
        alias="translation"
    )

    explain: Optional[CopyleaksAiTextDetectionExplainModel] = Field(
        default=None,
        description="Explanation of the detection. Present only when explain was enabled for the scan.",
        alias="explain"
    )

    scanned_document: Optional[CopyleaksAiTextDetectionScannedDocumentModel] = Field(
        default=None,
        description="General information about the scanned document.",
        alias="scannedDocument",
        serialization_alias="scannedDocument"
    )

    scan_type: Optional[str] = Field(
        default=None,
        description="\"sandbox\" for sandbox scans. Not sent for regular scans.",
        alias="scanType",
        serialization_alias="scanType"
    )

    @field_validator('model_version', mode='before')
    @classmethod
    def model_version_number_to_str(cls, v):
        """Accept a numeric model version, as the other Copyleaks SDKs do."""
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return str(v)
        return v

    @field_validator('results', mode='before')
    @classmethod
    def results_none_to_empty(cls, v):
        """Treat a null `results` as an empty list."""
        return [] if v is None else v
