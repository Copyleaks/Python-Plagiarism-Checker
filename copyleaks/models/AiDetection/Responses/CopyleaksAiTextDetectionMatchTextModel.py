from typing import Optional
from pydantic import BaseModel, Field

from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionPositionsModel import CopyleaksAiTextDetectionPositionsModel


class CopyleaksAiTextDetectionMatchTextModel(BaseModel):
    """Character and word positions of a classified section."""

    chars: Optional[CopyleaksAiTextDetectionPositionsModel] = Field(
        default=None,
        description="Character positions of the section.",
        alias="chars"
    )

    words: Optional[CopyleaksAiTextDetectionPositionsModel] = Field(
        default=None,
        description="Word positions of the section.",
        alias="words"
    )
