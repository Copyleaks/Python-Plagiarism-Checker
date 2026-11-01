from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


def validate_headers(value):
    """Headers are a list of [name, value] pairs."""
    if value is None:
        return None
    if not isinstance(value, (list, tuple)):
        raise ValueError('headers must be a list of [name, value] pairs')
    pairs = []
    for pair in value:
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError('each header must be a [name, value] pair')
        pairs.append([pair[0], pair[1]])
    return pairs


class CopyleaksDetectionWebhooksModel(BaseModel):
    """Where Copyleaks sends the result of an asynchronous AI Image or AI Video Detection."""

    model_config = ConfigDict(populate_by_name=True)

    url: str = Field(
        ...,
        description="The URL that Copyleaks will POST the detection result to.",
        alias="url"
    )

    headers: Optional[List[List[str]]] = Field(
        default=None,
        description="Custom headers for the webhook request, as [name, value] pairs.",
        alias="headers"
    )

    @field_validator('url')
    @classmethod
    def validate_url(cls, v):
        if not v or not v.strip():
            raise ValueError('webhooks url is required')
        return v

    @field_validator('headers', mode='before')
    @classmethod
    def validate_headers(cls, v):
        return validate_headers(v)
