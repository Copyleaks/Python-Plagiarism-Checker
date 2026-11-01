from typing import Optional
from pydantic import Field

from ..ResultsModels.SharedResultsModel import SharedResultsModel
from ..ResultsModels.RepositoryMetadataModel import RepositoryMetadataModel


class NewResultsRepositoriesModel(SharedResultsModel):
    """A result found in a Private Cloud Hub repository, in the new result webhook."""
    __positional_fields__ = ('repository_id', 'id', 'title', 'introduction', 'matched_words', 'scan_id', 'metadata')

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
