from typing import List, Optional
from pydantic import AliasChoices, BaseModel, Field, field_validator


class CopyleaksAiTextDetectionPositionsModel(BaseModel):
    """
    Positions of matched segments, as parallel arrays of start positions and lengths. A null array is empty.
    Accepts the PascalCase `Starts`/`Lengths` keys of sandbox scans too.
    """

    starts: List[int] = Field(
        default_factory=list,
        description="Start positions of the matched segments.",
        alias="starts",
        validation_alias=AliasChoices("starts", "Starts")
    )

    lengths: List[int] = Field(
        default_factory=list,
        description="Lengths of the matched segments, one per start position.",
        alias="lengths",
        validation_alias=AliasChoices("lengths", "Lengths")
    )

    group_ids: Optional[List[int]] = Field(
        default=None,
        description="HTML group ids of the matched segments. Present only for HTML positions.",
        alias="groupIds",
        serialization_alias="groupIds"
    )

    @field_validator('starts', 'lengths', mode='before')
    @classmethod
    def positions_none_to_empty(cls, v):
        return [] if v is None else v
