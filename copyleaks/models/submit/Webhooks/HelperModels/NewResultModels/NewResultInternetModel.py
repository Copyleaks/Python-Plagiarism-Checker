from typing import List, Optional
from pydantic import AliasChoices, Field, field_validator

from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel, none_to_empty_list, str_or_number_to_str
from ..BaseModels.MetadataModel import MetadataModel
from ..ResultsModels.TagsModel import TagsModel


class NewResultsInternetModel(CopyleaksWebhookBaseModel):
    """A result found on the internet."""
    __positional_fields__ = ('id', 'title', 'introduction', 'matched_words', 'metadata', 'url')

    id: Optional[str] = Field(
        default=None,
        description="Unique result ID to identify the result. `id_val=` is accepted too.",
        alias="id",
        validation_alias=AliasChoices("id", "id_val")
    )

    title: Optional[str] = Field(
        default=None,
        description="Document title. Mostly extracted from the document content.",
        alias="title"
    )

    introduction: Optional[str] = Field(
        default=None,
        description="Document brief introduction. Mostly extracted from the document content.",
        alias="introduction"
    )

    matched_words: Optional[int] = Field(
        default=None,
        description="Total matched words between this result and the scanned document.",
        alias="matchedWords"
    )

    metadata: Optional[MetadataModel] = Field(
        default=None,
        description="Metadata of the result.",
        alias="metadata"
    )

    url: Optional[str] = Field(
        default=None,
        description="Public URL of the resource.",
        alias="url"
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
