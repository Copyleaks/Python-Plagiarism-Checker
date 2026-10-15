from typing import Optional
from pydantic import BaseModel, Field

from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionPatternMatchModel import CopyleaksAiTextDetectionPatternMatchModel
from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionPatternStatisticsModel import CopyleaksAiTextDetectionPatternStatisticsModel


class CopyleaksAiTextDetectionPatternsModel(BaseModel):
    """AI patterns found in the text, with their statistics and positions."""

    statistics: Optional[CopyleaksAiTextDetectionPatternStatisticsModel] = Field(
        default=None,
        description="Statistics of each pattern.",
        alias="statistics"
    )

    text: Optional[CopyleaksAiTextDetectionPatternMatchModel] = Field(
        default=None,
        description="Positions of the patterns in the plain text.",
        alias="text"
    )

    html: Optional[CopyleaksAiTextDetectionPatternMatchModel] = Field(
        default=None,
        description="Positions of the patterns in the HTML source. Present only for HTML submissions.",
        alias="html"
    )
