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

from typing import Optional
from pydantic import BaseModel, Field


class CopyleaksWritingAssistantStatisticsModel(BaseModel):
    """
    Statistics of the text.
    """

    sentence_count: Optional[int] = Field(
        default=None,
        description="Number of sentences.",
        alias="sentenceCount",
        serialization_alias="sentenceCount"
    )

    average_sentence_length: Optional[float] = Field(
        default=None,
        description="Average sentence length, in words.",
        alias="averageSentenceLength",
        serialization_alias="averageSentenceLength"
    )

    average_word_length: Optional[float] = Field(
        default=None,
        description="Average word length, in characters.",
        alias="averageWordLength",
        serialization_alias="averageWordLength"
    )

    reading_time_seconds: Optional[float] = Field(
        default=None,
        description="Estimated reading time, in seconds.",
        alias="readingTimeSeconds",
        serialization_alias="readingTimeSeconds"
    )

    speaking_time_seconds: Optional[float] = Field(
        default=None,
        description="Estimated speaking time, in seconds.",
        alias="speakingTimeSeconds",
        serialization_alias="speakingTimeSeconds"
    )
