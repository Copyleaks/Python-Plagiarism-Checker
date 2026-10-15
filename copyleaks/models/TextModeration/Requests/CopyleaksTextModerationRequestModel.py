from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from copyleaks.models.TextModeration.Requests.CopyleaksTextModerationLabel import CopyleaksTextModerationLabel

MAX_TEXT_MODERATION_LABELS = 16


class CopyleaksTextModerationRequestModel(BaseModel):
    """Request of Text Moderation. `text` and `labels` are required."""

    text: str = Field(
        ...,
        description="The input text to be moderated. 1 to 25000 characters."
    )

    sandbox: bool = Field(
        default=False,
        description="Whether to run the moderation in sandbox (test) mode."
    )

    language: Optional[str] = Field(
        default=None,
        description="The language code of the input text (e.g., \"en\" for English). If None, auto-detect."
    )

    labels: List[CopyleaksTextModerationLabel] = Field(
        ...,
        description="The moderation categories to check: 1 to 16 labels. A dict such as {\"id\": \"toxic-v1\"} is accepted."
    )

    @field_validator('text')
    @classmethod
    def text_must_not_be_empty(cls, v):
        if not isinstance(v, str) or not v.strip():
            raise ValueError('text is required and must be a non-empty string')
        return v

    @field_validator('labels', mode='before')
    @classmethod
    def labels_length(cls, v):
        if not isinstance(v, (list, tuple)) or not v:
            raise ValueError('labels must be a non-empty list')
        if len(v) > MAX_TEXT_MODERATION_LABELS:
            raise ValueError(f'labels must contain at least 1 and no more than {MAX_TEXT_MODERATION_LABELS} elements')
        return v
