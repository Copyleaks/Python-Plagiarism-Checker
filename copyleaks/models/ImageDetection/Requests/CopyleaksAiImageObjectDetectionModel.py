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
