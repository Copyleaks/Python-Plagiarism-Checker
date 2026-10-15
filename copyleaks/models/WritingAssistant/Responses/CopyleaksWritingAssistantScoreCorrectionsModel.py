from typing import Optional
from pydantic import BaseModel, Field


class CopyleaksWritingAssistantScoreCorrectionsModel(BaseModel):
    """Correction counts, scores (0-100) and score weights per correction category, and the overall score."""

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
