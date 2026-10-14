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


def _describe_response(response):
    """A short `HTTP <status>: <body>` text for an error response. Never includes request headers."""
    status = getattr(response, 'status_code', None)
    if status is None:
        if isinstance(response, (bytes, bytearray)):
            return response.decode('utf-8', 'replace')[:500]
        return '' if response is None else str(response)[:500]
    try:
        body = (response.text or '').strip()
    except Exception:
        body = ''
    return f"HTTP {status}: {body[:500]}" if body else f"HTTP {status}"


class CommandError(Exception):
    """
    The server rejected the request.
    `get_response()` returns the `requests.Response`, with its status code, headers and body.
    """

    def __init__(self, response):
        super().__init__(response)
        self.__set_response(response)

    def get_response(self):
        return self.__x

    def __set_response(self, x):
        self.__x = x

    @property
    def status_code(self):
        """The HTTP status code of the response, or None."""
        return getattr(self.__x, 'status_code', None)

    def __str__(self):
        return _describe_response(self.__x)
