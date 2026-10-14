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


class CopyleaksImagePlagiarismScannedImageModel(BaseModel):
    """
    Metadata about the submitted image and the scan. Missing fields are None.
    """

    model_config = ConfigDict(populate_by_name=True)

    scan_id: Optional[str] = Field(
        default=None,
        description="The scan ID provided in the request path.",
        alias="scanId"
    )

    expected_credits: Optional[int] = Field(
        default=None,
        description="The number of credits expected to be charged for this scan.",
        alias="expectedCredits"
    )

    actual_credits: Optional[int] = Field(
        default=None,
        description="The number of credits actually charged for this scan.",
        alias="actualCredits"
    )

    creation_time: Optional[str] = Field(
        default=None,
        description="UTC timestamp of when the scan was created (ISO 8601).",
        alias="creationTime"
    )

    width: Optional[int] = Field(
        default=None,
        description="Width of the submitted image in pixels.",
        alias="width"
    )

    height: Optional[int] = Field(
        default=None,
        description="Height of the submitted image in pixels.",
        alias="height"
    )

    filename: Optional[str] = Field(
        default=None,
        description="The filename provided in the request.",
        alias="filename"
    )
