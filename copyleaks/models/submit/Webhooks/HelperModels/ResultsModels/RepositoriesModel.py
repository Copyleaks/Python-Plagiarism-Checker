from typing import Optional
from pydantic import Field

from .SharedResultsModel import SharedResultsModel
from .RepositoryMetadataModel import RepositoryMetadataModel


class RepositoriesModel(SharedResultsModel):
    """A result found in a Private Cloud Hub repository."""
    __positional_fields__ = ('repository_id', 'tags', 'id', 'title', 'introduction', 'matched_words', 'scan_id',
                             'metadata')

    repository_id: Optional[str] = Field(
        default=None,
        description="The repository Id that has the result.",
        alias="repositoryId"
    )

    metadata: Optional[RepositoryMetadataModel] = Field(
        default=None,
        description="Metadata of the result.",
        alias="metadata"
    )
