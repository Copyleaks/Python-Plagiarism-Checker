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

from pydantic import BaseModel, Field


class CopyleaksAiImageDetectionScannedDocumentModel(BaseModel):
    """
    Metadata about the AI image detection scan operation.
    """
    
    scan_id: str = Field(
        ...,
        description="The unique identifier for this scan.",
        alias="scanId"
    )
    
    actual_credits: int = Field(
        ...,
        description="The actual number of credits consumed by this scan.",
        alias="actualCredits"
    )
    
    expected_credits: int = Field(
        ...,
        description="The expected number of credits for this scan.",
        alias="expectedCredits"
    )
    
    creation_time: str = Field(
        ...,
        description="ISO 8601 timestamp of when the scan was created.",
        alias="creationTime"
    )

