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

from typing import Dict, List
from pydantic import ConfigDict, Field, field_validator

from copyleaks.helpers.copyleaks_dict_access_mixin import CopyleaksDictAccessMixin


def _to_language_map(value):
    """The API returns {language name: ISO-639-1 code}. A plain list of codes is accepted too ({code: code})."""
    if value is None:
        return {}
    if isinstance(value, (list, tuple)):
        return {code: code for code in value}
    return value


class CopyleaksAllowedCrossLanguagesResponseModel(CopyleaksDictAccessMixin):
    """
    The languages supported by cross-language plagiarism detection.
    This is the response of `Copyleaks.allowed_cross_languages`.

    `document_languages` and `result_languages` map each language name to its ISO-639-1 code,
    for example {"english": "en", "french": "fr"}. `document_language_codes` and `result_language_codes`
    list the codes only.
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
