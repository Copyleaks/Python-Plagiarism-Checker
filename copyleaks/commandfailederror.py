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
try:
    from consts import Consts
except:
    from copyleaks.consts import Consts

class CommandFailedError(Exception):
    '''
    classdocs
    '''


    def __init__(self, response):
        '''
        Constructor
        '''        
        self.copyleaksErrorCode = CommandFailedError.__parseCopyleaksErrorCode(response)
        self.copyleaksErrorMessage = CommandFailedError.__parseCopyleaksErrorMessage(response, self.copyleaksErrorCode)
        self.httpStatusCode = response.status_code

        super(CommandFailedError, self).__init__(self.copyleaksErrorMessage)
    
    def getErrorCode(self):
        return self.httpStatusCode
    
    @staticmethod
    def __parseCopyleaksErrorCode(response):
        if response.headers.get(Consts.COPYLEAKS_ERROR_HEADER) != None:
            return int(response.headers[Consts.COPYLEAKS_ERROR_HEADER])
        else:
            return Consts.UNDEFINED_COPYLEAKS_HEADER_ERROR_CODE
        
    @staticmethod
    def __parseCopyleaksErrorMessage(response, copyleaksErrorCode):
        if copyleaksErrorCode == Consts.UNDEFINED_COPYLEAKS_HEADER_ERROR_CODE:
            return "The application has encountered an unknown error. Please try again later."
        else:
            return response.json()['Message']