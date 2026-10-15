from typing import List, Optional
from pydantic import ConfigDict, Field, field_validator

from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionBaseRequestModel import CopyleaksAiImageDetectionBaseRequestModel
from copyleaks.models.shared.CopyleaksDetectionWebhooksModel import CopyleaksDetectionWebhooksModel, validate_headers


class CopyleaksAiImageDetectionAsyncRequestModel(CopyleaksAiImageDetectionBaseRequestModel):
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

    webhooks: CopyleaksDetectionWebhooksModel = Field(
        ...,
        description="Where to send the result. A dict such as {\"url\": \"https://...\"} is accepted.",
        alias="webhooks"
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

    @field_validator('url')
    @classmethod
    def validate_url(cls, v):
        if not v or not v.strip():
            raise ValueError('value is required and cannot be empty')
        return v

    @field_validator('headers', mode='before')
    @classmethod
    def validate_headers(cls, v):
        return validate_headers(v)
