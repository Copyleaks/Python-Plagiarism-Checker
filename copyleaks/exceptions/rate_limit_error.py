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

from copyleaks.exceptions.command_error import CommandError, _describe_response


def _parse_retry_after(response):
    """The `Retry-After` header in seconds, or None when it is missing or is not a number of seconds."""
    headers = getattr(response, 'headers', None)
    if not headers:
        return None
    try:
        value = headers.get('Retry-After')
    except Exception:
        return None
    if value is None:
        return None
    try:
        seconds = float(str(value).strip())
    except ValueError:
        return None
    return seconds if seconds >= 0 else None


class RateLimitError(CommandError):
    """
    Too many requests (HTTP 429). Wait before calling again.
    `get_response()` returns the `requests.Response` and `retry_after` is the server's `Retry-After`
    value in seconds, when the server sent one.
    It is a `CommandError`, so code that catches `CommandError` also catches it.
    """

    def __init__(self, response=None):
        super().__init__(response)

    @property
    def retry_after(self):
        """Seconds to wait before retrying, from the `Retry-After` response header, or None."""
        return _parse_retry_after(self.get_response())

    def __str__(self):
        response = self.get_response()
        return _describe_response(response) if response is not None else 'Too many requests'
