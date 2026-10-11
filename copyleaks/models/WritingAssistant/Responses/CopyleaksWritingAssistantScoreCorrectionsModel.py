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


class CopyleaksWritingAssistantScoreCorrectionsModel(BaseModel):
    """
    Correction counts, scores (0-100) and score weights per correction category, and the overall score.
    """

    grammar_corrections_count: Optional[int] = Field(
        default=None,
        description="Number of grammar corrections.",
        alias="grammarCorrectionsCount",
        serialization_alias="grammarCorrectionsCount"
    )

    grammar_corrections_score: Optional[int] = Field(
        default=None,
        description="Grammar score.",
        alias="grammarCorrectionsScore",
        serialization_alias="grammarCorrectionsScore"
    )

    grammar_score_weight: Optional[float] = Field(
        default=None,
        description="Weight of the grammar score in the overall score.",
        alias="grammarScoreWeight",
        serialization_alias="grammarScoreWeight"
    )

    mechanics_corrections_count: Optional[int] = Field(
        default=None,
        description="Number of mechanics corrections.",
        alias="mechanicsCorrectionsCount",
        serialization_alias="mechanicsCorrectionsCount"
    )

    mechanics_corrections_score: Optional[int] = Field(
        default=None,
        description="Mechanics score.",
        alias="mechanicsCorrectionsScore",
        serialization_alias="mechanicsCorrectionsScore"
    )

    mechanics_score_weight: Optional[float] = Field(
        default=None,
        description="Weight of the mechanics score in the overall score.",
        alias="mechanicsScoreWeight",
        serialization_alias="mechanicsScoreWeight"
    )

    sentence_structure_corrections_count: Optional[int] = Field(
        default=None,
        description="Number of sentence structure corrections.",
        alias="sentenceStructureCorrectionsCount",
        serialization_alias="sentenceStructureCorrectionsCount"
    )

    sentence_structure_corrections_score: Optional[int] = Field(
        default=None,
        description="Sentence structure score.",
        alias="sentenceStructureCorrectionsScore",
        serialization_alias="sentenceStructureCorrectionsScore"
    )

    sentence_structure_score_weight: Optional[float] = Field(
        default=None,
        description="Weight of the sentence structure score in the overall score.",
        alias="sentenceStructureScoreWeight",
        serialization_alias="sentenceStructureScoreWeight"
    )

    word_choice_corrections_count: Optional[int] = Field(
        default=None,
        description="Number of word choice corrections.",
        alias="wordChoiceCorrectionsCount",
        serialization_alias="wordChoiceCorrectionsCount"
    )

    word_choice_corrections_score: Optional[int] = Field(
        default=None,
        description="Word choice score.",
        alias="wordChoiceCorrectionsScore",
        serialization_alias="wordChoiceCorrectionsScore"
    )

    word_choice_score_weight: Optional[float] = Field(
        default=None,
        description="Weight of the word choice score in the overall score.",
        alias="wordChoiceScoreWeight",
        serialization_alias="wordChoiceScoreWeight"
    )

    overall_score: Optional[int] = Field(
        default=None,
        description="Overall writing score.",
        alias="overallScore",
        serialization_alias="overallScore"
    )
