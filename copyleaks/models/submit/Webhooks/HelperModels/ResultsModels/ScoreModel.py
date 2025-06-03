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
from pydantic import BaseModel

class ScoreModel(BaseModel):
    """
    Represents scoring details, including word counts and an aggregated score.
    """
    _identical_words: Optional[int] = None
    _minor_changed_words: Optional[int] = None
    _related_meaning_words: Optional[int] = None
    _aggregated_score: Optional[float] = None

    def __init__(self,
                 identical_words: Optional[int] = None,      
                 minor_changed_words: Optional[int] = None,  
                 related_meaning_words: Optional[int] = None, 
                 aggregated_score: Optional[float] = None):   
        """
        Initializes a Score object, storing values in internal attributes.
        """
        super().__init__(identical_words=identical_words, minor_changed_words=minor_changed_words,
                         related_meaning_words=related_meaning_words, aggregated_score=aggregated_score)
        self._identical_words = identical_words
        self._minor_changed_words = minor_changed_words
        self._related_meaning_words = related_meaning_words
        self._aggregated_score = aggregated_score
