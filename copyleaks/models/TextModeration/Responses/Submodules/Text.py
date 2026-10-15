from typing import  Optional
from pydantic import BaseModel

from copyleaks.models.TextModeration.Responses.Submodules.TextModerationChars import TextModerationChars

class Text(BaseModel):
    """Labelled segments, as parallel arrays in `chars`."""
    chars: Optional['TextModerationChars'] 
