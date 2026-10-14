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


class CopyleaksAiVideoDetectionVideoMetadataModel(BaseModel):
    """
    Metadata extracted from the video file (for example C2PA provenance data), when available.
    """

    model_config = ConfigDict(populate_by_name=True)

    issued_time: Optional[str] = Field(
        default=None,
        description="When the video was created, if available.",
        alias="issuedTime"
    )

    issued_by: Optional[str] = Field(
        default=None,
        description="The AI service or tool that created the video, if present in the metadata.",
        alias="issuedBy"
    )

    app_or_device_used: Optional[str] = Field(
        default=None,
        description="The application or device used to create the video, if available.",
        alias="appOrDeviceUsed"
    )

    content_summary: Optional[str] = Field(
        default=None,
        description="A summary of how the video was generated, if available.",
        alias="contentSummary"
    )


class CopyleaksAiVideoDetectionVideoInfoModel(BaseModel):
    """
    Information about the analyzed video.
    """

    duration: Optional[float] = Field(
        default=None,
        description="Total duration of the video in seconds.",
        alias="duration"
    )

    metadata: Optional[CopyleaksAiVideoDetectionVideoMetadataModel] = Field(
        default=None,
        description="Metadata extracted from the video file, when available.",
        alias="metadata"
    )
