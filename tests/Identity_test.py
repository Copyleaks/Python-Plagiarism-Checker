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

import unittest

from datetime import datetime, timedelta
from dateutil import parser
from copyleaksSdk.CopyleaksIdentityApi import CopyleaksIdentityApi

class identity_test(unittest.TestCase):
    TOKEN = ""
    EMAIL = "YOUR EMAIL"
    API_KEY = "YOUR API KEY"
    SCAN_ID="YOUR SCAN ID"
    
    def setUp(self):
        assert identity_test.EMAIL != "YOUR EMAIL", "Email is missing"
        assert identity_test.API_KEY != "YOUR API KEY", "api key is missing"
        assert identity_test.SCAN_ID != "YOUR SCAN ID", "Scan id is missing"
    def test_login(self):
        identity = CopyleaksIdentityApi()
        token = identity.login(identity_test.EMAIL, identity_test.API_KEY)

        self.assertTrue(len(token.access_token) > 10)
        
        issued = parser.parse(token.issued).replace(tzinfo=None)
        self.assertAlmostEqual(issued, datetime.utcnow(), delta=timedelta(days=2))
        
        expires = parser.parse(token.expires).replace(tzinfo=None)
        self.assertAlmostEqual(expires, datetime.utcnow(), delta=timedelta(days=2))
        identity_test.TOKEN = token.access_token

    def test_readonly_key(self):
        identity = CopyleaksIdentityApi()
        new_key = identity.regenerate_readonly_key(identity_test.TOKEN, identity_test.SCAN_ID)
        self.assertFalse(new_key == "")

        existing_key = identity.get_read_only_key(identity_test.TOKEN, identity_test.SCAN_ID)
        self.assertEqual(existing_key, new_key)
        identity.delete_readonly_key(identity_test.TOKEN, identity_test.SCAN_ID)
        with self.assertRaises(Exception):
            _ = identity.get_read_only_key(identity_test.TOKEN, identity_test.SCAN_ID)
