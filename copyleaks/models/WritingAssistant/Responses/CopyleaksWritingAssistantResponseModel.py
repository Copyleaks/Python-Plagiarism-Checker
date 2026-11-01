from typing import Optional
from pydantic import BaseModel, Field

from copyleaks.helpers.copyleaks_dict_access_mixin import CopyleaksDictAccessMixin
from copyleaks.models.WritingAssistant.Responses.CopyleaksWritingAssistantCorrectionsModel import CopyleaksWritingAssistantCorrectionsModel
from copyleaks.models.WritingAssistant.Responses.CopyleaksWritingAssistantScannedDocumentModel import CopyleaksWritingAssistantScannedDocumentModel
from copyleaks.models.WritingAssistant.Responses.CopyleaksWritingAssistantScoreModel import CopyleaksWritingAssistantScoreModel


class CopyleaksWritingAssistantResponseModel(CopyleaksDictAccessMixin, BaseModel):
    """
    Result of the Writing Assistant (Grammar Checker). Unknown fields are ignored and missing ones are None.
    `model_dump(by_alias=True)` gives the camelCase keys.
    """

    score: Optional[CopyleaksWritingAssistantScoreModel] = Field(
        default=None,
        description="Writing quality scores, readability and text statistics.",
        alias="score"
    )

    corrections: Optional[CopyleaksWritingAssistantCorrectionsModel] = Field(
        default=None,
        description="Suggested corrections to the text.",
        alias="corrections"
    )

    scanned_document: Optional[CopyleaksWritingAssistantScannedDocumentModel] = Field(
        default=None,
        description="General information about the scanned document.",
        alias="scannedDocument",
        serialization_alias="scannedDocument"
    )

    scan_type: Optional[str] = Field(
        default=None,
        description="\"sandbox\" for sandbox scans. Not sent for regular scans.",
        alias="scanType",
        serialization_alias="scanType"
    )
