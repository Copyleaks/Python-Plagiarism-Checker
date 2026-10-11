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

from typing import Optional
from pydantic import BaseModel, Field

from copyleaks.helpers.copyleaks_dict_access_mixin import CopyleaksDictAccessMixin
from copyleaks.models.WritingAssistant.Responses.CopyleaksWritingAssistantCorrectionsModel import CopyleaksWritingAssistantCorrectionsModel
from copyleaks.models.WritingAssistant.Responses.CopyleaksWritingAssistantScannedDocumentModel import CopyleaksWritingAssistantScannedDocumentModel
from copyleaks.models.WritingAssistant.Responses.CopyleaksWritingAssistantScoreModel import CopyleaksWritingAssistantScoreModel


class CopyleaksWritingAssistantResponseModel(CopyleaksDictAccessMixin, BaseModel):
    """
    Result of the Copyleaks Writing Assistant (Grammar Checker).
    This is the response of `WritingAssistantClient.submit_text`.
    Unknown fields are ignored and missing fields are None.
    Serialize with `model_dump(by_alias=True)` to get the camelCase JSON keys back.
    """

    score: Optional[CopyleaksWritingAssistantScoreModel] = Field(
        default=None,
        description="Writing quality scores, readability and text statistics.",
        alias="score"
    )

    corrections: Optional[CopyleaksWritingAssistantCorrectionsModel] = Field(
        default=None,
        description="Suggested corrections to the text.",
        alias="corrections"
    )

    scanned_document: Optional[CopyleaksWritingAssistantScannedDocumentModel] = Field(
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
