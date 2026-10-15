from typing import Optional
from pydantic import BaseModel, Field

from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionResultModel import CopyleaksAiImageDetectionResultModel


class CopyleaksAiImageDetectionDetectedObjectModel(BaseModel):
    """
    An object from the request's `object_detection` list that was found in the image.
    Objects that were requested but not found are not listed, so look entries up by `object`.
    """

    object: Optional[str] = Field(
        default=None,
        description="The object from the request that this entry corresponds to.",
        alias="object"
    )

    mask: Optional[CopyleaksAiImageDetectionResultModel] = Field(
        default=None,
        description="Run-Length Encoded (RLE) segmentation mask of the object, in the coordinate space of `image_info.shape`.",
        alias="mask"
    )
