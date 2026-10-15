from typing import Optional
from pydantic import BaseModel, Field

from copyleaks.models.shared.CopyleaksMediaMetadataModel import CopyleaksMediaMetadataModel


class CopyleaksAiVideoDetectionVideoInfoModel(BaseModel):
    """Information about the analyzed video."""

    duration: Optional[float] = Field(
        default=None,
        description="Total duration of the video in seconds.",
        alias="duration"
    )

    metadata: Optional[CopyleaksMediaMetadataModel] = Field(
        default=None,
        description="Metadata extracted from the video file, when available.",
        alias="metadata"
    )
