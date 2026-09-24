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
from pydantic import BaseModel, ConfigDict, Field

from copyleaks.models.AiDetection.Responses.CopyleaksAiDetectionExplainModel import CopyleaksAiDetectionExplainModel
from copyleaks.models.AiDetection.Responses.CopyleaksAiDetectionResultModel import CopyleaksAiDetectionResultModel
from copyleaks.models.AiDetection.Responses.CopyleaksAiDetectionSummaryModel import CopyleaksAiDetectionSummaryModel


class CopyleaksAiDetectionResponseModel(BaseModel):
    """
    Result of Copyleaks AI text detection.
    This is the decoded `additionalData` of the `suspected-ai-text` alert in the completed webhook.
    Unknown fields are ignored.
    """

    # Lets pydantic versions older than 2.10 accept the `model_version` field name without a warning.
    model_config = ConfigDict(protected_namespaces=())

    model_version: Optional[str] = Field(
        default=None,
        description="The version of the AI detection model used for the analysis.",
        alias="modelVersion"
    )

    results: List[CopyleaksAiDetectionResultModel] = Field(
        default_factory=list,
        description="Classified sections of the scanned text.",
        alias="results"
    )

    summary: Optional[CopyleaksAiDetectionSummaryModel] = Field(
        default=None,
        description="Human and AI portions of the scanned text.",
        alias="summary"
    )

    translation_provider: Optional[int] = Field(
        default=None,
        description="Machine translation provider used before the detection. 0 = the text was not translated.",
        alias="translationProvider"
    )

    translation: Optional[str] = Field(
        default=None,
        description="The machine-translated English text. Present only when the text was translated.",
        alias="translation"
    )

    explain: Optional[CopyleaksAiDetectionExplainModel] = Field(
        default=None,
        description="Explanation of the detection. Present only when explain was enabled for the scan.",
        alias="explain"
    )
