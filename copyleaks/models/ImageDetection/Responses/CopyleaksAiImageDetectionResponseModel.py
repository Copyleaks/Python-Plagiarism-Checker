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
from pydantic import BaseModel, ConfigDict, Field
from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionDetectedObjectModel import CopyleaksAiImageDetectionDetectedObjectModel
from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionImageInfoModel import CopyleaksAiImageDetectionImageInfoModel
from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionResultModel import CopyleaksAiImageDetectionResultModel
from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionScannedDocumentModel import CopyleaksAiImageDetectionScannedDocumentModel
from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionSummaryModel import CopyleaksAiImageDetectionSummaryModel
from copyleaks.models.submit.Webhooks.HelperModels.ErrorModels.ErrorModel import ErrorModel


class CopyleaksAiImageDetectionResponseModel(BaseModel):
    """
    Response model for Copyleaks AI image detection analysis.
    Contains the AI detection results, image information, and scan metadata.
    It is also the payload of the asynchronous AI Image Detection webhook:
    `CopyleaksAiImageDetectionResponseModel(**request.json)`. In a webhook, check `error` first: when the scan
    failed, the webhook has `error` and `developer_payload` and no result.
    Fields that the model does not define are kept.
    """

    model_config = ConfigDict(populate_by_name=True, extra='allow')

    error: Optional[ErrorModel] = Field(
        default=None,
        description="Why an asynchronous scan failed, in its webhook. None when the scan succeeded.",
        alias="error"
    )

    model: Optional[str] = Field(
        default=None,
        description="The version of the AI detection model used for analysis.",
        alias="model"
    )

    result: Optional[CopyleaksAiImageDetectionResultModel] = Field(
        default=None,
        description="RLE-encoded mask data of the AI-detected regions. None when the request used the \"none\" mask type.",
        alias="result"
    )

    summary: Optional[CopyleaksAiImageDetectionSummaryModel] = Field(
        default=None,
        description="Summary statistics of the AI detection analysis.",
        alias="summary"
    )

    is_ai_detected: Optional[bool] = Field(
        default=None,
        description="Whether the image was determined to be AI-generated.",
        alias="isAiDetected"
    )

    image_info: Optional[CopyleaksAiImageDetectionImageInfoModel] = Field(
        default=None,
        description="Information about the analyzed image.",
        alias="imageInfo"
    )

    detected_objects: Optional[List[CopyleaksAiImageDetectionDetectedObjectModel]] = Field(
        default=None,
        description="Present only when the request included object detection: one entry per object found in the image.",
        alias="detectedObjects"
    )

    scanned_document: Optional[CopyleaksAiImageDetectionScannedDocumentModel] = Field(
        default=None,
        description="Metadata about the scan operation.",
        alias="scannedDocument"
    )

    developer_payload: Optional[str] = Field(
        default=None,
        description="The developer payload of the asynchronous request, in its webhook result.",
        alias="developerPayload"
    )

    scan_type: Optional[str] = Field(
        default=None,
        description="\"sandbox\" for sandbox scans. Not sent for regular scans.",
        alias="scanType"
    )
