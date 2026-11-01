from typing import Dict, List
from pydantic import ConfigDict, Field, field_validator

from copyleaks.helpers.copyleaks_dict_access_mixin import CopyleaksDictAccessMixin


def _to_language_map(value):
    """The API returns {language name: ISO-639-1 code}; null is read as {}."""
    return {} if value is None else value


class CopyleaksAllowedCrossLanguagesResponseModel(CopyleaksDictAccessMixin):
    """
    Languages supported by cross-language plagiarism detection. `document_languages` and `result_languages` map
    language names to ISO-639-1 codes, e.g. {"english": "en"}; the `*_language_codes` properties list the codes.
    """

    model_config = ConfigDict(populate_by_name=True)

    document_languages: Dict[str, str] = Field(
        default_factory=dict,
        description="Languages that the scanned document can be in: language name to ISO-639-1 code.",
        alias="documentLanguages"
    )

    result_languages: Dict[str, str] = Field(
        default_factory=dict,
        description="Languages that you can scan the document against (`Scanning.set_cross_languages`): "
                    "language name to ISO-639-1 code.",
        alias="resultLanguages"
    )

    @field_validator('document_languages', 'result_languages', mode='before')
    @classmethod
    def to_language_map(cls, v):
        return _to_language_map(v)

    @property
    def document_language_codes(self) -> List[str]:
        """The ISO-639-1 codes of `document_languages`."""
        return list(self.document_languages.values())

    @property
    def result_language_codes(self) -> List[str]:
        """The ISO-639-1 codes of `result_languages`, to use with `Language.set_code`."""
        return list(self.result_languages.values())
