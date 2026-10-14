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
from pydantic import ConfigDict, Field, field_validator

from copyleaks.helpers.copyleaks_dict_access_mixin import CopyleaksDictAccessMixin


class CopyleaksAllowedCrossLanguagesResponseModel(CopyleaksDictAccessMixin):
    """
    The languages supported by cross-language plagiarism detection, as ISO-639-1 codes.
    This is the response of `Copyleaks.allowed_cross_languages`.
    """

    model_config = ConfigDict(populate_by_name=True)

    document_languages: List[str] = Field(
        default_factory=list,
        description="Languages that the scanned document can be in.",
        alias="documentLanguages"
    )

    result_languages: List[str] = Field(
        default_factory=list,
        description="Languages that you can scan the document against (`Scanning.set_cross_languages`).",
        alias="resultLanguages"
    )

    @field_validator('document_languages', 'result_languages', mode='before')
    @classmethod
    def none_to_empty(cls, v):
        return [] if v is None else v
