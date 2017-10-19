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


class Consts():
    '''
        System constraints
    '''

    HTTP_SUCCESS = 200

    UNDEFINED_COPYLEAKS_HEADER_ERROR_CODE = 9999

    CONTENT_TYPE_JSON = "application/json"

    CONTENT_TYPE_MULTIPART = 'multipart/form-data'

    CONTENT_TYPE_HEADER = 'Content-Type'

    AUTHORIZATION_HEADER = 'Authorization'

    COPYLEAKS_ERROR_HEADER = 'Copyleaks-Error-Code'

    COPYLEAKS_HEADER_PREFIX = "copyleaks-"

    CLIENT_CUSTOM_PREFIX = "%sclient-custom-" % (COPYLEAKS_HEADER_PREFIX)

    EMAIL_CALLBACK = '%semail-callback' % (COPYLEAKS_HEADER_PREFIX)

    HTTP_CALLBACK = '%shttp-completion-callback' % (COPYLEAKS_HEADER_PREFIX)

    HTTP_IN_PROGRESS_RESULT_CALLBACK = '%sin-progress-new-result' % (COPYLEAKS_HEADER_PREFIX)

    SANDBOX_MODE_HEADER = '%ssandbox-mode' % (COPYLEAKS_HEADER_PREFIX)

    ALLOW_PARTIAL_SCAN = '%sallow-partial-scan' % (COPYLEAKS_HEADER_PREFIX)

    COMPARE_BETWEEN_FILES = '%scompare-documents-for-similarity' % (COPYLEAKS_HEADER_PREFIX)

    IMPORT_TO_DATABASE_ONLY_HEADER = '%sindex-only' % (COPYLEAKS_HEADER_PREFIX)

    MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB

    SERVICE_ENTRY_POINT = 'https://api.copyleaks.com/'

    SERVICE_VERSION = 'v1'

    DOWNLOADS_ENTRY_POINT = 'downloads'
