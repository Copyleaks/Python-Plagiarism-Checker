from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageObjectDetectionModel import CopyleaksAiImageObjectDetectionModel, to_object_detection_list

SUPPORTED_IMAGE_EXTENSIONS = ['.png', '.bmp', '.jpg', '.jpeg', '.webp', '.heic', '.heif', '.avif']


class CopyleaksAiImageDetectionBaseRequestModel(BaseModel):
    """
    Options and checks shared by the AI Image Detection requests. Each request defines `file_name` and `model`
    itself, because the JSON name of the file name differs (`filename` or `fileName`).
    """

    mask_type: Optional[str] = Field(
        default=None,
        description="The detection mask to return: \"binary\" (default), \"heatmap\" or \"none\" (synchronous only). "
                    "See `CopyleaksAiImageMaskTypes`.",
        alias="maskType"
    )

    object_detection: Optional[List[CopyleaksAiImageObjectDetectionModel]] = Field(
        default=None,
        description="Up to 3 objects to locate in the image, for example [\"face\", \"hand\"].",
        alias="objectDetection"
    )

    @field_validator('file_name', check_fields=False)
    @classmethod
    def validate_file_name(cls, v):
        if not v or not v.strip():
            raise ValueError('File name is required')
        if not any(v.lower().endswith(ext) for ext in SUPPORTED_IMAGE_EXTENSIONS):
            raise ValueError(f'File name must have one of the supported extensions: {", ".join(SUPPORTED_IMAGE_EXTENSIONS)}')
        return v

    @field_validator('model', check_fields=False)
    @classmethod
    def validate_model(cls, v):
        if not v or not v.strip():
            raise ValueError('Model name is required and cannot be empty')
        return v

    @field_validator('object_detection', mode='before')
    @classmethod
    def validate_object_detection(cls, v):
        return to_object_detection_list(v)
