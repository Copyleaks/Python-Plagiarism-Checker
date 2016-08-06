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

class ProcessOptions(object):
    '''
    Additional options to your processes.
    '''
    
    def __init__(self):
        #default settings - undefined
        self.setHttpCallback(None)
        self.setCustomFields(None)
        self.setEmailCallback(None)
        self.setSandboxMode(None)
        self.setAllowPartialScan(None)
        
    def getHttpCallback(self):
        return self.httpCallback
    def setHttpCallback(self, value):
        '''
            Add Http callback to your requests.
        '''
        self.httpCallback = value
        
    def getCustomFields(self):
        return self.customFields
    def setCustomFields(self, value):
        '''
            Add your own custom fields to your requests. 
            You can store any kind of information which will be later available under 'CopyleaksProcess'. 
        '''
        self.customFields = value
    
    def getEmailCallback(self):
        return self.emailCallback
    def setEmailCallback(self, value):
        '''
            You can register a callback email to get informed when the request is completed. 
        '''
        self.emailCallback = value
    
    def getSandboxMode(self):
        return self.sandboxMode
    def setSandboxMode(self, value):
        '''
            Enable Sandbox mode for testing purposes
        '''
        self.sandboxMode = value

    def getAllowPartialScan(self):
        return self.allowPartialScan
    def setAllowPartialScan(self, value):
        '''
            In case of lack of credits, allow partial scan of the content.
            "value" is boolean
        '''
        self.allowPartialScan = value

    def getHeaders(self):
        headers = {}
        
        if self.getHttpCallback() != None:
            headers[Consts.HTTP_CALLBACK] = self.getHttpCallback()
        
        if self.getCustomFields() != None and len(self.getCustomFields()) > 0:
            for key, value in self.getCustomFields().items():
                headers[Consts.CLIENT_CUSTOM_PREFIX + key] = value 

        if self.getEmailCallback() != None:
            headers[Consts.EMAIL_CALLBACK] = self.getEmailCallback()
            
        if self.getSandboxMode() != None and self.getSandboxMode() == True:
            headers[Consts.SANDBOX_MODE_HEADER] = ''
        
        if self.getAllowPartialScan():
            headers[Consts.ALLOW_PARTIAL_SCAN] = 'true'
            
        return headers