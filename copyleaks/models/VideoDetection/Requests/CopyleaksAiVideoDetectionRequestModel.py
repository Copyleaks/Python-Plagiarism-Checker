from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

from copyleaks.models.shared.CopyleaksDetectionWebhooksModel import CopyleaksDetectionWebhooksModel, validate_headers

SUPPORTED_VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.mpg', '.m4v', '.3gp', '.mxf']


class CopyleaksAiVideoDetectionRequestModel(BaseModel):
    """
    Request of AI Video Detection: Copyleaks downloads the video from `url` and sends the result to `webhooks.url`.
    Use it with `VideoDetectionClient.submit`.
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

    webhooks: CopyleaksDetectionWebhooksModel = Field(
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
