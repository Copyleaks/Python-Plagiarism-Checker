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

class MetadataModel(BaseModel):
    final_url: Optional[str] = None
    """The submitted URL after all HTTP redirects."""
    
    canonical_url: Optional[str] = None
    """Extracted canonical URL from the scanned document."""
    
    publish_date: Optional[str] = None
    """Publication date of the scanned document."""
    
    creation_date: Optional[str] = None
    """Creation date of the scanned document."""
    
    last_modification_date: Optional[str] = None
    """Last modification date of the scanned document."""
    
    author: Optional[str] = None
    """Scanned document author."""
    
    organization: Optional[str] = None
    """Scanned document organization."""
    
    filename: Optional[str] = None
    """Scanned document filename."""