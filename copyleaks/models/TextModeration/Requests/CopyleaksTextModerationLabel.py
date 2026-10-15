from pydantic import BaseModel, Field, field_validator


class CopyleaksTextModerationLabel(BaseModel):
    """A moderation category (label) to check. See `CopyleaksTextModerationConstants`."""

    id: str = Field(
        ...,
        description="The label id, for example \"toxic-v1\". 1 to 32 characters.",
        min_length=1,
        max_length=32
    )
