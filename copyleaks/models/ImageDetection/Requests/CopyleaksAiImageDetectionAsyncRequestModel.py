from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageObjectDetectionModel import CopyleaksAiImageObjectDetectionModel, to_object_detection_list


def validate_headers(value):
    """Headers are a list of [name, value] pairs."""
    if value is None:
        return None
    if not isinstance(value, (list, tuple)):
        raise ValueError('headers must be a list of [name, value] pairs')
    pairs = []
    for pair in value:
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError('each header must be a [name, value] pair')
        pairs.append([pair[0], pair[1]])
    return pairs


class CopyleaksAiImageDetectionWebhooksModel(BaseModel):
    """Where Copyleaks sends the result of an asynchronous AI Image Detection."""

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


class CopyleaksAiImageDetectionAsyncRequestModel(BaseModel):
    """
    Request of asynchronous AI Image Detection: Copyleaks downloads the image from `url` and sends the result to
    `webhooks.url`. Use it with `ImageDetectionClient.submit_async`.
    """

    model_config = ConfigDict(populate_by_name=True, protected_namespaces=())

    url: str = Field(
        ...,
        description="Publicly accessible URL of the image to analyze.",
        alias="url"
    )

    file_name: str = Field(
        ...,
        description="The name of the image file including its extension, for example \"image1.png\".",
        alias="fileName"
    )

    model: str = Field(
        ...,
        description="The AI detection model, for example \"ai-image-1-ultra\". See `CopyleaksAiImageDetectionModels`.",
        alias="model"
    )

    webhooks: CopyleaksAiImageDetectionWebhooksModel = Field(
        ...,
        description="Where to send the result. A dict such as {\"url\": \"https://...\"} is accepted.",
        alias="webhooks"
    )

    mask_type: Optional[str] = Field(
        default=None,
        description="The detection mask to include in the result: \"binary\" (default) or \"heatmap\". See `CopyleaksAiImageMaskTypes`.",
        alias="maskType"
    )

    object_detection: Optional[List[CopyleaksAiImageObjectDetectionModel]] = Field(
        default=None,
        description="Up to 3 objects to locate in the image, for example [\"face\", \"hand\"].",
        alias="objectDetection"
    )

    headers: Optional[List[List[str]]] = Field(
        default=None,
        description="Custom headers to send when Copyleaks downloads the image from `url`, as [name, value] pairs.",
        alias="headers"
    )

    sandbox: Optional[bool] = Field(
        default=None,
        description="Use sandbox mode to test your integration without consuming any credits. The server default is False.",
        alias="sandbox"
    )

    developer_payload: Optional[str] = Field(
        default=None,
        description="A custom string that Copyleaks includes in the webhook result.",
        alias="developerPayload"
    )

    @field_validator('url', 'file_name', 'model')
    @classmethod
    def validate_required_text(cls, v):
        if not v or not v.strip():
            raise ValueError('value is required and cannot be empty')
        return v

    @field_validator('object_detection', mode='before')
    @classmethod
    def validate_object_detection(cls, v):
        return to_object_detection_list(v)

    @field_validator('headers', mode='before')
    @classmethod
    def validate_headers(cls, v):
        return validate_headers(v)
