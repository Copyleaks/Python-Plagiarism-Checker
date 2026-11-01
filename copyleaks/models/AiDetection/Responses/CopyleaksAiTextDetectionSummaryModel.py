from typing import Optional
from pydantic import AliasChoices, BaseModel, Field


class CopyleaksAiTextDetectionSummaryModel(BaseModel):
    """Summary of the AI text detection. Accepts the PascalCase `Human`/`Ai` keys of sandbox scans too."""

    human: Optional[float] = Field(
        default=None,
        description="Portion of the scanned text classified as human-written, from 0 to 1. None when missing.",
        alias="human",
        validation_alias=AliasChoices("human", "Human")
    )

    ai: Optional[float] = Field(
        default=None,
        description="Portion of the scanned text classified as AI-generated, from 0 to 1. None when missing.",
        alias="ai",
        validation_alias=AliasChoices("ai", "Ai")
    )
