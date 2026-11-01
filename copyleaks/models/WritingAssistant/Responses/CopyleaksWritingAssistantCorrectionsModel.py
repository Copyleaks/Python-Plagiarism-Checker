from typing import Optional
from pydantic import BaseModel, Field

from copyleaks.models.WritingAssistant.Responses.CopyleaksWritingAssistantCorrectionsTextModel import CopyleaksWritingAssistantCorrectionsTextModel


class CopyleaksWritingAssistantCorrectionsModel(BaseModel):
    """Suggested corrections to the text."""

    text: Optional[CopyleaksWritingAssistantCorrectionsTextModel] = Field(
        default=None,
        description="Corrections in the plain text.",
        alias="text"
    )
