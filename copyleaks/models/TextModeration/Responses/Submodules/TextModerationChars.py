from typing import List
from pydantic import BaseModel

class TextModerationChars(BaseModel):

    """Labelled segments: `labels` (index into the legend), `starts` and `lengths`, in characters."""
    labels: List[int]
    
    starts: List[int] 
    
    lengths: List[int] 
