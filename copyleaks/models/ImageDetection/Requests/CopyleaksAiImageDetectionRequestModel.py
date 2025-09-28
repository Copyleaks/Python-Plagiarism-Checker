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

from pydantic import BaseModel, Field, field_validator, validator


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
        example="ai-image-1-ultra-01-09-2025",
        alias="model"
    )
    
    sandbox: bool = Field(
        default=False,
        description="Use sandbox mode to test your integration with the Copyleaks API without consuming any credits.",
        example=False,
        alias="sandbox"
    )
    
    def __init__(self, base64: str, file_name: str, model: str, sandbox: bool = False, **data):
        """
        Initialize the CopyleaksAiImageDetectionRequestModel.
        
        Args:
            base64: The base64-encoded image data to be analyzed for AI generation.
                   Requirements:
                   - Minimum 512×512px, maximum 16 megapixels, less than 32MB
                   - Supported formats: PNG, JPEG, BMP, WebP, HEIC/HEIF
            file_name: The name of the image file including its extension.
                      Requirements:
                      - Supported extensions: .png, .bmp, .jpg, .jpeg, .webp, .heic, .heif
                      - Maximum 255 characters
            model: The AI detection model to use for analysis.
                  Available models:
                  - AI Image 1 Ultra: "ai-image-1-ultra-01-09-2025" (full name) or "ai-image-1-ultra" (alias)
                    AI image detection model. Produces an overlay of the detected AI segments.
            sandbox: Use sandbox mode to test your integration with the Copyleaks API without consuming any credits.
                    Submit images for AI detection and get returned mock results, simulating Copyleaks' API functionality 
                    to ensure you have successfully integrated the API.
                    This feature is intended to be used for development purposes only.
                    Default value is False.
        """
        super().__init__(base64=base64, filename=file_name, model=model, sandbox=sandbox, **data)
    
    @field_validator('file_name')
    def validate_file_name(cls, v):
        """Validate the file name has a supported extension."""
        if not v:
            raise ValueError('File name is required')
        
        supported_extensions = ['.png', '.bmp', '.jpg', '.jpeg', '.webp', '.heic', '.heif']
        if not any(v.lower().endswith(ext) for ext in supported_extensions):
            raise ValueError(f'File name must have one of the supported extensions: {", ".join(supported_extensions)}')
        
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

