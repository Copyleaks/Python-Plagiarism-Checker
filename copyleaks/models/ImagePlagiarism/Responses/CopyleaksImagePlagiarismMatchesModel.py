from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from copyleaks.models.ImagePlagiarism.Responses.CopyleaksImagePlagiarismInternetMatchModel import CopyleaksImagePlagiarismInternetMatchModel
from copyleaks.models.ImagePlagiarism.Responses.CopyleaksImagePlagiarismScoreModel import CopyleaksImagePlagiarismScoreModel


class CopyleaksImagePlagiarismMatchesModel(BaseModel):
    """The detection results of the Image Plagiarism Detector."""

    internet: List[CopyleaksImagePlagiarismInternetMatchModel] = Field(
        default_factory=list,
        description="Matching images found on the web: full matches first, then partial matches.",
        alias="internet"
    )

    score: Optional[CopyleaksImagePlagiarismScoreModel] = Field(
        default=None,
        description="A summary of match counts.",
        alias="score"
    )

    @field_validator('internet', mode='before')
    @classmethod
    def none_to_empty(cls, v):
        return [] if v is None else v
