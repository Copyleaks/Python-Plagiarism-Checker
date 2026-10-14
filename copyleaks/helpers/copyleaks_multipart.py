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

import mimetypes


class CopyleaksMultipart:
    """Helpers to build multipart/form-data requests with `requests`."""

    @staticmethod
    def bool_field(value):
        """A boolean form field value: "true" or "false"."""
        return 'true' if value else 'false'

    @staticmethod
    def file_part(filename, content):
        """
        The `files=` entry of an uploaded file: (filename, content, content type).
        `content` is bytes or a file object opened in binary mode, which is read when the request body is built.
        """
        if isinstance(content, (bytearray, memoryview)):
            content = bytes(content)
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        return (filename, content, content_type)
