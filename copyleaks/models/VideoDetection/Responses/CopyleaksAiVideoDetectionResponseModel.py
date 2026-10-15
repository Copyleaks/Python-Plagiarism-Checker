from typing import Optional
from pydantic import ConfigDict, Field

from copyleaks.helpers.copyleaks_dict_access_mixin import CopyleaksDictAccessMixin
from copyleaks.models.submit.Webhooks.HelperModels.ErrorModels.ErrorModel import ErrorModel
from copyleaks.models.VideoDetection.Responses.CopyleaksAiVideoDetectionScannedVideoModel import CopyleaksAiVideoDetectionScannedVideoModel
from copyleaks.models.VideoDetection.Responses.CopyleaksAiVideoDetectionSummaryModel import CopyleaksAiVideoDetectionSummaryModel
from copyleaks.models.VideoDetection.Responses.CopyleaksAiVideoDetectionTrackResultModel import CopyleaksAiVideoDetectionTrackResultModel
from copyleaks.models.VideoDetection.Responses.CopyleaksAiVideoDetectionVideoInfoModel import CopyleaksAiVideoDetectionVideoInfoModel


class CopyleaksAiVideoDetectionResponseModel(CopyleaksDictAccessMixin):
    """
    Result of AI Video Detection, the body of its webhook (`Model(**request.json)`). Check `error` first: a failed scan
    has only `error` and `developer_payload`. Track positions and lengths are in ms. Undefined fields are kept.
    """

    model_config = ConfigDict(populate_by_name=True, extra='allow', protected_namespaces=())

    error: Optional[ErrorModel] = Field(
        default=None,
        description="Why the scan failed. None when the scan succeeded.",
        alias="error"
    )

    model: Optional[str] = Field(
        default=None,
        description="The version of the AI detection model used for the analysis.",
        alias="model"
    )

    audio_result: Optional[CopyleaksAiVideoDetectionTrackResultModel] = Field(
        default=None,
        description="AI-detected segments of the audio track.",
        alias="audioResult"
    )

    visual_result: Optional[CopyleaksAiVideoDetectionTrackResultModel] = Field(
        default=None,
        description="AI-detected segments of the visual track.",
        alias="visualResult"
    )

    summary: Optional[CopyleaksAiVideoDetectionSummaryModel] = Field(
        default=None,
        description="Overall AI ratios of the video.",
        alias="summary"
    )

    is_ai_detected: Optional[bool] = Field(
        default=None,
        description="Whether the video was determined to contain AI-generated content.",
        alias="isAiDetected"
    )

    video_info: Optional[CopyleaksAiVideoDetectionVideoInfoModel] = Field(
        default=None,
        description="Information about the analyzed video.",
        alias="videoInfo"
    )

    scanned_video: Optional[CopyleaksAiVideoDetectionScannedVideoModel] = Field(
        default=None,
        description="Metadata about the scan.",
        alias="scannedVideo"
    )

    developer_payload: Optional[str] = Field(
        default=None,
        description="The developer payload of the request.",
        alias="developerPayload"
    )
