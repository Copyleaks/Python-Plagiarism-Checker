import json
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict
from copyleaks.models.TextModeration.Responses.Submodules.ModerationsModel import ModerationsModel
from copyleaks.models.TextModeration.Responses.Submodules.TextModerationScannedDocument import TextModerationScannedDocument
from copyleaks.models.TextModeration.Responses.Submodules.TextModerationsLegend import TextModerationsLegend

class CopyleaksTextModerationResponseModel(BaseModel):
    """Result of Text Moderation."""

    model_config = ConfigDict(extra="ignore", protected_namespaces=())

    modelVersion: Optional[str] = None

    moderations: ModerationsModel

    # Labels referenced by index in `moderations.text.chars.labels`.
    legend: Optional[List['TextModerationsLegend']] = None

    scannedDocument: TextModerationScannedDocument

