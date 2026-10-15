from typing import Optional
from pydantic import BaseModel, Field


class CopyleaksImagePlagiarismWebPageModel(BaseModel):
    """A web page that contains a matching image."""

    url: Optional[str] = Field(
        default=None,
        description="The URL of the web page containing the matching image.",
        alias="url"
    )
