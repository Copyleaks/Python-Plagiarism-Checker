from typing import Optional
from pydantic import BaseModel, Field


class CopyleaksAiImageDetectionScannedDocumentModel(BaseModel):
    """Metadata about the AI image detection scan operation. Missing fields are None."""

    scan_id: Optional[str] = Field(
        default=None,
        description="The unique identifier for this scan.",
        alias="scanId"
    )

    actual_credits: Optional[int] = Field(
        default=None,
        description="The actual number of credits consumed by this scan.",
        alias="actualCredits"
    )

    expected_credits: Optional[int] = Field(
        default=None,
        description="The expected number of credits for this scan.",
        alias="expectedCredits"
    )

    creation_time: Optional[str] = Field(
        default=None,
        description="ISO 8601 timestamp of when the scan was created.",
        alias="creationTime"
    )
