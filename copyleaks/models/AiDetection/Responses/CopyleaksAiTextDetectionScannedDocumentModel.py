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


class CopyleaksAiTextDetectionScannedDocumentModel(BaseModel):
    """
    General information about the scanned document. Missing fields are None.
    """

    scan_id: Optional[str] = Field(
        default=None,
        description="The scan id given by the user.",
        alias="scanId",
        serialization_alias="scanId"
    )

    total_words: Optional[int] = Field(
        default=None,
        description="Total number of words found in the scanned text.",
        alias="totalWords",
        serialization_alias="totalWords"
    )

    total_excluded: Optional[int] = Field(
        default=None,
        description="Number of excluded words in the scanned text.",
        alias="totalExcluded",
        serialization_alias="totalExcluded"
    )

    actual_credits: Optional[int] = Field(
        default=None,
        description="The number of credits spent on the scan.",
        alias="actualCredits",
        serialization_alias="actualCredits"
    )

    expected_credits: Optional[int] = Field(
        default=None,
        description="The number of credits that was expected to be spent on the scan.",
        alias="expectedCredits",
        serialization_alias="expectedCredits"
    )

    creation_time: Optional[str] = Field(
        default=None,
        description="ISO 8601 creation time of the scan (UTC).",
        alias="creationTime",
        serialization_alias="creationTime"
    )
