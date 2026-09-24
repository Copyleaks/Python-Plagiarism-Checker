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

from typing import List
from pydantic import BaseModel, Field, field_validator


class CopyleaksAiTextDetectionPatternStatisticsModel(BaseModel):
    """
    Statistics of the AI patterns found in the text. The arrays are parallel, one entry per pattern.
    A missing or null array is an empty list.
    """

    ai_count: List[float] = Field(
        default_factory=list,
        description="How often each pattern appears in AI-generated text.",
        alias="aiCount",
        serialization_alias="aiCount"
    )

    human_count: List[float] = Field(
        default_factory=list,
        description="How often each pattern appears in human-written text.",
        alias="humanCount",
        serialization_alias="humanCount"
    )

    proportion: List[float] = Field(
        default_factory=list,
        description="Ratio between the AI and the human frequency of each pattern.",
        alias="proportion"
    )

    source: List[int] = Field(
        default_factory=list,
        description="Source of each pattern: 1 = AI, 2 = humanizer.",
        alias="source"
    )

    @field_validator('ai_count', 'human_count', 'proportion', 'source', mode='before')
    @classmethod
    def statistics_none_to_empty(cls, v):
        """Treat a null statistics array as an empty list."""
        return [] if v is None else v
