from typing import List, Optional
from pydantic import Field, field_validator

from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel, none_to_empty_list, str_or_number_to_str
from .TagsModel import TagsModel


class InternalAiDataModel(CopyleaksWebhookBaseModel):
    """A match in the Copyleaks internal AI database, found by Internal AI Source Match."""

    id: Optional[str] = Field(
        default=None,
        description="Short identifier for the match.",
        alias="id"
    )

    title: Optional[str] = Field(
        default=None,
        description="Title of the matched database entry.",
        alias="title"
    )

    introduction: Optional[str] = Field(
        default=None,
        description="Sample excerpt of the matched content.",
        alias="introduction"
    )

    matched_words: Optional[int] = Field(
        default=None,
        description="Total number of words matched from the Copyleaks internal AI database.",
        alias="matchedWords"
    )

    identical_words: Optional[int] = Field(
        default=None,
        description="Number of exactly identical words.",
        alias="identicalWords"
    )

    similar_words: Optional[int] = Field(
        default=None,
        description="Number of similar but not identical words.",
        alias="similarWords"
    )

    paraphrased_words: Optional[int] = Field(
        default=None,
        description="Number of paraphrased words.",
        alias="paraphrasedWords"
    )

    total_words: Optional[int] = Field(
        default=None,
        description="Total word count of the matched database entry.",
        alias="totalWords"
    )

    tags: List[TagsModel] = Field(
        default_factory=list,
        description="Result tags.",
        alias="tags"
    )

    @field_validator('id', mode='before')
    @classmethod
    def id_to_str(cls, v):
        return str_or_number_to_str(v)

    @field_validator('tags', mode='before')
    @classmethod
    def tags_none_to_empty(cls, v):
        return none_to_empty_list(v)
