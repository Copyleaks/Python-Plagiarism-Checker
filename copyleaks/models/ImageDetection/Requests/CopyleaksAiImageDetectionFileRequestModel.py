from typing import Any
from pydantic import ConfigDict, Field, field_validator

from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionBaseRequestModel import CopyleaksAiImageDetectionBaseRequestModel


class CopyleaksAiImageDetectionFileRequestModel(CopyleaksAiImageDetectionBaseRequestModel):
    """
    Request of AI Image Detection with the image file uploaded as multipart/form-data, without base64.
    Recommended for large images. Use it with `ImageDetectionClient.submit_file`.
    """

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, protected_namespaces=())

    image: Any = Field(
        ...,
        description="The image: bytes, or a file object opened in binary mode. Minimum 512x512px, maximum "
                    "6000x4500px (27 megapixels), less than 32MB. PNG, JPEG, BMP, WebP, HEIC/HEIF or AVIF.",
        exclude=True
    )

    file_name: str = Field(
        ...,
        description="The name of the image file including its extension. Maximum 255 characters.",
        alias="filename",
        max_length=255
    )

    model: str = Field(
        ...,
        description="The AI detection model, for example \"ai-image-1-ultra\". See `CopyleaksAiImageDetectionModels`.",
        alias="model"
    )

    sandbox: bool = Field(
        default=False,
        description="Use sandbox mode to test your integration without consuming any credits.",
        alias="sandbox"
    )

    @field_validator('image')
    @classmethod
    def validate_image(cls, v):
        if isinstance(v, (bytes, bytearray, memoryview)):
            if len(v) == 0:
                raise ValueError('image is empty')
            return v
        if callable(getattr(v, 'read', None)):
            return v
        raise ValueError('image must be bytes or a file object opened in binary mode')
