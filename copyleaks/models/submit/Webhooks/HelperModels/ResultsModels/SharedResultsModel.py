from typing import List, Optional
from pydantic import AliasChoices, Field, field_validator

from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel, none_to_empty_list, str_or_number_to_str
from ..BaseModels.MetadataModel import MetadataModel
from .TagsModel import TagsModel


class SharedResultsModel(CopyleaksWebhookBaseModel):
    __positional_fields__ = ('id', 'title', 'introduction', 'matched_words', 'scan_id', 'metadata')

    id: Optional[str] = Field(
        default=None,
        description="Unique result ID to identify this result. `id_val=` is accepted too.",
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

    scan_id: Optional[str] = Field(
        default=None,
        description="The scan id of the result, when it is one of your own submissions.",
        alias="scanId"
    )

    metadata: Optional[MetadataModel] = Field(
        default=None,
        description="Metadata of the result.",
        alias="metadata"
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

    @property
    def id_val(self):
        """Same as `id`."""
        return self.id
