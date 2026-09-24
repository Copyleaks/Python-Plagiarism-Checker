'''
 The MIT License(MIT)

 Copyright(c) 2016 Copyleaks LTD (https://copyleaks.com)

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
'''

from typing import List, Optional
from pydantic import AliasChoices, BaseModel, Field, field_validator


class CopyleaksAiTextDetectionPositionsModel(BaseModel):
    """
    Positions of matched segments, as parallel arrays of start positions and lengths.
    Accepts the camelCase keys and the PascalCase `Starts`/`Lengths` keys sent by sandbox scans.
    A missing or null `starts`/`lengths` is an empty list.
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
        """Treat a null `starts`/`lengths` as an empty list."""
        return [] if v is None else v
