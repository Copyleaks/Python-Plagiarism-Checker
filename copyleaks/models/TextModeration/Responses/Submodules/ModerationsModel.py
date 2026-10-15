from typing import Optional
from pydantic import BaseModel
from copyleaks.models.TextModeration.Responses.Submodules.Text import Text

class ModerationsModel(BaseModel):
    
    """Moderated segments of the submitted text, in its textual version."""
    text: Optional['Text']

