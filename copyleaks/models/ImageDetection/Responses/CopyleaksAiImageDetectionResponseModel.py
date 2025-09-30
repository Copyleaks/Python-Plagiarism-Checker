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

from pydantic import BaseModel, Field
from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionImageInfoModel import CopyleaksAiImageDetectionImageInfoModel
from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionResultModel import CopyleaksAiImageDetectionResultModel
from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionScannedDocumentModel import CopyleaksAiImageDetectionScannedDocumentModel
from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionSummaryModel import CopyleaksAiImageDetectionSummaryModel



class CopyleaksAiImageDetectionResponseModel(BaseModel):
    """
    Response model for Copyleaks AI image detection analysis.
    Contains the AI detection results, image information, and scan metadata.
    """
    
    model: str = Field(
        ...,
        description="The version of the AI detection model used for analysis.",
        alias="model"
    )
    
    result: CopyleaksAiImageDetectionResultModel = Field(
        ...,
        description="RLE-encoded mask data containing arrays of start positions and lengths for AI-detected regions.",
        alias="result"
    )
    
    summary: CopyleaksAiImageDetectionSummaryModel = Field(
        ...,
        description="Summary statistics of the AI detection analysis.",
        alias="summary"
    )
    
    image_info: CopyleaksAiImageDetectionImageInfoModel = Field(
        ...,
        description="Information about the analyzed image.",
        alias="imageInfo"
    )
    
    scanned_document: CopyleaksAiImageDetectionScannedDocumentModel = Field(
        ...,
        description="Metadata about the scan operation.",
        alias="scannedDocument"
    )
