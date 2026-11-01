from typing import Optional
from pydantic import BaseModel, Field

from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionMatchTextModel import CopyleaksAiTextDetectionMatchTextModel


class CopyleaksAiTextDetectionMatchModel(BaseModel):
    """Location of a classified section in the scanned document."""

    text: Optional[CopyleaksAiTextDetectionMatchTextModel] = Field(
        default=None,
        description="Positions of the section in the plain text.",
        alias="text"
    )

    html: Optional[CopyleaksAiTextDetectionMatchTextModel] = Field(
        default=None,
        description="Positions of the section in the HTML source. Present only for HTML submissions.",
        alias="html"
    )
