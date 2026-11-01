from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

from copyleaks.models.ImagePlagiarism.Responses.CopyleaksImagePlagiarismWebPageModel import CopyleaksImagePlagiarismWebPageModel


class CopyleaksImagePlagiarismInternetMatchModel(BaseModel):
    """A matching image found on the web."""

    model_config = ConfigDict(populate_by_name=True)

    url: Optional[str] = Field(
        default=None,
        description="The URL of the matching image.",
        alias="url"
    )

    match_type: Optional[int] = Field(
        default=None,
        description="0 = full match (exact or near-exact copy), 1 = partial match (cropped, resized or otherwise modified). "
                    "See `CopyleaksImagePlagiarismMatchTypes`.",
        alias="matchType"
    )

    web_pages: List[CopyleaksImagePlagiarismWebPageModel] = Field(
        default_factory=list,
        description="The web pages where the image was found. Empty when the image was not located on any page.",
        alias="webPages"
    )

    @field_validator('web_pages', mode='before')
    @classmethod
    def none_to_empty(cls, v):
        return [] if v is None else v
