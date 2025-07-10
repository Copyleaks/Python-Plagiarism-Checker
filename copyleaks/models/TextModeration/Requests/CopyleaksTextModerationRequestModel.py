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

import json
from typing import List, Optional, Any
from pydantic import BaseModel, Field, field_validator

class CopyleaksTextModerationRequestModel(BaseModel):

    """The input text to be moderated."""
    text: str 

    """Whether to run the moderation in sandbox (test) mode."""
    sandbox: bool = False  

    """The language code of the input text (e.g., "en" for English). If None, auto-detect."""
    language: Optional[str] = None  

    """A list of label objects specifying which moderation categories to check."""
    labels: Optional[List[Any]] = None  
     
    @field_validator('text')
    @classmethod
    def text_must_not_be_empty(cls, v):
        if not isinstance(v, str) or not v.strip():
            raise ValueError('text is required and must be a non-empty string')
        return v

    @field_validator('labels')
    @classmethod
    def labels_length(cls, v):
        if not isinstance(v, list) or not v:
            raise ValueError('labels must be a non-empty list')
        if not (1 <= len(v) <= 32):
            raise ValueError('labels must contain at least 1 and no more than 32 elements')
        return v
