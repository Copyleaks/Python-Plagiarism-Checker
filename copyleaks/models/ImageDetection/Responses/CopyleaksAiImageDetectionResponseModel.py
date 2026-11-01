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
    Result of AI Image Detection, and the body of the asynchronous detection webhook (`Model(**request.json)`).
    In a webhook, check `error` first: a failed scan has only `error` and `developer_payload`.
    Undefined fields are kept.
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
