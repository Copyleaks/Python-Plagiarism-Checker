from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class CopyleaksAiVideoDetectionSummaryModel(BaseModel):
    """Overall AI ratios of the video, from 0.0 to 1.0, calculated from the scored segments only."""

    model_config = ConfigDict(populate_by_name=True)

    audio_ai_ratio: Optional[float] = Field(
        default=None,
        description="AI-detected audio duration divided by the total audible duration.",
        alias="audioAIRatio"
    )

    visual_ai_ratio: Optional[float] = Field(
        default=None,
        description="AI-detected visual duration divided by the total visible duration.",
        alias="visualAIRatio"
    )

    overall_ai_ratio: Optional[float] = Field(
        default=None,
        description="Combined AI ratio of the audio and visual tracks, relative to the total video duration.",
        alias="overallAIRatio"
    )
