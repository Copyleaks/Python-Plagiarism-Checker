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
    Result of AI Video Detection, delivered to the webhook of `VideoDetectionClient.submit`.
    Parse the webhook body with `CopyleaksAiVideoDetectionResponseModel(**request.json)`.
    Check `error` first: when the scan failed, the webhook has `error` and `developer_payload` and no result.
    Positions and lengths of the track results are in milliseconds.
    Fields that the model does not define are kept.
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
