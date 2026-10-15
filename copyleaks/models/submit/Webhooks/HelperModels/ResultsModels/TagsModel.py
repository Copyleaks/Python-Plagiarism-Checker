from typing import Optional
from pydantic import Field

from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel


class TagsModel(CopyleaksWebhookBaseModel):
    __positional_fields__ = ('code', 'title', 'description')

    code: Optional[str] = Field(
        default=None,
        description="Unique ID that signifies the type of result tag.",
        alias="code"
    )

    title: Optional[str] = Field(
        default=None,
        description="A simple name for this tag.",
        alias="title"
    )

    description: Optional[str] = Field(
        default=None,
        description="Short text describing this tag.",
        alias="description"
    )
