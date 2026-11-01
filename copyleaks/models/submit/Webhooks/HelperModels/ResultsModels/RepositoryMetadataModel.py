from typing import Optional
from pydantic import Field

from ..BaseModels.MetadataModel import MetadataModel


class RepositoryMetadataModel(MetadataModel):
    __positional_fields__ = ('submitted_by',)

    submitted_by: Optional[str] = Field(
        default=None,
        description="Email of the user which added this document to the repository.",
        alias="submittedBy"
    )
