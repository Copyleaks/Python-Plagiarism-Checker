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
from pydantic import BaseModel, ConfigDict, Field, field_validator

from copyleaks.models.ImagePlagiarism.Responses.CopyleaksImagePlagiarismWebPageModel import CopyleaksImagePlagiarismWebPageModel


class CopyleaksImagePlagiarismInternetMatchModel(BaseModel):
    """
    A matching image found on the web.
    """

    model_config = ConfigDict(populate_by_name=True)

    url: Optional[str] = Field(
        default=None,
        description="The URL of the matching image.",
        alias="url"
    )

    match_type: Optional[int] = Field(
        default=None,
        description="0 = full match (exact or near-exact copy), 1 = partial match (cropped, resized or otherwise modified). "
                    "See `CopyleaksImagePlagiarismMatchTypes`.",
        alias="matchType"
    )

    web_pages: List[CopyleaksImagePlagiarismWebPageModel] = Field(
        default_factory=list,
        description="The web pages where the image was found. Empty when the image was not located on any page.",
        alias="webPages"
    )

    @field_validator('web_pages', mode='before')
    @classmethod
    def none_to_empty(cls, v):
        return [] if v is None else v
