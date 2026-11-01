from typing import Optional
from pydantic import Field

from copyleaks.models.submit.Webhooks.HelperModels.BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel


class MetadataModel(CopyleaksWebhookBaseModel):
    final_url: Optional[str] = Field(
        default=None,
        description="The submitted URL after all HTTP redirects.",
        alias="finalUrl"
    )

    canonical_url: Optional[str] = Field(
        default=None,
        description="Extracted canonical URL from the scanned document.",
        alias="canonicalUrl"
    )

    publish_date: Optional[str] = Field(
        default=None,
        description="Publication date of the scanned document.",
        alias="publishDate"
    )

    creation_date: Optional[str] = Field(
        default=None,
        description="Creation date of the scanned document.",
        alias="creationDate"
    )

    last_modification_date: Optional[str] = Field(
        default=None,
        description="Last modification date of the scanned document.",
        alias="lastModificationDate"
    )

    author: Optional[str] = Field(
        default=None,
        description="Scanned document author.",
        alias="author"
    )

    organization: Optional[str] = Field(
        default=None,
        description="Scanned document organization.",
        alias="organization"
    )

    filename: Optional[str] = Field(
        default=None,
        description="Scanned document filename.",
        alias="filename"
    )
