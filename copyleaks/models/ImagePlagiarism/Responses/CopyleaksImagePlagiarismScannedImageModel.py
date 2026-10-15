from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class CopyleaksImagePlagiarismScannedImageModel(BaseModel):
    """Metadata about the submitted image and the scan. Missing fields are None."""

    model_config = ConfigDict(populate_by_name=True)

    scan_id: Optional[str] = Field(
        default=None,
        description="The scan ID provided in the request path.",
        alias="scanId"
    )

    expected_credits: Optional[int] = Field(
        default=None,
        description="The number of credits expected to be charged for this scan.",
        alias="expectedCredits"
    )

    actual_credits: Optional[int] = Field(
        default=None,
        description="The number of credits actually charged for this scan.",
        alias="actualCredits"
    )

    creation_time: Optional[str] = Field(
        default=None,
        description="UTC timestamp of when the scan was created (ISO 8601).",
        alias="creationTime"
    )

    width: Optional[int] = Field(
        default=None,
        description="Width of the submitted image in pixels.",
        alias="width"
    )

    height: Optional[int] = Field(
        default=None,
        description="Height of the submitted image in pixels.",
        alias="height"
    )

    filename: Optional[str] = Field(
        default=None,
        description="The filename provided in the request.",
        alias="filename"
    )
