from typing import Optional
from pydantic import Field, field_validator

from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionBaseRequestModel import CopyleaksAiImageDetectionBaseRequestModel


class CopyleaksAiImageDetectionRequestModel(CopyleaksAiImageDetectionBaseRequestModel):
    """Request of AI Image Detection with a base64 image. Use it with `ImageDetectionClient.submit`."""
    
    base64: str = Field(
        ...,
        description="The base64-encoded image data to be analyzed for AI generation.",
        example="aGVsbG8gd29ybGQ=",
        alias="base64"
    )
    
    file_name: str = Field(
        ...,
        description="The name of the image file including its extension.",
        example="my-image.png",
        alias="filename",
        max_length=255
    )
    
    model: str = Field(
        ...,
        description="The AI detection model to use for analysis. You can use either the full model name or its alias.",
        example="ai-image-1-ultra",
        alias="model"
    )
    
    sandbox: bool = Field(
        default=False,
        description="Use sandbox mode to test your integration with the Copyleaks API without consuming any credits.",
        example=False,
        alias="sandbox"
    )
    
    def __init__(self, base64: str, file_name: str, model: str, sandbox: bool = False,
                 mask_type: Optional[str] = None, object_detection: Optional[list] = None, **data):
        """
        Args:
            base64: The image, base64-encoded. 512x512 to 6000x4500 px, under 32 MB.
            file_name: File name with extension (.png, .jpg, .webp, .heic, .avif, ...), max 255 chars.
            model: Detection model, see CopyleaksAiImageDetectionModels.
            sandbox: Return mock results without using credits.
            mask_type: "binary" (default), "heatmap" or "none".
            object_detection: Up to 3 objects to locate, e.g. ["face", "hand"].
        """
        if mask_type is not None:
            data['maskType'] = mask_type
        if object_detection is not None:
            data['objectDetection'] = object_detection
        super().__init__(base64=base64, filename=file_name, model=model, sandbox=sandbox, **data)

    @field_validator('base64')
    def validate_base64(cls, v):
        if not v or not v.strip():
            raise ValueError('Base64 data is required and cannot be empty')
        return v
