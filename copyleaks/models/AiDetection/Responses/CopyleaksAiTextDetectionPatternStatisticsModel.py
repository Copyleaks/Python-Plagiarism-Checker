from typing import List
from pydantic import BaseModel, Field, field_validator


class CopyleaksAiTextDetectionPatternStatisticsModel(BaseModel):
    """Statistics of the AI patterns found: parallel arrays, one entry per pattern. A null array is empty."""

    ai_count: List[float] = Field(
        default_factory=list,
        description="How often each pattern appears in AI-generated text.",
        alias="aiCount",
        serialization_alias="aiCount"
    )

    human_count: List[float] = Field(
        default_factory=list,
        description="How often each pattern appears in human-written text.",
        alias="humanCount",
        serialization_alias="humanCount"
    )

    proportion: List[float] = Field(
        default_factory=list,
        description="Ratio between the AI and the human frequency of each pattern.",
        alias="proportion"
    )

    source: List[int] = Field(
        default_factory=list,
        description="Source of each pattern: 1 = AI, 2 = humanizer.",
        alias="source"
    )

    @field_validator('ai_count', 'human_count', 'proportion', 'source', mode='before')
    @classmethod
    def statistics_none_to_empty(cls, v):
        return [] if v is None else v
