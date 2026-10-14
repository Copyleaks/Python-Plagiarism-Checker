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

from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageObjectDetectionModel import CopyleaksAiImageObjectDetectionModel, to_object_detection_list

SUPPORTED_IMAGE_EXTENSIONS = ['.png', '.bmp', '.jpg', '.jpeg', '.webp', '.heic', '.heif', '.avif']


class CopyleaksAiImageDetectionRequestModel(BaseModel):
    """
    Request model for Copyleaks AI image detection.
    The request body is a JSON object containing the image to analyze.
    """
    
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

    def __init__(self, base64: str, file_name: str, model: str, sandbox: bool = False,
                 mask_type: Optional[str] = None, object_detection: Optional[list] = None, **data):
        """
        Initialize the CopyleaksAiImageDetectionRequestModel.

        Args:
            base64: The base64-encoded image data to be analyzed for AI generation.
                   Requirements:
                   - Minimum 512x512px, maximum 6000x4500px (27 megapixels), less than 32MB
                   - Supported formats: PNG, JPEG, BMP, WebP, HEIC/HEIF, AVIF
            file_name: The name of the image file including its extension.
                      Requirements:
                      - Supported extensions: .png, .bmp, .jpg, .jpeg, .webp, .heic, .heif, .avif
                      - Maximum 255 characters
            model: The AI detection model to use for analysis.
                  Available models:
                  - AI Image 1 Ultra: "ai-image-1-ultra" (see `CopyleaksAiImageDetectionModels`)
            sandbox: Use sandbox mode to test your integration with the Copyleaks API without consuming any credits.
                    Submit images for AI detection and get returned mock results, simulating Copyleaks' API functionality
                    to ensure you have successfully integrated the API.
                    This feature is intended to be used for development purposes only.
                    Default value is False.
            mask_type: Optional. The detection mask to return, one of `CopyleaksAiImageMaskTypes`:
                    "binary" (the server default), "heatmap" (adds `result.labels`) or "none" (no `result`).
            object_detection: Optional. 1 to 3 objects to locate and segment in the image, as strings
                    (for example ["face", "hand"]) or `CopyleaksAiImageObjectDetectionModel` objects.
                    The response then lists the objects found in `detected_objects`.
        """
        if mask_type is not None:
            data['maskType'] = mask_type
        if object_detection is not None:
            data['objectDetection'] = object_detection
        super().__init__(base64=base64, filename=file_name, model=model, sandbox=sandbox, **data)

    @field_validator('file_name')
    def validate_file_name(cls, v):
        """Validate the file name has a supported extension."""
        if not v:
            raise ValueError('File name is required')
        
        if not any(v.lower().endswith(ext) for ext in SUPPORTED_IMAGE_EXTENSIONS):
            raise ValueError(f'File name must have one of the supported extensions: {", ".join(SUPPORTED_IMAGE_EXTENSIONS)}')
        
        return v
    
    @field_validator('base64')
    def validate_base64(cls, v):
        """Validate base64 string is not empty."""
        if not v or not v.strip():
            raise ValueError('Base64 data is required and cannot be empty')
        return v
    
    @field_validator('model')
    def validate_model(cls, v):
        """Validate model name is not empty."""
        if not v or not v.strip():
            raise ValueError('Model name is required and cannot be empty')
        return v

    @field_validator('object_detection', mode='before')
    @classmethod
    def validate_object_detection(cls, v):
        """1 to 3 entries; strings are accepted as object names."""
        return to_object_detection_list(v)
