from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class CopyleaksAiVideoDetectionSegmentsModel(BaseModel):
    """Time segments of a video track, as parallel arrays of start positions and lengths in milliseconds."""

    starts: List[int] = Field(
        default_factory=list,
        description="Start positions of the segments, in milliseconds.",
        alias="starts"
    )

    lengths: List[int] = Field(
        default_factory=list,
        description="Durations of the segments, in milliseconds, one per start position.",
        alias="lengths"
    )

    @field_validator('starts', 'lengths', mode='before')
    @classmethod
    def none_to_empty(cls, v):
        return [] if v is None else v


class CopyleaksAiVideoDetectionTrackResultModel(CopyleaksAiVideoDetectionSegmentsModel):
    """
    AI detection result of a video track (audio or visual): AI-detected segments in `starts`/`lengths`,
    segments that were not scored in `exclude`.
    """

    exclude: Optional[CopyleaksAiVideoDetectionSegmentsModel] = Field(
        default=None,
        description="Segments of the track that were not scored and are excluded from the AI ratios.",
        alias="exclude"
    )
