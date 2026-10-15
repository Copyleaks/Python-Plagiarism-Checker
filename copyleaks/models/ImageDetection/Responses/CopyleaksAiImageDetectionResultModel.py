from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class CopyleaksAiImageDetectionResultModel(BaseModel):
    """RLE-encoded mask data for AI-detected regions."""

    starts: List[int] = Field(
        default_factory=list,
        description="Start positions of AI-detected segments in the flattened image array.",
        alias="starts"
    )

    lengths: List[int] = Field(
        default_factory=list,
        description="Lengths of AI-detected segments corresponding to each start position.",
        alias="lengths"
    )

    labels: Optional[List[int]] = Field(
        default=None,
        description="Present only for the \"heatmap\" mask type: one confidence band, from 0 (lowest) to 4 (highest), per segment.",
        alias="labels"
    )

    @field_validator('starts', 'lengths', mode='before')
    @classmethod
    def none_to_empty(cls, v):
        return [] if v is None else v
