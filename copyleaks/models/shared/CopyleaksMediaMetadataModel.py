from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class CopyleaksMediaMetadataModel(BaseModel):
    """Metadata extracted from the image or video file (for example C2PA provenance data), when available."""

    model_config = ConfigDict(populate_by_name=True)

    issued_time: Optional[str] = Field(
        default=None,
        description="When the file was created, if available.",
        alias="issuedTime"
    )

    issued_by: Optional[str] = Field(
        default=None,
        description="The AI service or tool that created the file, if detected.",
        alias="issuedBy"
    )

    app_or_device_used: Optional[str] = Field(
        default=None,
        description="The application or device used to create the file, if available.",
        alias="appOrDeviceUsed"
    )

    content_summary: Optional[str] = Field(
        default=None,
        description="A summary of how the file was generated, if available.",
        alias="contentSummary"
    )
