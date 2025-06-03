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

class AlertsModel(BaseModel):
    """
    Represents a single alert notification detail.
    """
    _category: Optional[str] = None
    _code: Optional[str] = None
    _title: Optional[str] = None
    _message: Optional[str] = None
    _help_link: Optional[str] = None
    _severity: Optional[str] = None
    _additional_data: Optional[str] = None

    def __init__(self,
                 category: Optional[str] = None,
                 code: Optional[str] = None,
                 title: Optional[str] = None,
                 message: Optional[str] = None,
                 help_link: Optional[str] = None,
                 severity: Optional[str] = None,
                 additional_data: Optional[str] = None):
        """
        Initializes an Alerts object, storing values in internal attributes.
        """
        super().__init__(category=category, code=code, title=title, message=message,
                         help_link=help_link, severity=severity, additional_data=additional_data)
        self._category = category
        self._code = code
        self._title = title
        self._message = message
        self._help_link = help_link
        self._severity = severity
        self._additional_data = additional_data
