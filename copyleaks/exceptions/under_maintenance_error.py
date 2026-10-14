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

from copyleaks.exceptions.command_error import _describe_response
from copyleaks.exceptions.rate_limit_error import _parse_retry_after


class UnderMaintenanceError(Exception):
    """
    Copyleaks servers are unavailable for maintenance (HTTP 503). Retry later with exponential backoff.
    `get_response()` returns the `requests.Response` and `retry_after` is the server's `Retry-After`
    value in seconds, when the server sent one.
    """

    def __init__(self, response=None):
        super().__init__(*(() if response is None else (response,)))
        self._response = response

    def get_response(self):
        return self._response

    @property
    def status_code(self):
        return getattr(self._response, 'status_code', None)

    @property
    def retry_after(self):
        """Seconds to wait before retrying, from the `Retry-After` response header, or None."""
        return _parse_retry_after(self._response)

    def __str__(self):
        return _describe_response(self._response) if self._response is not None else 'Under maintenance'
