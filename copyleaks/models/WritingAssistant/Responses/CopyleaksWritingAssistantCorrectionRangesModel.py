from typing import List
from pydantic import BaseModel, Field


class CopyleaksWritingAssistantCorrectionRangesModel(BaseModel):
    """Corrections as parallel arrays, one entry per correction. A missing array is an empty list."""

    types: List[int] = Field(
        default_factory=list,
        description="Correction type ids. See `WritingAssistantClient.get_correction_types`.",
        alias="types"
    )

    starts: List[int] = Field(
        default_factory=list,
        description="Start positions of the corrected segments.",
        alias="starts"
    )

    lengths: List[int] = Field(
        default_factory=list,
        description="Lengths of the corrected segments.",
        alias="lengths"
    )

    operation_texts: List[str] = Field(
        default_factory=list,
        description="Suggested replacement text for each corrected segment.",
        alias="operationTexts",
        serialization_alias="operationTexts"
    )
