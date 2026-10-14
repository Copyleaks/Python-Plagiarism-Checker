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


class CopyleaksSupportedAiTextDetectionFileTypesResponseModel(CopyleaksDictAccessMixin):
    """
    The file types supported by AI Text Detection, for example "pdf" and "docx".
    This is the response of `Copyleaks.supported_ai_text_detection_file_types`.
    """

    model_config = ConfigDict(populate_by_name=True)

    supported_ai_file_types: List[str] = Field(
        default_factory=list,
        description="The supported file extensions, without the dot.",
        alias="supportedAiFileTypes"
    )

    @field_validator('supported_ai_file_types', mode='before')
    @classmethod
    def none_to_empty(cls, v):
        return [] if v is None else v
