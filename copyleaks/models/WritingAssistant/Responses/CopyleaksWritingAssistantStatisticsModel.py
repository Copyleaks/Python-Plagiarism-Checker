from typing import Optional
from pydantic import BaseModel, Field


class CopyleaksWritingAssistantStatisticsModel(BaseModel):
    """Statistics of the text."""

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
