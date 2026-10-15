from typing import Optional
from pydantic import Field
from .HelperModels.BaseModels.StatusWebhookModel import StatusWebhookModel
from .HelperModels.CompletedModels.ScannedDocumentModel import ScannedDocumentModel


class CreditsCheckedWebhookModel(StatusWebhookModel):
    """Credits checked webhook. Parse it with `CreditsCheckedWebhookModel(**request.json)`."""
    __positional_fields__ = ('credits', 'scanned_document', 'status')

    credits: Optional[int] = Field(
        default=None,
        description="The price of the scan: the credits a full scan will use.",
        alias="credits"
    )

    scanned_document: Optional[ScannedDocumentModel] = Field(
        default=None,
        description="General information about the scanned document.",
        alias="scannedDocument"
    )
