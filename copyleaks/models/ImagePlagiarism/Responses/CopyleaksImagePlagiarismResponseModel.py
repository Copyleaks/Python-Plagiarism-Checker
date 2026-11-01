from typing import Optional
from pydantic import ConfigDict, Field

from copyleaks.helpers.copyleaks_dict_access_mixin import CopyleaksDictAccessMixin
from copyleaks.models.ImagePlagiarism.Responses.CopyleaksImagePlagiarismMatchesModel import CopyleaksImagePlagiarismMatchesModel
from copyleaks.models.ImagePlagiarism.Responses.CopyleaksImagePlagiarismScannedImageModel import CopyleaksImagePlagiarismScannedImageModel


class CopyleaksImagePlagiarismResponseModel(CopyleaksDictAccessMixin):
    """
    Result of the Image Plagiarism Detector: where on the web copies of the image were found.
    An empty `matches.internet` list with zero scores means no matching image was found.
    """

    model_config = ConfigDict(populate_by_name=True)

    developer_payload: Optional[str] = Field(
        default=None,
        description="The developer payload of the request, unchanged. None when it was not provided.",
        alias="developerPayload"
    )

    scanned_image: Optional[CopyleaksImagePlagiarismScannedImageModel] = Field(
        default=None,
        description="Metadata about the submitted image and the scan.",
        alias="scannedImage"
    )

    matches: Optional[CopyleaksImagePlagiarismMatchesModel] = Field(
        default=None,
        description="The detection results.",
        alias="matches"
    )
