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
from pydantic import BaseModel, Field


class CopyleaksWritingAssistantCorrectionRangesModel(BaseModel):
    """
    Corrections as parallel arrays, one entry per correction. A missing array is an empty list.
    """

    types: List[int] = Field(
        default_factory=list,
        description="Correction type ids. See `WritingAssistantClient.get_correction_types`.",
        alias="types"
    )

    starts: List[int] = Field(
        default_factory=list,
        description="Start positions of the corrected segments.",
        alias="starts"
    )

    lengths: List[int] = Field(
        default_factory=list,
        description="Lengths of the corrected segments.",
        alias="lengths"
    )

    operation_texts: List[str] = Field(
        default_factory=list,
        description="Suggested replacement text for each corrected segment.",
        alias="operationTexts",
        serialization_alias="operationTexts"
    )
