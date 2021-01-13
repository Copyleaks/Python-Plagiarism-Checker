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
from abc import ABC


class Export:
    def get_completion_webhook(self):
        '''
            Scan id to export.
        '''
        return self.completionWebhook

    def set_completion_webhook(self, value):
        '''
            Scan id to export.

            Parameters: 
                value: String (uri).
        '''

        assert value

        self.completionWebhook = value

    def get_max_retries(self):
        '''
            How many retries to send before giving up. 
            Using high value (12) may lead to a longer time until the completionWebhook being executed.
            A low value (1) may lead to errors while your service is temporary having problems.
        '''
        return self.maxRetries

    def set_max_retries(self, value):
        '''
            How many retries to send before giving up. 
            Using high value (12) may lead to a longer time until the completionWebhook being executed.
            A low value (1) may lead to errors while your service is temporary having problems.

            Parameters: 
                value: String (uri).
        '''

        assert value and value >= 1 and value <= 12

        self.maxRetries = value

    def get_developer_payload(self):
        '''
            Add a custom developer payload that will then be provided on the Export-Completed webhook.
        '''
        return self.developerPayload

    def set_developer_payload(self, value):
        '''
            Add a custom developer payload that will then be provided on the Export-Completed webhook.

            Parameters: 
                value: String (uri).
        '''

        assert value and len(value) <= 512

        self.developerPayload = value

    def get_results(self):
        '''
            An list of results to be exported.
        '''
        return self.results

    def set_results(self, value):
        '''
            An list of results to be exported.

            Parameters: 
                value: `ExportResult` list.
        '''

        assert value

        self.results = value

    def get_pdf_report(self):
        '''
            Download the PDF report. Allowed only when `properties.pdf.create` was set to true on the scan submittion.
        '''
        return self.pdfReport

    def set_pdf_report(self, value):
        '''
            Download the PDF report. Allowed only when `properties.pdf.create` was set to true on the scan submittion.

            Parameters: 
                value: `ExportPdf`.
        '''

        assert value

        self.pdfReport = value

    def get_crawled_version(self):
        '''
            Download the crawled version of the submitted text.
        '''
        return self.crawledVersion

    def set_crawled_version(self, value):
        '''
            Download the crawled version of the submitted text.

            Parameters: 
                value: `ExportCrawledVersion`.
        '''

        assert value

        self.crawledVersion = value

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class ExportItem(ABC):
    def get_endpoint(self):
        '''
            The HTTP url to upload the data.
        '''
        return self.endpoint

    def set_endpoint(self, value):
        '''
            The HTTP url to upload the data.

            Parameters: 
                value: String.
        '''

        assert value

        self.endpoint = value

    def get_verb(self):
        '''
            The HTTP verb (also called "HTTP Methods") to upload the data to your specified endpoint.
        '''
        return self.verb

    def set_verb(self, value):
        '''
            The HTTP verb (also called "HTTP Methods") to upload the data to your specified endpoint.

            Parameters: 
                value: String.
        '''

        assert value

        self.verb = value

    def get_headers(self):
        '''
            List of headers to be submitted with the upload request. You may use this field to provide additional request headers, such as "Authorization" header.
        '''
        return self.headers

    def set_headers(self, value):
        '''
            List of headers to be submitted with the upload request. You may use this field to provide additional request headers, such as "Authorization" header.

            Parameters: 
                value: List of list of strings.

            Example:
                [["header-key1", "header-value1"], ["header-key2", "header-value2"]]
        '''

        assert value

        self.headers = value


class ExportResult(ExportItem):
    def get_id(self):
        '''
            Result identification to be downloaded. You get these identifications from the completed webhook.
        '''
        return self.id

    def set_id(self, value):
        '''
            Result identification to be downloaded. You get these identifications from the completed webhook.

            Parameters: 
                value: String.
        '''

        assert value

        self.id = value


class ExportPdf(ExportItem):
    def __init__(self):
        pass


class ExportCrawledVersion(ExportItem):
    def __init__(self):
        pass
