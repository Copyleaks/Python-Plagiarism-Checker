from typing import Optional
from pydantic import BaseModel, Field

from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionPatternsModel import CopyleaksAiTextDetectionPatternsModel


class CopyleaksAiTextDetectionExplainModel(BaseModel):
    """Explanation of the AI detection (AI Logic). Present only when explain was enabled for the scan."""

    patterns: Optional[CopyleaksAiTextDetectionPatternsModel] = Field(
        default=None,
        description="AI patterns found in the text.",
        alias="patterns"
    )
