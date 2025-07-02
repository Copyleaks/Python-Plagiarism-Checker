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
from ..BaseModels.MetadataModel import MetadataModel 
from typing import Optional, List
from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

class ScannedDocumentModel(BaseModel):
    
    """The unique scan id provided by you."""
    _scan_id: Optional[str] = None

    """Total number of words found in the scanned text."""
    _total_words: Optional[int] = None

    """Number of excluded words in the submitted content."""
    _total_excluded: Optional[int] = None

    """Overall credits used for the scan."""
    _credits: Optional[int] = None

    """The creation time of the scan."""
    _creation_time: Optional[str] = None

    """Metadata object"""
    _metadata: Optional['MetadataModel'] = None

    def __init__(self,
                 scan_id: Optional[str] = None,
                 total_words: Optional[int] = None,
                 total_excluded: Optional[int] = None,
                 credits: Optional[int] = None,
                 creation_time: Optional[str] = None,
                 metadata: Optional['MetadataModel'] = None):
        """
        Initializes a ScannedDocument object.
        """
        super().__init__(scan_id=scan_id, total_words=total_words, total_excluded=total_excluded,
                         credits=credits, creation_time=creation_time, metadata=metadata)
        self._scan_id = scan_id
        self._total_words = total_words
        self._total_excluded = total_excluded
        self._credits = credits
        self._creation_time = creation_time
        self._metadata = metadata
