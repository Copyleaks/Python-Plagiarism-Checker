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

import json
import requests
import re
import os.path

try:
    from copyleaks.consts import Consts
    from copyleaks.commandfailederror import CommandFailedError
    from copyleaks.copyleaksprocess import CopyleaksProcess
    from copyleaks.logintoken import LoginToken
    from copyleaks.eocrlanguage import eOcrLanguage
except:
    from consts import Consts
    from commandfailederror import CommandFailedError
    from copyleaksprocess import CopyleaksProcess
    from logintoken import LoginToken
    from eocrlanguage import eOcrLanguage

class CopyleaksCloud(object):
    '''
     This class allows you to connect to Copyleaks cloud, 
     scan for plagiarism and get your Copyleaks account status. 
    '''

    def __init__(self, product, email, apiKey):
        '''
        Create a new cloud connection with login credentials
        '''
        assert product, 'Missing product!'
        
        self.login(email, apiKey)
        self.product = product

        
    def login(self, email, apiKey):
        
        assert email and apiKey
        
        self.token = LoginToken(email, apiKey)
        self.token.login()

    def getProduct(self):
        return self.product

    def getCredits(self):
        '''
            Get your current credit balance
        '''
        url = "%s%s/%s/count-credits" % (Consts.SERVICE_ENTRY_POINT, Consts.SERVICE_VERSION, self.product)
        headers = {
            Consts.AUTHORIZATION_HEADER: self.token.generateAuthrizationHeader()
        }
        response = requests.get(url, headers=headers)
        if (response.status_code == Consts.HTTP_SUCCESS):
            return int(response.json()['Amount'])
        else:
            raise CommandFailedError(response)
    
    def getProcesses(self):
        '''
            Get your active processes
        '''
        url = "%s%s/%s/list" % (Consts.SERVICE_ENTRY_POINT, Consts.SERVICE_VERSION, self.product)
        headers = {
            Consts.AUTHORIZATION_HEADER: self.token.generateAuthrizationHeader()
        }
        response = requests.get(url, headers=headers)
        if (response.status_code == Consts.HTTP_SUCCESS):
            return CopyleaksProcess.parseProcesses(self.login, response.json())
        else:
            raise CommandFailedError(response)
    
    def createByUrl(self, url, options):
        '''
            Submitting URL to plagiarism scan
        '''
        
        assert url, 'Missing URL'
        assert bool(re.match('http://|https://', url, re.I)), 'url must starts with "http://" or "https://"'
        
        serviceUrl = "%s%s/%s/create-by-url" % (Consts.SERVICE_ENTRY_POINT, Consts.SERVICE_VERSION, self.product)
        payload = {
            'url': url 
        }
        headers = {
            Consts.AUTHORIZATION_HEADER: self.token.generateAuthrizationHeader(),
            Consts.CONTENT_TYPE_HEADER: Consts.CONTENT_TYPE_JSON
        }
        
        if options != None:
            headers = headers.copy()
            headers.update(options.getHeaders())
            
        response = requests.post(serviceUrl, headers=headers, data=json.dumps(payload))
        if (response.status_code == Consts.HTTP_SUCCESS):
            return CopyleaksProcess(self.getProduct(), self.token, response.json())
        else:
            raise CommandFailedError(response) 
    
    def createByFile(self, filePath, options):
        '''
            Submitting local file to plagiarism scan
        '''
        assert filePath, 'Missing filePath'
        assert os.path.exists(filePath), 'filePath is not exists!'
        assert os.path.getsize(filePath) <= Consts.MAX_FILE_SIZE_BYTES, 'Exceed max file size (max allowed: %s bytes)' % (Consts.MAX_FILE_SIZE_BYTES)
        
        serviceUrl = "%s%s/%s/create-by-file" % (Consts.SERVICE_ENTRY_POINT, Consts.SERVICE_VERSION, self.product)

        headers = {
            Consts.AUTHORIZATION_HEADER: self.token.generateAuthrizationHeader()
        }
        
        if options != None:
            headers = headers.copy()
            headers.update(options.getHeaders())
        
        theFile = {'file': (os.path.basename(filePath), open(filePath, 'rb'))}
        response = requests.post(serviceUrl, headers=headers, files=theFile)
        if (response.status_code == Consts.HTTP_SUCCESS):
            return CopyleaksProcess(self.getProduct(), self.token, response.json())
        else:
            raise CommandFailedError(response) 

    def createByOcr(self, filePath, lang, options):
        '''
            Submitting picture, containing textual content, to plagiarism scan
        '''
        assert filePath, 'Missing filePath'
        assert os.path.exists(filePath), 'filePath is not exists!'
        assert os.path.getsize(filePath) <= Consts.MAX_FILE_SIZE_BYTES, 'Exceed max file size (max allowed: %s bytes)' % (Consts.MAX_FILE_SIZE_BYTES)
        assert lang, 'Missing lang'
        assert lang.value in eOcrLanguage.__members__ , 'Unknown language'
        
        serviceUrl = "%s%s/%s/create-by-file-ocr?language=%s" % (Consts.SERVICE_ENTRY_POINT, Consts.SERVICE_VERSION, self.product, lang.value)

        headers = {
            Consts.AUTHORIZATION_HEADER: self.token.generateAuthrizationHeader()
        }
        
        if options != None:
            headers = headers.copy()
            headers.update(options.getHeaders())
        
        theFile = {'file': (os.path.basename(filePath), open(filePath, 'rb'))}
        response = requests.post(serviceUrl, headers=headers, files=theFile)
        if (response.status_code == Consts.HTTP_SUCCESS):
            return CopyleaksProcess(self.getProduct(), self.token, response.json())
        else:
            raise CommandFailedError(response)