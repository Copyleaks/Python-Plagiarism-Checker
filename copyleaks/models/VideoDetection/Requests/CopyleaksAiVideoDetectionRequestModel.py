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

from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionAsyncRequestModel import validate_headers

SUPPORTED_VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.mpg', '.m4v', '.3gp', '.mxf']


class CopyleaksAiVideoDetectionWebhooksModel(BaseModel):
    """
    Where Copyleaks sends the result of an AI Video Detection.
    """

    model_config = ConfigDict(populate_by_name=True)

    url: str = Field(
        ...,
        description="The URL that Copyleaks will POST the detection result to.",
        alias="url"
    )

    headers: Optional[List[List[str]]] = Field(
        default=None,
        description="Custom headers for the webhook request, as [name, value] pairs.",
        alias="headers"
    )

    @field_validator('url')
    @classmethod
    def validate_url(cls, v):
        if not v or not v.strip():
            raise ValueError('webhooks url is required')
        return v

    @field_validator('headers', mode='before')
    @classmethod
    def validate_headers(cls, v):
        return validate_headers(v)


class CopyleaksAiVideoDetectionRequestModel(BaseModel):
    """
    Request of AI Video Detection: Copyleaks downloads the video from `url` and sends the result to
    `webhooks.url`. Use it with `VideoDetectionClient.submit`.
    """

    model_config = ConfigDict(populate_by_name=True, protected_namespaces=())

    url: str = Field(
        ...,
        description="Publicly accessible URL of the video file to analyze.",
        alias="url"
    )

    file_name: str = Field(
        ...,
        description="The name of the video file including its extension, for example \"my-video.mp4\". Maximum 255 characters. "
                    "`filename=` is accepted too.",
        alias="filename",
        max_length=255
    )

    model: str = Field(
        ...,
        description="The AI detection model, for example \"ai-video-1-pro\". See `CopyleaksAiVideoDetectionModels`.",
        alias="model"
    )

    webhooks: CopyleaksAiVideoDetectionWebhooksModel = Field(
        ...,
        description="Where to send the result. A dict such as {\"url\": \"https://...\"} is accepted.",
        alias="webhooks"
    )

    headers: Optional[List[List[str]]] = Field(
        default=None,
        description="Custom headers to send when Copyleaks downloads the video from `url`, as [name, value] pairs.",
        alias="headers"
    )

    verb: Optional[str] = Field(
        default=None,
        description="The HTTP method used to download the video from `url`: \"GET\" (the server default), \"POST\" or \"PUT\".",
        alias="verb"
    )

    sandbox: Optional[bool] = Field(
        default=None,
        description="Use sandbox mode to test your integration without consuming any credits. Returns mock results. "
                    "The server default is False.",
        alias="sandbox"
    )

    developer_payload: Optional[str] = Field(
        default=None,
        description="A custom string that Copyleaks includes in the webhook result.",
        alias="developerPayload"
    )

    @field_validator('url', 'model')
    @classmethod
    def validate_required_text(cls, v):
        if not v or not v.strip():
            raise ValueError('value is required and cannot be empty')
        return v

    @field_validator('file_name')
    @classmethod
    def validate_file_name(cls, v):
        if not v or not v.strip():
            raise ValueError('filename is required')
        if not any(v.lower().endswith(ext) for ext in SUPPORTED_VIDEO_EXTENSIONS):
            raise ValueError(f'filename must have one of the supported extensions: {", ".join(SUPPORTED_VIDEO_EXTENSIONS)}')
        return v

    @field_validator('headers', mode='before')
    @classmethod
    def validate_headers(cls, v):
        return validate_headers(v)

    @field_validator('verb')
    @classmethod
    def validate_verb(cls, v):
        if v is not None and v.upper() not in ('GET', 'POST', 'PUT'):
            raise ValueError('verb must be "GET", "POST" or "PUT"')
        return v.upper() if v is not None else v
