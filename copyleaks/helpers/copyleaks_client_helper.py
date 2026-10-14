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
from datetime import datetime, timedelta, timezone

import dateutil.parser

from copyleaks.consts import Consts
from copyleaks.exceptions.auth_expired_error import AuthExipredError


class CopyleaksClientHelper:
    @staticmethod
    def verify_auth_token(auth_token):
        '''
            Verify that Copyleaks authentication token is exists and not expired.

            Parameters:
                auth_token: Copyleaks authentication token

            Raises:
                `AuthExipredError`: authentication expired. Need to login again.
        '''
        assert auth_token and auth_token['.expires'] and auth_token['access_token']

        now = datetime.now(timezone.utc) + timedelta(0, 5 * 60)  # adds 5 minutes ahead for a safety shield.
        upTo = dateutil.parser.parse(auth_token['.expires'])
        if upTo.tzinfo is None:
            upTo = upTo.replace(tzinfo=timezone.utc)

        if upTo <= now:
            raise AuthExipredError()  # expired

    @staticmethod
    def headers(auth_token=None, content_type='application/json'):
        '''
            Request headers: the SDK User-Agent, the `Authorization` bearer token when `auth_token` is given,
            and `Content-Type` when `content_type` is given.
        '''
        headers = {'User-Agent': Consts.USER_AGENT}
        if content_type:
            headers['Content-Type'] = content_type
        if auth_token is not None:
            headers['Authorization'] = f"Bearer {auth_token['access_token']}"
        return headers

    @staticmethod
    def to_json(obj):
        '''
            Serialize a request object (its public attributes, recursively) as compact JSON.
        '''
        return json.dumps(obj, default=lambda o: o.__dict__, separators=(',', ':'))

    @staticmethod
    def to_json_bytes(obj):
        '''
            The UTF-8 bytes of `to_json(obj)`, ready to send as a request body.
        '''
        if hasattr(obj, 'toJSON'):
            text = obj.toJSON()
        else:
            text = CopyleaksClientHelper.to_json(obj)
        return text.encode('utf-8')

    @staticmethod
    def model_to_json_bytes(model):
        '''
            The JSON body of a pydantic request model: camelCase keys, unset optional fields left out.
        '''
        return model.model_dump_json(by_alias=True, exclude_none=True).encode('utf-8')
