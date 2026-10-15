from typing import Optional
from pydantic import BaseModel, Field


class CopyleaksWritingAssistantReadabilityModel(BaseModel):
    """Readability of the text."""

    score: Optional[int] = Field(
        default=None,
        description="Readability score.",
        alias="score"
    )

    readability_level: Optional[int] = Field(
        default=None,
        description="Readability level.",
        alias="readabilityLevel",
        serialization_alias="readabilityLevel"
    )

    readability_level_text: Optional[str] = Field(
        default=None,
        description="Readability level as text, e.g. \"10th to 12th Grader\".",
        alias="readabilityLevelText",
        serialization_alias="readabilityLevelText"
    )

    readability_level_description: Optional[str] = Field(
        default=None,
        description="Description of the readability level, e.g. \"Fairly difficult to read\".",
        alias="readabilityLevelDescription",
        serialization_alias="readabilityLevelDescription"
    )
