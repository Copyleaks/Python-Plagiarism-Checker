from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

SUPPORTED_IMAGE_PLAGIARISM_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.ico']


class CopyleaksImagePlagiarismRequestModel(BaseModel):
    """Request of the Image Plagiarism Detector (multipart upload). Use it with `ImagePlagiarismClient.check`."""

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    image: Any = Field(
        ...,
        description="The image: bytes, or a file object opened in binary mode. Less than 20MB, at most 75 megapixels. "
                    "JPG, JPEG, PNG, GIF, BMP, WebP or ICO.",
        exclude=True
    )

    file_name: str = Field(
        ...,
        description="The name of the image file including its extension. Maximum 255 characters. "
                    "`filename=` is accepted too.",
        alias="filename",
        max_length=255
    )

    sandbox: bool = Field(
        default=False,
        description="Use sandbox mode to test your integration without consuming credits. Returns mock results.",
        alias="sandbox"
    )

    developer_payload: Optional[str] = Field(
        default=None,
        description="A custom string that is returned unchanged in the response `developer_payload`.",
        alias="developerPayload"
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

    @field_validator('file_name')
    @classmethod
    def validate_file_name(cls, v):
        if not v or not v.strip():
            raise ValueError('filename is required')
        if not any(v.lower().endswith(ext) for ext in SUPPORTED_IMAGE_PLAGIARISM_EXTENSIONS):
            raise ValueError(f'filename must have one of the supported extensions: {", ".join(SUPPORTED_IMAGE_PLAGIARISM_EXTENSIONS)}')
        return v
