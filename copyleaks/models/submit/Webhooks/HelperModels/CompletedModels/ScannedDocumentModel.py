from typing import Optional
from pydantic import Field

from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel
from ..BaseModels.MetadataModel import MetadataModel


class ScannedDocumentModel(CopyleaksWebhookBaseModel):
    """General information about the scanned document."""
    __positional_fields__ = ('scan_id', 'total_words', 'total_excluded', 'credits', 'creation_time', 'metadata')

    scan_id: Optional[str] = Field(
        default=None,
        description="The unique scan id provided by you.",
        alias="scanId"
    )

    total_words: Optional[int] = Field(
        default=None,
        description="Total number of words found in the scanned text.",
        alias="totalWords"
    )

    total_excluded: Optional[int] = Field(
        default=None,
        description="Number of excluded words in the submitted content.",
        alias="totalExcluded"
    )

    credits: Optional[int] = Field(
        default=None,
        description="Overall credits used for the scan.",
        alias="credits"
    )

    creation_time: Optional[str] = Field(
        default=None,
        description="The creation time of the scan (UTC).",
        alias="creationTime"
    )

    metadata: Optional[MetadataModel] = Field(
        default=None,
        description="Metadata of the scanned document.",
        alias="metadata"
    )
