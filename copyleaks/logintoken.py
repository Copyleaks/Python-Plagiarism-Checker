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

from dateutil import parser
from datetime import datetime
try:
    from consts import Consts
    from commandfailederror import CommandFailedError
except:
    from copyleaks.consts import Consts
    from copyleaks.commandfailederror import CommandFailedError

class LoginToken(object):
    '''
    classdocs
    '''


    def __init__(self, email, apiKey):
        '''
        Constructor
        '''
        assert email and apiKey
                
        self.Email = email
        self.ApiKey = apiKey 
        
    
    def getAccessToken(self):
        return self.AccessToken
    def __setAccessToken(self, value):
        self.AccessToken = value
    
    def getIssuedTime(self):
        return self.IssuedTime
    def __setIssuedTime(self, value):
        self.IssuedTime = value
        
    def getExpiresTime(self):
        return self.ExpiresTime
    def __setExpiresTime(self, value):
        self.ExpiresTime = value
    
    def login(self):
        '''
            Login to Copyleaks authentication server.
        '''
        url = "%s%s/account/login-api" % (Consts.SERVICE_ENTRY_POINT, Consts.SERVICE_VERSION)
        payload = {
            'email': self.Email, 
            'apikey': self.ApiKey
        }
        headers = {
            Consts.CONTENT_TYPE_HEADER: Consts.CONTENT_TYPE_JSON
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if (response.status_code == Consts.HTTP_SUCCESS):
            self.__setAccessToken(response.json()['access_token'])
            self.__setIssuedTime(parser.parse(response.json()['.issued']).replace(tzinfo=None))
            self.__setExpiresTime(parser.parse(response.json()['.expires']).replace(tzinfo=None))
        else:
            raise CommandFailedError(response) 
    
    def generateAuthrizationHeader(self):
        
        if datetime.utcnow() <= self.getExpiresTime(): # If token expired, renew it.
            self.login()
        
        return "Bearer %s" % (self.getAccessToken())
    