from pydantic import BaseModel

class TextModerationsLegend(BaseModel):

    """A label of the legend: its `index` in `chars.labels`, and its `id`, see `CopyleaksTextModerationConstants`."""
    index: int

    id: str
