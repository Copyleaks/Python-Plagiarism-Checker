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
from pydantic import BaseModel, ConfigDict, Field


class CopyleaksAiVideoDetectionScannedVideoModel(BaseModel):
    """
    Metadata about the AI Video Detection scan. Missing fields are None.
    """

    model_config = ConfigDict(populate_by_name=True)

    scan_id: Optional[str] = Field(
        default=None,
        description="The scan ID provided in the request.",
        alias="scanId"
    )

    actual_credits: Optional[int] = Field(
        default=None,
        description="The actual number of credits consumed by the scan.",
        alias="actualCredits"
    )

    expected_credits: Optional[int] = Field(
        default=None,
        description="The expected number of credits for the scan.",
        alias="expectedCredits"
    )

    creation_time: Optional[str] = Field(
        default=None,
        description="ISO 8601 timestamp of when the scan was created.",
        alias="creationTime"
    )
