from typing import Optional
from pydantic import BaseModel, Field


class CopyleaksWritingAssistantScannedDocumentModel(BaseModel):
    """General information about the scanned document. Missing fields are None."""

    scan_id: Optional[str] = Field(
        default=None,
        description="The scan id given by the user.",
        alias="scanId",
        serialization_alias="scanId"
    )

    total_words: Optional[int] = Field(
        default=None,
        description="Total number of words found in the scanned text.",
        alias="totalWords",
        serialization_alias="totalWords"
    )

    total_excluded: Optional[int] = Field(
        default=None,
        description="Number of excluded words in the scanned text.",
        alias="totalExcluded",
        serialization_alias="totalExcluded"
    )

    actual_credits: Optional[int] = Field(
        default=None,
        description="The number of credits spent on the scan.",
        alias="actualCredits",
        serialization_alias="actualCredits"
    )

    expected_credits: Optional[int] = Field(
        default=None,
        description="The number of credits that was expected to be spent on the scan.",
        alias="expectedCredits",
        serialization_alias="expectedCredits"
    )

    creation_time: Optional[str] = Field(
        default=None,
        description="ISO 8601 creation time of the scan (UTC).",
        alias="creationTime",
        serialization_alias="creationTime"
    )
