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
import unittest

from copyleaksSdk.models.requests.FileDocument import FileDocument
from copyleaksSdk.models.requests.FileOcrDocument import FileOcrDocument
from copyleaksSdk.models.requests.ScanProperties import ScanProperties 
from copyleaksSdk.models.requests.properties.Author import Author 
from copyleaksSdk.models.requests.properties.CallbacksSection import CallbacksSection
from copyleaksSdk.models.requests.properties.ExcludeSection import ExcludeSection
from copyleaksSdk.models.requests.properties.Filters import Filters
from copyleaksSdk.models.requests.properties.Scanning import Scanning
from copyleaksSdk.models.requests.StartRequest import StartRequest
from copyleaksSdk.models.requests.UrlDocument import UrlDocument


class RequestModelTests(unittest.TestCase):

    def test_full_file_document(self):
        data = '''{"base64":"aGVsbG8gd29ybGQ=","filename":"file.txt","properties":{"action":0,"outputMode":1,"developerPayload":"DeveloperPayload","sandbox":true,"callbacks":{"completion":"https://completeion/callback","onNewResult":"https://new-result/callback"},
        "experation":123,"scanning":{"internet":true,"copyleaksDB":true},"exclude":{"references":false,"quotes":false,"titles":false,"htmlTemplate":false},
        "filters":{"idenitcalEnabled":true,"minorChangedEnabled":true,"relatedMeaningEnabled":true,"minCopiedWords":10,"safeSearch":true,"domains":["www.google.com","www.bing.com"],"domainsMode":1},"author":{"id":"AuthorId"}}}'''
        json_data = json.loads(data)
    
        fileDocument = FileDocument(
            base64 = json_data['base64'],
            filename = json_data['filename'],
            properties = ScanProperties(
                action = json_data['properties']['action'],
                outputMode = json_data['properties']['outputMode'],
                developerPayload = json_data['properties']['developerPayload'],
                sandbox = json_data['properties']['sandbox'],
                callbacks = CallbacksSection(json_data['properties']['callbacks']['completion'], json_data['properties']['callbacks']['onNewResult']),
                experation = json_data['properties']['experation'],
                scanning = Scanning(json_data['properties']['scanning']['internet'], json_data['properties']['scanning']['copyleaksDB']),
                exclude = ExcludeSection(
                    json_data['properties']['exclude']['references'], 
                    json_data['properties']['exclude']['quotes'],
                    json_data['properties']['exclude']['titles'],
                    json_data['properties']['exclude']['htmlTemplate']
                ),
                filters = Filters(
                    json_data['properties']['filters']['idenitcalEnabled'], 
                    json_data['properties']['filters']['minorChangedEnabled'], 
                    json_data['properties']['filters']['relatedMeaningEnabled'],
                    json_data['properties']['filters']['minCopiedWords'],
                    json_data['properties']['filters']['safeSearch'],
                    json_data['properties']['filters']['domains'],
                    json_data['properties']['filters']['domainsMode']
                    ),
                author=Author(json_data['properties']['author']['id'])
            )

        )
        self.assertEqual(fileDocument.base64, json_data['base64'])
        self.assertEqual(fileDocument.filename, json_data['filename'])
        self.assertEqual(fileDocument.properties.action, json_data['properties']['action'])
        self.assertEqual(fileDocument.properties.outputMode, json_data['properties']['outputMode'])
        self.assertEqual(fileDocument.properties.developerPayload, json_data['properties']['developerPayload'])
        self.assertEqual(fileDocument.properties.sandbox, json_data['properties']['sandbox'])
        self.assertEqual(fileDocument.properties.callbacks.completion, json_data['properties']['callbacks']['completion'])
        self.assertEqual(fileDocument.properties.callbacks.onNewResult, json_data['properties']['callbacks']['onNewResult'])
        self.assertEqual(fileDocument.properties.experation, json_data['properties']['experation'])
        self.assertEqual(fileDocument.properties.scanning.internet, json_data['properties']['scanning']['internet'])
        self.assertEqual(fileDocument.properties.scanning.copyleaksDB, json_data['properties']['scanning']['copyleaksDB'])
        self.assertEqual(fileDocument.properties.exclude.references, json_data['properties']['exclude']['references'])
        self.assertEqual(fileDocument.properties.exclude.quotes, json_data['properties']['exclude']['quotes'])
        self.assertEqual(fileDocument.properties.exclude.titles, json_data['properties']['exclude']['titles'])
        self.assertEqual(fileDocument.properties.exclude.htmlTemplate, json_data['properties']['exclude']['htmlTemplate'])
        self.assertEqual(fileDocument.properties.filters.idenitcalEnabled, json_data['properties']['filters']['idenitcalEnabled'])
        self.assertEqual(fileDocument.properties.filters.minorChangedEnabled, json_data['properties']['filters']['minorChangedEnabled'])
        self.assertEqual(fileDocument.properties.filters.relatedMeaningEnabled, json_data['properties']['filters']['relatedMeaningEnabled'])
        self.assertEqual(fileDocument.properties.filters.minCopiedWords, json_data['properties']['filters']['minCopiedWords'])
        self.assertEqual(fileDocument.properties.filters.safeSearch, json_data['properties']['filters']['safeSearch'])
        self.assertEqual(fileDocument.properties.filters.domains, json_data['properties']['filters']['domains'])
        self.assertEqual(fileDocument.properties.filters.domainsMode, json_data['properties']['filters']['domainsMode'])
        self.assertEqual(fileDocument.properties.author.id, json_data['properties']['author']['id'])
    
    def test_file_document(self):
        base64 = "aGVsbG8gd29ybGQ="
        filename = "file.txt"
        fileDocument = FileDocument(base64=base64, filename=filename)
        self.assertEqual(fileDocument.base64, base64)
        self.assertEqual(fileDocument.filename, filename)

    def test_full_ocr_file_document(self):
        data = '''{"langCode":"en","base64":"aGVsbG8gd29ybGQ=","filename":"file.txt","properties":{"action":0,"outputMode":1,"developerPayload":"DeveloperPayload","sandbox":true,"callbacks":{"completion":"https://completeion/callback","onNewResult":"https://new-result/callback"},"experation":123,"scanning":{"internet":true,"copyleaksDB":true},"exclude":{"references":false,"quotes":false,"titles":false,"htmlTemplate":false},"filters":{"idenitcalEnabled":true,"minorChangedEnabled":true,"relatedMeaningEnabled":true,"minCopiedWords":10,"safeSearch":true,"domains":["www.google.com","www.bing.com"],"domainsMode":1},"author":{"id":"AuthorId"}}}'''
        json_data = json.loads(data)
    
        fileOcrDocument = FileOcrDocument(
                langCode = json_data['langCode'],
                base64=json_data['base64'],
                filename=json_data['filename'],
                properties=ScanProperties(
                action = json_data['properties']['action'],
                outputMode = json_data['properties']['outputMode'],
                developerPayload = json_data['properties']['developerPayload'],
                sandbox = json_data['properties']['sandbox'],
                callbacks = CallbacksSection(json_data['properties']['callbacks']['completion'], json_data['properties']['callbacks']['onNewResult']),
                experation = json_data['properties']['experation'],
                scanning = Scanning(json_data['properties']['scanning']['internet'], json_data['properties']['scanning']['copyleaksDB']),
                exclude = ExcludeSection(
                    json_data['properties']['exclude']['references'], 
                    json_data['properties']['exclude']['quotes'],
                    json_data['properties']['exclude']['titles'],
                    json_data['properties']['exclude']['htmlTemplate']
                ),
                filters = Filters(
                    json_data['properties']['filters']['idenitcalEnabled'], 
                    json_data['properties']['filters']['minorChangedEnabled'], 
                    json_data['properties']['filters']['relatedMeaningEnabled'],
                    json_data['properties']['filters']['minCopiedWords'],
                    json_data['properties']['filters']['safeSearch'],
                    json_data['properties']['filters']['domains'],
                    json_data['properties']['filters']['domainsMode']
                    ),
                author=Author(json_data['properties']['author']['id'])
            )
        )
        self.assertEqual(fileOcrDocument.langCode, json_data['langCode'])
        self.assertEqual(fileOcrDocument.base64, json_data['base64'])
        self.assertEqual(fileOcrDocument.filename, json_data['filename'])
        self.assertEqual(fileOcrDocument.properties.action, json_data['properties']['action'])
        self.assertEqual(fileOcrDocument.properties.outputMode, json_data['properties']['outputMode'])
        self.assertEqual(fileOcrDocument.properties.developerPayload, json_data['properties']['developerPayload'])
        self.assertEqual(fileOcrDocument.properties.sandbox, json_data['properties']['sandbox'])
        self.assertEqual(fileOcrDocument.properties.callbacks.completion, json_data['properties']['callbacks']['completion'])
        self.assertEqual(fileOcrDocument.properties.callbacks.onNewResult, json_data['properties']['callbacks']['onNewResult'])
        self.assertEqual(fileOcrDocument.properties.experation, json_data['properties']['experation'])
        self.assertEqual(fileOcrDocument.properties.scanning.internet, json_data['properties']['scanning']['internet'])
        self.assertEqual(fileOcrDocument.properties.scanning.copyleaksDB, json_data['properties']['scanning']['copyleaksDB'])
        self.assertEqual(fileOcrDocument.properties.exclude.references, json_data['properties']['exclude']['references'])
        self.assertEqual(fileOcrDocument.properties.exclude.quotes, json_data['properties']['exclude']['quotes'])
        self.assertEqual(fileOcrDocument.properties.exclude.titles, json_data['properties']['exclude']['titles'])
        self.assertEqual(fileOcrDocument.properties.exclude.htmlTemplate, json_data['properties']['exclude']['htmlTemplate'])
        self.assertEqual(fileOcrDocument.properties.filters.idenitcalEnabled, json_data['properties']['filters']['idenitcalEnabled'])
        self.assertEqual(fileOcrDocument.properties.filters.minorChangedEnabled, json_data['properties']['filters']['minorChangedEnabled'])
        self.assertEqual(fileOcrDocument.properties.filters.relatedMeaningEnabled, json_data['properties']['filters']['relatedMeaningEnabled'])
        self.assertEqual(fileOcrDocument.properties.filters.minCopiedWords, json_data['properties']['filters']['minCopiedWords'])
        self.assertEqual(fileOcrDocument.properties.filters.safeSearch, json_data['properties']['filters']['safeSearch'])
        self.assertEqual(fileOcrDocument.properties.filters.domains, json_data['properties']['filters']['domains'])
        self.assertEqual(fileOcrDocument.properties.filters.domainsMode, json_data['properties']['filters']['domainsMode'])
        self.assertEqual(fileOcrDocument.properties.author.id, json_data['properties']['author']['id'])

    def test_ocr_file_document(self):
        langCode = "en"
        base64 = "aGVsbG8gd29ybGQ="
        filename = "file.txt"
        fileOcrDocument = FileOcrDocument(
            langCode = langCode,
            base64=base64,
            filename=filename
        )
        self.assertEqual(fileOcrDocument.langCode, langCode)
        self.assertEqual(fileOcrDocument.base64, base64)
        self.assertEqual(fileOcrDocument.filename, filename)

    def test_full_url_document(self):
        data = '''{"url":"http://www.example.com","properties":{"action":0,"outputMode":1,"developerPayload":"DeveloperPayload","sandbox":true,"callbacks":{"completion":"https://completeion/callback","onNewResult":"https://new-result/callback"},"experation":123,"scanning":{"internet":true,"copyleaksDB":true},"exclude":{"references":false,"quotes":false,"titles":false,"htmlTemplate":false},"filters":{"idenitcalEnabled":true,"minorChangedEnabled":true,"relatedMeaningEnabled":true,"minCopiedWords":10,"safeSearch":true,"domains":["www.google.com","www.bing.com"],"domainsMode":1},"author":{"id":"AuthorId"}}}'''
        json_data = json.loads(data)
        urlDocument = UrlDocument(
                url = json_data['url'],
                properties=ScanProperties(
                action = json_data['properties']['action'],
                outputMode = json_data['properties']['outputMode'],
                developerPayload = json_data['properties']['developerPayload'],
                sandbox = json_data['properties']['sandbox'],
                callbacks = CallbacksSection(json_data['properties']['callbacks']['completion'], json_data['properties']['callbacks']['onNewResult']),
                experation = json_data['properties']['experation'],
                scanning = Scanning(json_data['properties']['scanning']['internet'], json_data['properties']['scanning']['copyleaksDB']),
                exclude = ExcludeSection(
                    json_data['properties']['exclude']['references'], 
                    json_data['properties']['exclude']['quotes'],
                    json_data['properties']['exclude']['titles'],
                    json_data['properties']['exclude']['htmlTemplate']
                ),
                filters = Filters(
                    json_data['properties']['filters']['idenitcalEnabled'], 
                    json_data['properties']['filters']['minorChangedEnabled'], 
                    json_data['properties']['filters']['relatedMeaningEnabled'],
                    json_data['properties']['filters']['minCopiedWords'],
                    json_data['properties']['filters']['safeSearch'],
                    json_data['properties']['filters']['domains'],
                    json_data['properties']['filters']['domainsMode']
                    ),
                author=Author(json_data['properties']['author']['id'])
            )
        )

        self.assertEqual(urlDocument.url, json_data['url'])
        self.assertEqual(urlDocument.properties.action, json_data['properties']['action'])
        self.assertEqual(urlDocument.properties.outputMode, json_data['properties']['outputMode'])
        self.assertEqual(urlDocument.properties.developerPayload, json_data['properties']['developerPayload'])
        self.assertEqual(urlDocument.properties.sandbox, json_data['properties']['sandbox'])
        self.assertEqual(urlDocument.properties.callbacks.completion, json_data['properties']['callbacks']['completion'])
        self.assertEqual(urlDocument.properties.callbacks.onNewResult, json_data['properties']['callbacks']['onNewResult'])
        self.assertEqual(urlDocument.properties.experation, json_data['properties']['experation'])
        self.assertEqual(urlDocument.properties.scanning.internet, json_data['properties']['scanning']['internet'])
        self.assertEqual(urlDocument.properties.scanning.copyleaksDB, json_data['properties']['scanning']['copyleaksDB'])
        self.assertEqual(urlDocument.properties.exclude.references, json_data['properties']['exclude']['references'])
        self.assertEqual(urlDocument.properties.exclude.quotes, json_data['properties']['exclude']['quotes'])
        self.assertEqual(urlDocument.properties.exclude.titles, json_data['properties']['exclude']['titles'])
        self.assertEqual(urlDocument.properties.exclude.htmlTemplate, json_data['properties']['exclude']['htmlTemplate'])
        self.assertEqual(urlDocument.properties.filters.idenitcalEnabled, json_data['properties']['filters']['idenitcalEnabled'])
        self.assertEqual(urlDocument.properties.filters.minorChangedEnabled, json_data['properties']['filters']['minorChangedEnabled'])
        self.assertEqual(urlDocument.properties.filters.relatedMeaningEnabled, json_data['properties']['filters']['relatedMeaningEnabled'])
        self.assertEqual(urlDocument.properties.filters.minorChangedEnabled, json_data['properties']['filters']['minorChangedEnabled'])
        self.assertEqual(urlDocument.properties.filters.minCopiedWords, json_data['properties']['filters']['minCopiedWords'])
        self.assertEqual(urlDocument.properties.filters.safeSearch, json_data['properties']['filters']['safeSearch'])
        self.assertEqual(urlDocument.properties.filters.domains, json_data['properties']['filters']['domains'])
        self.assertEqual(urlDocument.properties.filters.domainsMode, json_data['properties']['filters']['domainsMode'])
        self.assertEqual(urlDocument.properties.author.id, json_data['properties']['author']['id'])

    def test_url_document(self):
        url = "http://www.example.com"
        
        urlDocument = UrlDocument(url)
        self.assertEqual(urlDocument.url, url)
