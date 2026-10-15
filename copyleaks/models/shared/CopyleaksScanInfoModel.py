from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class CopyleaksScanInfoModel(BaseModel):
    """ID, credits and creation time of an AI Image or AI Video Detection scan. Missing fields are None."""

    model_config = ConfigDict(populate_by_name=True)

    scan_id: Optional[str] = Field(
        default=None,
        description="The scan ID provided in the request.",
        alias="scanId"
    )

    actual_credits: Optional[int] = Field(
        default=None,
        description="The number of credits the scan used.",
        alias="actualCredits"
    )

    expected_credits: Optional[int] = Field(
        default=None,
        description="The expected number of credits for the scan.",
        alias="expectedCredits"
    )

    creation_time: Optional[str] = Field(
        default=None,
        description="ISO 8601 timestamp of when the scan was created.",
        alias="creationTime"
    )
