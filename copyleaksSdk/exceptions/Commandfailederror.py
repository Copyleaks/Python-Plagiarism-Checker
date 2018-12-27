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
class CommandFailedError(Exception):
    '''
    An exception for a failed HTTP call to Copyleaks API.
    The exception includes the Copyleaks error code and the error message
    A detailed list of Copyleaks error codes can be found at: https://api.copyleaks.com/documentation/errors
    '''
    def __init__(self, response):
        self.copyleaksErrorCode, self.copyleaksErrorMessage = CommandFailedError.__get_message(response)
        self.httpStatusCode = response.status_code
        super(CommandFailedError, self).__init__(self.copyleaksErrorMessage)
        
    @staticmethod
    def __get_message(response):
        response_json = response.json()
        return response_json['CopyleaksErrorCode'], response['Message']
