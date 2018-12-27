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
import uuid
import json

from copyleaksSdk.CopyleaksIdentityApi import CopyleaksIdentityApi
from copyleaksSdk.CopyleaksScansApi import CopyleaksScansApi
from copyleaksSdk.models.types.eProduct import eProduct
from copyleaksSdk.models.requests.FileDocument import FileDocument
from copyleaksSdk.models.requests.UrlDocument import UrlDocument
from copyleaksSdk.models.requests.FileOcrDocument import FileOcrDocument
from copyleaksSdk.models.requests.ScanProperties import ScanProperties
from copyleaksSdk.models.types.eSubmitAction import eSubmitAction
from copyleaksSdk.models.requests.StartRequest import StartRequest


class scan_api_test(unittest.TestCase):
    EMAIL = "YOUR EMAIL"
    API_KEY = "YOUR API KEY"
    
    def setUp(self):
        self.token = CopyleaksIdentityApi().login(scan_api_test.EMAIL, scan_api_test.API_KEY).access_token
        self.scan_id = uuid.uuid4()
        #self.scan_id = "python_test2"
        self.api = CopyleaksScansApi(eProduct.Education, self.token)
    
    def test_credit_balance(self):
        credit_balance = self.api.credit_balance()
        self.assertTrue(type(credit_balance) is int)
    
    def test_submit_file(self):
        file_document = FileDocument(
            base64 = "aGVsbG8gd29ybGQ=",
            filename = "file.txt",
            properties=ScanProperties(
                action = eSubmitAction.checkCredits,
                sandbox = True,
                experation = 2880
            )
            
        )
        try:
            self.api.submit_file(f"file_{self.scan_id}", file_document)
        except Exception as ex:
            self.fail(f"submit file has failed: {ex}")
    
    def test_submit_url(self):
        url = "http://example.com"
        
        url_document = UrlDocument(
            url,
            properties=ScanProperties(
                action = eSubmitAction.checkCredits,
                sandbox = True                
            )
        )
        try:
            self.api.submit_url(f"url_{self.scan_id}", url_document)
        except Exception as ex:
            self.fail(f"submit file has failed: {ex}")

    def test_submit_ocr(self):
        ocr_document = FileOcrDocument(
            langCode = 'en',
            base64='''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''',
            filename = "ocr_file.txt",
            properties=ScanProperties(
                    action = eSubmitAction.checkCredits,
                    sandbox = True,
                    experation = 2880
            )
        )
        try:
            self.api.submit_ocr(f"ocr_file_{self.scan_id}", ocr_document)
        except Exception as ex:
            self.fail(f"submit ocr file has failed: {ex}")
    
    def test_progress(self):
        progress = self.api.progress(f"url_{self.scan_id}")
        self.assertTrue(type(progress) is int)

    def test_results(self):
        result = self.api.result(f"url_{self.scan_id}")
        self.assertTrue(result.scannedDocument.totalWords == 2)

    def test_start(self):
        try:
            self.api.start([f"file_{self.scan_id}"])
        except Exception as ex:
            self.fail(f"start request failed: {ex}")
        
    def test_delete(self):
        try:
            self.api.delete([f"file_{self.scan_id}"])
        except Exception as ex:
            self.fail(f"delete request failed: {ex}")
    
    def test_get_supported_file_types(self):
        result = self.api.get_supported_file_types()
        self.assertTrue("docx" in result.textual)
        self.assertTrue("png" in result.ocr)

    def test_get_ocr_language_list(self):
        result = self.api.get_ocr_language_list()
        self.assertTrue("en" in result)