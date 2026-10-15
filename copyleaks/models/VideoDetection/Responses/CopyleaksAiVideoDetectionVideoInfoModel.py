from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class CopyleaksAiVideoDetectionVideoMetadataModel(BaseModel):
    """Metadata extracted from the video file (for example C2PA provenance data), when available."""

    model_config = ConfigDict(populate_by_name=True)

    issued_time: Optional[str] = Field(
        default=None,
        description="When the video was created, if available.",
        alias="issuedTime"
    )

    issued_by: Optional[str] = Field(
        default=None,
        description="The AI service or tool that created the video, if present in the metadata.",
        alias="issuedBy"
    )

    app_or_device_used: Optional[str] = Field(
        default=None,
        description="The application or device used to create the video, if available.",
        alias="appOrDeviceUsed"
    )

    content_summary: Optional[str] = Field(
        default=None,
        description="A summary of how the video was generated, if available.",
        alias="contentSummary"
    )


class CopyleaksAiVideoDetectionVideoInfoModel(BaseModel):
    """Information about the analyzed video."""

    duration: Optional[float] = Field(
        default=None,
        description="Total duration of the video in seconds.",
        alias="duration"
    )

    metadata: Optional[CopyleaksAiVideoDetectionVideoMetadataModel] = Field(
        default=None,
        description="Metadata extracted from the video file, when available.",
        alias="metadata"
    )
