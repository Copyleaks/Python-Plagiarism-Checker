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

import requests
import json

from copyleaksSdk.helpers.ConfigurationManager import ConfigurationManager
from copyleaksSdk.exceptions.Commandfailederror import CommandFailedError
from copyleaksSdk.models.responses.LoginResponse import LoginResponse
from copyleaksSdk.helpers.RequestHelper import RequestHelper

class CopyleaksIdentityApi:
    '''
    Connect to Copyleaks identity server, get your token and perform readonly operations
    '''
    def __init__(self, certificate=None):
        self.copyleaks_identity_server = ConfigurationManager.instance().configuration['idEndPoint']
        self.api_version = ConfigurationManager.instance().configuration['apiVersion']
        self.timeout = ConfigurationManager.instance().configuration['requestsTimeout']
        self.certificate = certificate

    '''
    Login to Copyleaks API and get your access token using your email and api key
    '''
    def login(self, email, api_key):
        '''
        Login to Copyleaks API
        '''
        assert email and api_key
        url = f"{self.copyleaks_identity_server}{self.api_version}/account/login/api"
        payload = {
            "email": email,
            "key": api_key
        }
        headers = {
         'Content-Type' :'application/json'
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=self.timeout, cert=self.certificate)
        json_response = RequestHelper.extract_json_from_response(response)
        return LoginResponse(json_response)

    def __readonly_token(self, token, scan_id, request_method):
        url = f"{self.copyleaks_identity_server}{self.api_version}/account/permissions/{scan_id}/readonly"
        headers = RequestHelper.get_authentication_header(token)
        response = request_method(url, headers=headers, cert=self.certificate)
        return RequestHelper.extract_string_from_response(response)
    
    def get_read_only_key(self, token, scan_id):
        '''
        Get an existing readonly key for scan
        '''
        return self.__readonly_token(token, scan_id, requests.get)

    def regenerate_readonly_key(self, token, scan_id):
        '''
        Get or create a readonly key for scan
        '''
        return self.__readonly_token(token, scan_id, requests.post)

    def delete_readonly_key(self, token, scan_id):
        '''
        Delete a readonly key for scan
        '''
        return self.__readonly_token(token, scan_id, requests.delete)
    
