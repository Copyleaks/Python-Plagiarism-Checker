from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class CopyleaksImagePlagiarismScoreModel(BaseModel):
    """Match counts of the Image Plagiarism Detector."""

    model_config = ConfigDict(populate_by_name=True)

    total_matches: Optional[int] = Field(
        default=None,
        description="Total number of matching images found.",
        alias="totalMatches"
    )

    full_matches: Optional[int] = Field(
        default=None,
        description="Number of full matches (match type 0).",
        alias="fullMatches"
    )

    partial_matches: Optional[int] = Field(
        default=None,
        description="Number of partial matches (match type 1).",
        alias="partialMatches"
    )
