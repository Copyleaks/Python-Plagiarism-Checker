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

from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionRequestModel import SUPPORTED_IMAGE_EXTENSIONS
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageObjectDetectionModel import CopyleaksAiImageObjectDetectionModel, to_object_detection_list


class CopyleaksAiImageDetectionFileRequestModel(BaseModel):
    """
    Request of AI Image Detection with the image file uploaded as multipart/form-data, without base64.
    Recommended for large images. Use it with `ImageDetectionClient.submit_file`.

    Example:
        with open('photo.png', 'rb') as f:
            request = CopyleaksAiImageDetectionFileRequestModel(
                image=f, file_name='photo.png', model=CopyleaksAiImageDetectionModels.AI_IMAGE_1_ULTRA, sandbox=True)
            response = Copyleaks.ImageDetectionClient.submit_file(auth_token, scan_id, request)
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

    mask_type: Optional[str] = Field(
        default=None,
        description="The detection mask to return: \"binary\" (default), \"heatmap\" or \"none\". See `CopyleaksAiImageMaskTypes`.",
        alias="maskType"
    )

    object_detection: Optional[List[CopyleaksAiImageObjectDetectionModel]] = Field(
        default=None,
        description="Up to 3 objects to locate in the image, for example [\"face\", \"hand\"].",
        alias="objectDetection"
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
            raise ValueError('File name is required')
        if not any(v.lower().endswith(ext) for ext in SUPPORTED_IMAGE_EXTENSIONS):
            raise ValueError(f'File name must have one of the supported extensions: {", ".join(SUPPORTED_IMAGE_EXTENSIONS)}')
        return v

    @field_validator('model')
    @classmethod
    def validate_model(cls, v):
        if not v or not v.strip():
            raise ValueError('Model name is required and cannot be empty')
        return v

    @field_validator('object_detection', mode='before')
    @classmethod
    def validate_object_detection(cls, v):
        return to_object_detection_list(v)
