from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

MAX_OBJECT_DETECTION_ENTRIES = 3
MAX_OBJECT_LENGTH = 32


class CopyleaksAiImageObjectDetectionModel(BaseModel):
    """
    An object to locate and segment in the image, for AI Image Detection `object_detection`.
    The response then has a `detected_objects` entry, with a segmentation mask, for each object found.
    """

    object: str = Field(
        ...,
        description="The object to find, for example \"face\" or \"hand\". 1 to 32 characters.",
        alias="object"
    )

    @field_validator('object')
    @classmethod
    def validate_object(cls, v):
        if not isinstance(v, str) or not v.strip():
            raise ValueError('object must be a non-empty string')
        if len(v) > MAX_OBJECT_LENGTH:
            raise ValueError(f'object must be at most {MAX_OBJECT_LENGTH} characters')
        return v


def to_object_detection_list(value) -> Optional[List[CopyleaksAiImageObjectDetectionModel]]:
    """
    Validate an `object_detection` value: None, or 1 to 3 entries. An entry can be a
    `CopyleaksAiImageObjectDetectionModel`, a dict such as {"object": "face"}, or the object name as a string.
    """
    if value is None:
        return None
    if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple)):
        raise ValueError('object_detection must be a list of objects, for example ["face", "hand"]')
    if not 1 <= len(value) <= MAX_OBJECT_DETECTION_ENTRIES:
        raise ValueError(f'object_detection must contain 1 to {MAX_OBJECT_DETECTION_ENTRIES} entries. '
                         'Leave it unset to turn object detection off')
    items = []
    for entry in value:
        if isinstance(entry, CopyleaksAiImageObjectDetectionModel):
            items.append(entry)
        elif isinstance(entry, str):
            items.append(CopyleaksAiImageObjectDetectionModel(object=entry))
        else:
            items.append(CopyleaksAiImageObjectDetectionModel.model_validate(entry))
    return items
