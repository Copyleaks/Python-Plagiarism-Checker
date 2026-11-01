from typing import Optional
from pydantic import BaseModel, Field

from copyleaks.models.WritingAssistant.Responses.CopyleaksWritingAssistantReadabilityModel import CopyleaksWritingAssistantReadabilityModel
from copyleaks.models.WritingAssistant.Responses.CopyleaksWritingAssistantScoreCorrectionsModel import CopyleaksWritingAssistantScoreCorrectionsModel
from copyleaks.models.WritingAssistant.Responses.CopyleaksWritingAssistantStatisticsModel import CopyleaksWritingAssistantStatisticsModel


class CopyleaksWritingAssistantScoreModel(BaseModel):
    """Writing quality scores, readability and text statistics."""

    corrections: Optional[CopyleaksWritingAssistantScoreCorrectionsModel] = Field(
        default=None,
        description="Correction counts and scores per category, and the overall score.",
        alias="corrections"
    )

    readability: Optional[CopyleaksWritingAssistantReadabilityModel] = Field(
        default=None,
        description="Readability of the text.",
        alias="readability"
    )

    statistics: Optional[CopyleaksWritingAssistantStatisticsModel] = Field(
        default=None,
        description="Statistics of the text.",
        alias="statistics"
    )
