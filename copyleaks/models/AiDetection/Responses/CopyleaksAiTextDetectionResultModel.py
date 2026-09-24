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
from pydantic import BaseModel, Field, field_validator

from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionMatchModel import CopyleaksAiTextDetectionMatchModel


class CopyleaksAiTextDetectionResultModel(BaseModel):
    """
    A classified section of the scanned text.
    """

    classification: Optional[int] = Field(
        default=None,
        description="Classification of the section: 1 = human-written text, 2 = AI-generated text. None when missing.",
        alias="classification"
    )

    probability: Optional[float] = Field(
        default=None,
        description="Confidence of the classification. Deprecated by the server and may be missing.",
        alias="probability"
    )

    matches: List[CopyleaksAiTextDetectionMatchModel] = Field(
        default_factory=list,
        description="Locations of the section in the scanned document.",
        alias="matches"
    )

    @field_validator('matches', mode='before')
    @classmethod
    def matches_none_to_empty(cls, v):
        """Treat a null `matches` as an empty list."""
        return [] if v is None else v
