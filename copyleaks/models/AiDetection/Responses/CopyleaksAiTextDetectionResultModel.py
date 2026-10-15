from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionMatchModel import CopyleaksAiTextDetectionMatchModel


class CopyleaksAiTextDetectionResultModel(BaseModel):
    """A classified section of the scanned text."""

    classification: Optional[int] = Field(
        default=None,
        description="Classification of the section: 1 = human-written text, 2 = AI-generated text. None when missing.",
        alias="classification"
    )

    probability: Optional[float] = Field(
        default=None,
        description="Confidence of the classification. Deprecated by the server and may be missing.",
        alias="probability"
    )

    matches: List[CopyleaksAiTextDetectionMatchModel] = Field(
        default_factory=list,
        description="Locations of the section in the scanned document.",
        alias="matches"
    )

    @field_validator('matches', mode='before')
    @classmethod
    def matches_none_to_empty(cls, v):
        return [] if v is None else v
