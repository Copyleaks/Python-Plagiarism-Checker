from typing import Optional
from pydantic import BaseModel, Field

from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionPositionsModel import CopyleaksAiTextDetectionPositionsModel


class CopyleaksAiTextDetectionPatternMatchModel(BaseModel):
    """Positions of the AI patterns found in the text."""

    chars: Optional[CopyleaksAiTextDetectionPositionsModel] = Field(
        default=None,
        description="Character positions of the patterns.",
        alias="chars"
    )

    words: Optional[CopyleaksAiTextDetectionPositionsModel] = Field(
        default=None,
        description="Word positions of the patterns.",
        alias="words"
    )
