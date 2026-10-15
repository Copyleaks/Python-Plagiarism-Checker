from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class TextModerationScannedDocument(BaseModel):

    """General information about the scanned document."""
    scanId: str

    totalWords: Optional[int] = None

    totalExcluded: Optional[int] = None

    actualCredits: Optional[int] = None

    expectedCredits: Optional[int] = None

    creationTime: datetime
