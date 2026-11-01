from typing import Optional
from pydantic import BaseModel, Field

from copyleaks.models.WritingAssistant.Responses.CopyleaksWritingAssistantCorrectionRangesModel import CopyleaksWritingAssistantCorrectionRangesModel


class CopyleaksWritingAssistantCorrectionsTextModel(BaseModel):
    """Corrections in the plain text."""

    chars: Optional[CopyleaksWritingAssistantCorrectionRangesModel] = Field(
        default=None,
        description="Character positions of the corrections.",
        alias="chars"
    )
