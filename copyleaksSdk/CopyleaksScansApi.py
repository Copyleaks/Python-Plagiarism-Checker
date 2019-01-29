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

from copyleaksSdk.exceptions.Commandfailederror import CommandFailedError
from copyleaksSdk.helpers.Settings import Settings
from copyleaksSdk.helpers.RequestHelper import RequestHelper
from copyleaksSdk.models.requests.FileDocument import FileDocument
from copyleaksSdk.models.requests.FileOcrDocument import FileOcrDocument
from copyleaksSdk.models.requests.StartRequest import StartRequest
from copyleaksSdk.models.requests.UrlDocument import UrlDocument
from copyleaksSdk.models.responses.DeleteResponse import DeleteResponse
from copyleaksSdk.models.responses.result.Result import Result
from copyleaksSdk.models.responses.StartResponse import StartResponse
from copyleaksSdk.models.requests.StartBatchRequest import StartBatchRequest
from copyleaksSdk.models.types.eErrorHandling import eErrorHandling
from copyleaksSdk.models.responses.SupportedTypesResponse import SupportedTypesResponse
from copyleaksSdk.models.responses.download.DownloadResponse import DownloadResponse

class CopyleaksScansApi:
    '''
    Make requests to Copyleaks scan API, scan content and get the results of your scan
    '''

    def __init__(self, product, token, certificate=None):
        assert product, 'Missing product!'
        assert token, 'Missing token!'
        self.product = product
        self.token = token
        self.headers = RequestHelper.get_authentication_header(self.token)
        self.copyleaks_api_server = Settings.ApiEndPoint
        self.api_version = Settings.ApiVersion
        self.timeout = Settings.RequestsTimeout
        self.certificate = certificate

    def credit_balance(self):
        '''
        Get your current credit balance
        '''
        url = f"{self.copyleaks_api_server}{self.api_version}/{self.product}/credits"

        response = requests.get(url, headers=self.headers,
                                timeout=self.timeout, cert=self.certificate)
        balance = RequestHelper.extract_json_from_response(response)
        return balance.get('Amount')

    def __submit(self, scan_id, model, url):
        headers = RequestHelper.get_authentication_header(self.token)
        data = json.dumps(model, default=lambda o: o.__dict__,
                          ensure_ascii=False)
        response = requests.put(
            url, headers=headers, data=data, timeout=self.timeout, cert=self.certificate)
        RequestHelper.validate_response(response)

    def submit_url(self, scan_id, url_document):
        '''
        Submitting URL to plagiarism scan
        '''
        if not isinstance(url_document, UrlDocument):
            raise ValueError(f"model must be of type: {type(UrlDocument)}")
        url = f"{self.copyleaks_api_server}{self.api_version}/{self.product}/submit/url/{scan_id}"
        return self.__submit(scan_id, url_document, url)

    def submit_file(self, scan_id, file_document):
        '''
        Submitting local file or free text to plagiarism scan
        '''
        if not isinstance(file_document, FileDocument):
            raise ValueError(f"model must be of type: {type(FileDocument)}")
        url = f"{self.copyleaks_api_server}{self.api_version}/{self.product}/submit/file/{scan_id}"
        return self.__submit(scan_id, file_document, url)

    def submit_ocr(self, scan_id, ocr_document):
        '''
        Submitting an image containing textual content to plagiarism scan
        '''
        if not isinstance(ocr_document, FileOcrDocument):
            raise ValueError(f"model must be of type: {type(FileOcrDocument)}")
        url = f"{self.copyleaks_api_server}{self.api_version}/{self.product}/submit/file/{scan_id}"
        return self.__submit(scan_id, ocr_document, url)

    def progress(self, scan_id):
        '''
        Get the progress of the scan in percents
        '''
        url = f"{self.copyleaks_api_server}{self.api_version}/{self.product}/{scan_id}/progress"
        response = requests.get(url, headers=self.headers,
                                timeout=self.timeout, cert=self.certificate)
        json_response = RequestHelper.extract_json_from_response(response)
        return json_response['percents']

    def delete(self, scan_ids):
        '''
        Deletes a completed scan
        '''
        url = f"{self.copyleaks_api_server}{self.api_version}/{self.product}/delete"
        model = {
            'id': scan_ids
        }
        data = json.dumps(model, default=lambda o: o.__dict__,
                          ensure_ascii=False)
        response = requests.patch(
            url, headers=self.headers, timeout=self.timeout, data=data, cert=self.certificate)
        json_response = RequestHelper.extract_json_from_response(response)
        return DeleteResponse(json_response)

    def start(self, trigger, errorHandling=eErrorHandling.Cancel):
        '''
        Start a scan which is in 'price checked' status
        '''
        start_request = StartRequest(trigger, errorHandling)
        url = f"{self.copyleaks_api_server}{self.api_version}/{self.product}/start"
        data = json.dumps(
            start_request, default=lambda o: o.__dict__, ensure_ascii=False)
        response = requests.patch(
            url, headers=self.headers, timeout=self.timeout, data=data, cert=self.certificate)
        json_response = RequestHelper.extract_json_from_response(response)
        return StartResponse(json_response)

    def start_batch(self, trigger, include=[], errorHandling=eErrorHandling.Cancel):
        '''
        Starts a batch scan for a list of 'priceChecked' scans 
        '''
        start_batch_request = StartBatchRequest(
            trigger, include, errorHandling)
        url = f"{self.copyleaks_api_server}{self.api_version}/{self.product}/batch/start"
        data = json.dumps(start_batch_request,
                          default=lambda o: o.__dict__, ensure_ascii=False)
        response = requests.patch(
            url, headers=self.headers, timeout=self.timeout, data=data, cert=self.certificate)
        json_response = RequestHelper.extract_json_from_response(response)
        return StartResponse(json_response)

    def result(self, scan_id):
        '''
        Get the scan results from Copyleaks servers.
        '''
        url = f"{self.copyleaks_api_server}{self.api_version}/{self.product}/{scan_id}/result"
        response = requests.get(
            url, headers=self.headers, timeout=self.timeout, cert=self.certificate)
        json_response = RequestHelper.extract_json_from_response(response)
        return Result(json_response)

    def download_result(self, result_id):
        '''
        Get the report for the result id
        '''
        url = f"{self.copyleaks_api_server}{self.api_version}/downloads/{result_id}"
        response = requests.get(url, headers=self.headers, timeout=self.timeout, cert=self.certificate)
        json_response = RequestHelper.extract_json_from_response(response)
        return DownloadResponse(json_response)

    def get_supported_file_types(self):
        '''
        
        '''
        url = f"{self.copyleaks_api_server}v1/miscellaneous/supported-file-types"
        response = requests.get(url)
        json_response = RequestHelper.extract_json_from_response(response)
        return SupportedTypesResponse(json_response)
    
    def get_ocr_language_list(self):
        url = f"{self.copyleaks_api_server}v1/miscellaneous/ocr-languages-list"
        response = requests.get(url)
        json_response = RequestHelper.extract_json_from_response(response)
        return json_response
