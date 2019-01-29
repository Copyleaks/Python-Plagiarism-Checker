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
import json

from copyleaksSdk.models.responses.DeleteResponse import DeleteResponse
from copyleaksSdk.models.responses.LoginResponse import LoginResponse
from copyleaksSdk.models.responses.StartResponse import StartResponse
from copyleaksSdk.models.responses.result.Result import Result
from copyleaksSdk.models.responses.SupportedTypesResponse import SupportedTypesResponse
from copyleaksSdk.models.responses.download.DownloadResponse import DownloadResponse

class ResponseModelTests(unittest.TestCase):

    def test_start_response(self):
        data = '{"success":[{"id":"1"},{"id":"2"},{"id":"3"}],"failed":[{"id":"4"},{"id":"5"},{"id":"6"}]}'

        startResponse = StartResponse(json.loads(data))
        success = list(map(lambda x: x.id, startResponse.success))
        failed =  list(map(lambda x: x.id, startResponse.failed))
        self.assertTrue(success == ['1','2','3'])
        self.assertTrue(failed == ['4','5','6'])
        data = '{"success":[{"id":"1"},{"id":"2"},{"id":"3"}],"failed":[]}'
        startResponse = StartResponse(json.loads(data))
        success = list(map(lambda x: x.id, startResponse.success))
        failed =  list(map(lambda x: x.id, startResponse.failed))
        
        self.assertEqual(success, ['1','2','3'])
        self.assertEqual(failed, [])

    def test_delete_response(self):
        data = '{"failures":[{"id":"0","description":"description0"},{"id":"1","description":"description1"}]}'
        deleteResponse = DeleteResponse(json.loads(data))
        for idx, failure in enumerate(deleteResponse.failures):
            self.assertEqual(failure.id, str(idx))
            self.assertEqual(failure.description, f"description{idx}")

    def test_login_response(self):
        data = '''{
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBZG1pbmlzdHJhdG9yIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvZW1haWxhZGRyZXNzIjoiZXJlemhAY29weWxlYWtzLmNvbSIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL25hbWVpZGVudGlmaWVyIjoiYTUwNWE3MGUtYzZjOS00NDMwLTkzMDUtZjlkMmEzNTcxNDJhIiwiZXhwIjoxNTQyNzgyMzYyLCJpc3MiOiJjb3B5bGVha3MuY29tIiwiYXVkIjoiYXBpLXYxLmNvcHlsZWFrcy5jb20ifQ.SkbPcFYKQ7rNJ1aILiymMypMFlvdbXGs0pZIUvg8pw0zQSII8Pzndxzlum-8a7NSNnfSHJEPWyaDJqR-3Oemvslc8W8WrxiHmZ4in0u4Da8CgmDXd0Xaz0JrCt-mo30fqoH76RXD2Jpc2PITdlrQd7qbdyLA05giy1k6ym_CNSiqzffwvVafriHTYLNJwoZ82O_rWZYLxsUxLmQEojmpgOZT4s9CS0a1WzZoyHpmK8WGGgRp-sQ3Br-8HJxrGnqxwutIR_DrgGuwvukJfoq-BvIgYrdm6FNogsGjfHfwz4yj2zL3xI_3Stg8WnkyzsyuWtn8kqnfBGKvmqS9kxF12Q",
            ".issued": "2018-11-19T06:39:22.0751069Z",
            ".expires": "2018-11-21T06:39:22.075107Z"
        }'''
        json_data = json.loads(data)
        loginResponse = LoginResponse(json_data)
        self.assertEqual(loginResponse.access_token, json_data['access_token'])
        self.assertEqual(loginResponse.issued, json_data['.issued'])
        self.assertEqual(loginResponse.expires, json_data['.expires'])

    def test_full_result_response(self):
        data = '''{"scannedDocument":{"totalWords":100,"totalExcluded":10,"credits":10,"creationTime":"0001-01-01T00:00:00","cachedVersion":"https://report/url"},"results":{"internet":[{"url":"https://internet1","id":"internet1","title":"internet1 title","introduction":"internet1","matchedWords":1,"comparison":"https://internet1/comperison/result"},{"url":"https://internet2","id":"internet2","title":"internet2 title","introduction":"internet2","matchedWords":2,"comparison":"https://internet2/comperison/result"}],"database":[{"scanId":"scanid1","id":"Database1","title":"Database1 title","introduction":"Database1","matchedWords":1,"comparison":"https://Database1/comperison/result"},{"scanId":"scanid2","id":"Database2","title":"Database2 title","introduction":"Database2","matchedWords":2,"comparison":"https://Database2/comperison/result"}],"batch":[{"scanId":"scanid1","id":"batch1","title":"batch1 title","introduction":"batch1","matchedWords":1,"comparison":"https://batch1/comperison/result"},{"scanId":"scanid2","id":"batch2","title":"batch2 title","introduction":"batch2","matchedWords":2,"comparison":"https://batch2/comperison/result"}],"score":{"identicalWords":10,"minorChangedWords":5,"relatedMeaningWords":3}},"status":4,"error":{"message":"Error meassage","code":1},"developerPayload":"payload"}'''
        json_data = json.loads(data)
        result = Result(json_data)
        self.assertEqual(result.status, json_data['status'])
        self.assertEqual(result.developerPayload, json_data['developerPayload'])
        self.assertEqual(result.error.code, json_data['error']['code'])
        self.assertEqual(result.error.message, json_data['error']['message'])
    
        self.assertEqual(result.scannedDocument.totalWords, json_data['scannedDocument']['totalWords'])
        self.assertEqual(result.scannedDocument.totalExcluded, json_data['scannedDocument']['totalExcluded'])
        self.assertEqual(result.scannedDocument.credits, json_data['scannedDocument']['credits'])
        self.assertEqual(result.scannedDocument.creationTime, json_data['scannedDocument']['creationTime'])
        self.assertEqual(result.scannedDocument.cachedVersion, json_data['scannedDocument']['cachedVersion'])
    
        for idx, _ in enumerate(json_data['results']['internet']):
            self.assertEqual(result.results.internet[idx].url, json_data['results']['internet'][idx]['url'])
            self.assertEqual(result.results.internet[idx].id, json_data['results']['internet'][idx]['id'])
            self.assertEqual(result.results.internet[idx].title, json_data['results']['internet'][idx]['title'])
            self.assertEqual(result.results.internet[idx].introduction, json_data['results']['internet'][idx]['introduction'])
            self.assertEqual(result.results.internet[idx].matchedWords, json_data['results']['internet'][idx]['matchedWords'])
        for idx, _ in enumerate(json_data['results']['database']):
            self.assertEqual(result.results.database[idx].scanId, json_data['results']['database'][idx]['scanId'])
            self.assertEqual(result.results.database[idx].id, json_data['results']['database'][idx]['id'])
            self.assertEqual(result.results.database[idx].title, json_data['results']['database'][idx]['title'])
            self.assertEqual(result.results.database[idx].introduction, json_data['results']['database'][idx]['introduction'])
            self.assertEqual(result.results.database[idx].matchedWords, json_data['results']['database'][idx]['matchedWords'])
    
        for idx, _ in enumerate(json_data['results']['batch']):
            self.assertEqual(result.results.batch[idx].scanId, json_data['results']['batch'][idx]['scanId'])
            self.assertEqual(result.results.batch[idx].id, json_data['results']['batch'][idx]['id'])
            self.assertEqual(result.results.batch[idx].title, json_data['results']['batch'][idx]['title'])
            self.assertEqual(result.results.batch[idx].introduction, json_data['results']['batch'][idx]['introduction'])
            self.assertEqual(result.results.batch[idx].matchedWords, json_data['results']['batch'][idx]['matchedWords'])

        self.assertEqual(result.results.score.identicalWords, json_data['results']['score']['identicalWords'])
        self.assertEqual(result.results.score.minorChangedWords, json_data['results']['score']['minorChangedWords'])
        self.assertEqual(result.results.score.relatedMeaningWords, json_data['results']['score']['relatedMeaningWords'])
   
    def test_result_response(self):
        data = '''{"scannedDocument":{"totalWords":100,"totalExcluded":10,"credits":10,"creationTime":"0001-01-01T00:00:00","cachedVersion":"https://report/url"},"status":4,"error":{"message":"Error meassage","code":1},"developerPayload":"payload"}'''
        json_data = json.loads(data)
        result = Result(json_data)
        self.assertEqual(result.status, json_data['status'])
        self.assertEqual(result.developerPayload, json_data['developerPayload'])
        self.assertEqual(result.error.code, json_data['error']['code'])
        self.assertEqual(result.error.message, json_data['error']['message'])
    
        self.assertEqual(result.scannedDocument.totalWords, json_data['scannedDocument']['totalWords'])
        self.assertEqual(result.scannedDocument.totalExcluded, json_data['scannedDocument']['totalExcluded'])
        self.assertEqual(result.scannedDocument.credits, json_data['scannedDocument']['credits'])
        self.assertEqual(result.scannedDocument.creationTime, json_data['scannedDocument']['creationTime'])
        self.assertEqual(result.scannedDocument.cachedVersion, json_data['scannedDocument']['cachedVersion'])

    def test_supported_types_response(self):
        data = '''{"textual":["pdf","docx","doc","txt","rtf","xml","pptx","ppt","odt","chm","epub","odp","ppsx","pages","xlsx","xls","csv","LaTeX"],"ocr":["gif","png","bmp","jpg","jpeg"]}'''
        json_data = json.loads(data)
        result = SupportedTypesResponse(json_data)
        self.assertEqual(result.textual, json_data['textual'])
        self.assertEqual(result.ocr, json_data['ocr'])

    def test_download_response(self):
        data = '''{"statistics": { "identical": 2, "minorChanges": 0, "relatedMeaning": 0 }, "text": { "value": "some text", "pages": { "startPosition": [ 0, 1499 ] }, "comparison": { "identical": { "groupId": [ 0 ], "source": { "chars": { "starts": [ 0 ], "lengths": [ 11 ] }, "words": { "starts": [ 0 ], "lengths": [ 1 ] } }, "suspected": { "chars": { "starts": [ 341 ], "lengths": [ 11 ] }, "words": { "starts": [ 46 ], "lengths": [ 1 ] } } }, "minorChanges": { "groupId": [0], "source": { "chars": { "starts": [0], "lengths": [11] }, "words": { "starts": [0], "lengths": [11] } }, "suspected": { "chars": { "starts": [0], "lengths": [11] }, "words": { "starts": [0], "lengths": [11] } } }, "relatedMeaning": { "groupId": [1], "source": { "chars": { "starts": [0], "lengths": [11] }, "words": { "starts": [0], "lengths": [11] } }, "suspected": { "chars": { "starts": [0], "lengths": [11] }, "words": { "starts": [0], "lengths": [11] } } } } }, "html": { "value": "<!DOCTYPE html>some text</html>", "pages": null, "comparison": { "identical": { "groupId": [ 0 ], "source": { "chars": { "starts": [ 0 ], "lengths": [ 11 ] }, "words": { "starts": [ 0 ], "lengths": [ 1 ] } }, "suspected": { "chars": { "starts": [ 7070 ], "lengths": [ 11 ] }, "words": { "starts": [ 46 ], "lengths": [ 1 ] } } }, "minorChanges": { "groupId": [0], "source": { "chars": { "starts": [0], "lengths": [11] }, "words": { "starts": [0], "lengths": [11] } }, "suspected": { "chars": { "starts": [0], "lengths": [11] }, "words": { "starts": [0], "lengths": [11] } } }, "relatedMeaning": { "groupId": [0], "source": { "chars": { "starts": [0], "lengths": [11] }, "words": { "starts": [0], "lengths": [11] } }, "suspected": { "chars": { "starts": [0], "lengths": [11] }, "words": { "starts": [0], "lengths": [11]}}}}}}'''
        json_data = json.loads(data)
        result = DownloadResponse(json_data)
        #stats
        self.assertEqual(result.statistics.identical,
                         json_data['statistics']['identical'])
        self.assertEqual(result.statistics.minorChanges,
                         json_data['statistics']['minorChanges'])
        self.assertEqual(result.statistics.relatedMeaning,
                         json_data['statistics']['relatedMeaning'])
        # text section
        self.assertEqual(result.text.value, json_data['text']['value'])
        self.assertEqual(result.text.pages.startPosition, json_data['text']['pages']['startPosition'])
        self.assertEqual(result.text.comparison.identical.groupId, json_data['text']['comparison']['identical']['groupId'])
        # identical
        self.assertEqual(result.text.comparison.identical.source.chars.starts,
                        json_data['text']['comparison']['identical']['source']['chars']['starts'])
        self.assertEqual(result.text.comparison.identical.source.chars.lengths,
                        json_data['text']['comparison']['identical']['source']['chars']['lengths'])
        self.assertEqual(result.text.comparison.identical.source.words.starts,
                        json_data['text']['comparison']['identical']['source']['words']['starts'])
        self.assertEqual(result.text.comparison.identical.source.words.lengths,
                         json_data['text']['comparison']['identical']['source']['words']['lengths'])

        self.assertEqual(result.text.comparison.identical.suspected.chars.starts,
                        json_data['text']['comparison']['identical']['suspected']['chars']['starts'])
        self.assertEqual(result.text.comparison.identical.suspected.chars.lengths,
                        json_data['text']['comparison']['identical']['suspected']['chars']['lengths'])
        self.assertEqual(result.text.comparison.identical.suspected.words.starts,
                        json_data['text']['comparison']['identical']['suspected']['words']['starts'])
        self.assertEqual(result.text.comparison.identical.suspected.words.lengths,
                         json_data['text']['comparison']['identical']['suspected']['words']['lengths'])
        
        # minorChanges
        self.assertEqual(result.text.comparison.minorChanges.source.chars.starts,
                         json_data['text']['comparison']['minorChanges']['source']['chars']['starts'])
        self.assertEqual(result.text.comparison.minorChanges.source.chars.lengths,
                         json_data['text']['comparison']['minorChanges']['source']['chars']['lengths'])
        self.assertEqual(result.text.comparison.minorChanges.source.words.starts,
                         json_data['text']['comparison']['minorChanges']['source']['words']['starts'])
        self.assertEqual(result.text.comparison.minorChanges.source.words.lengths,
                         json_data['text']['comparison']['minorChanges']['source']['words']['lengths'])

        self.assertEqual(result.text.comparison.minorChanges.suspected.chars.starts,
                         json_data['text']['comparison']['minorChanges']['suspected']['chars']['starts'])
        self.assertEqual(result.text.comparison.minorChanges.suspected.chars.lengths,
                         json_data['text']['comparison']['minorChanges']['suspected']['chars']['lengths'])
        self.assertEqual(result.text.comparison.minorChanges.suspected.words.starts,
                         json_data['text']['comparison']['minorChanges']['suspected']['words']['starts'])
        self.assertEqual(result.text.comparison.minorChanges.suspected.words.lengths,
                         json_data['text']['comparison']['minorChanges']['suspected']['words']['lengths'])

        # relatedMeaning
        self.assertEqual(result.text.comparison.relatedMeaning.source.chars.starts,
                         json_data['text']['comparison']['relatedMeaning']['source']['chars']['starts'])
        self.assertEqual(result.text.comparison.relatedMeaning.source.chars.lengths,
                         json_data['text']['comparison']['relatedMeaning']['source']['chars']['lengths'])
        self.assertEqual(result.text.comparison.relatedMeaning.source.words.starts,
                         json_data['text']['comparison']['relatedMeaning']['source']['words']['starts'])
        self.assertEqual(result.text.comparison.relatedMeaning.source.words.lengths,
                         json_data['text']['comparison']['relatedMeaning']['source']['words']['lengths'])

        self.assertEqual(result.text.comparison.relatedMeaning.suspected.chars.starts,
                         json_data['text']['comparison']['relatedMeaning']['suspected']['chars']['starts'])
        self.assertEqual(result.text.comparison.relatedMeaning.suspected.chars.lengths,
                         json_data['text']['comparison']['relatedMeaning']['suspected']['chars']['lengths'])
        self.assertEqual(result.text.comparison.relatedMeaning.suspected.words.starts,
                         json_data['text']['comparison']['relatedMeaning']['suspected']['words']['starts'])
        self.assertEqual(result.text.comparison.relatedMeaning.suspected.words.lengths,
                         json_data['text']['comparison']['relatedMeaning']['suspected']['words']['lengths'])
        # html section
        
        self.assertEqual(result.html.value, json_data['html']['value'])
        
        self.assertEqual(result.html.comparison.identical.groupId,
                         json_data['html']['comparison']['identical']['groupId'])
        # identical
        self.assertEqual(result.html.comparison.identical.source.chars.starts,
                         json_data['html']['comparison']['identical']['source']['chars']['starts'])
        self.assertEqual(result.html.comparison.identical.source.chars.lengths,
                         json_data['html']['comparison']['identical']['source']['chars']['lengths'])
        self.assertEqual(result.html.comparison.identical.source.words.starts,
                         json_data['html']['comparison']['identical']['source']['words']['starts'])
        self.assertEqual(result.html.comparison.identical.source.words.lengths,
                         json_data['html']['comparison']['identical']['source']['words']['lengths'])

        self.assertEqual(result.html.comparison.identical.suspected.chars.starts,
                         json_data['html']['comparison']['identical']['suspected']['chars']['starts'])
        self.assertEqual(result.html.comparison.identical.suspected.chars.lengths,
                         json_data['html']['comparison']['identical']['suspected']['chars']['lengths'])
        self.assertEqual(result.html.comparison.identical.suspected.words.starts,
                         json_data['html']['comparison']['identical']['suspected']['words']['starts'])
        self.assertEqual(result.html.comparison.identical.suspected.words.lengths,
                         json_data['html']['comparison']['identical']['suspected']['words']['lengths'])

        # minorChanges
        self.assertEqual(result.html.comparison.minorChanges.source.chars.starts,
                         json_data['html']['comparison']['minorChanges']['source']['chars']['starts'])
        self.assertEqual(result.html.comparison.minorChanges.source.chars.lengths,
                         json_data['html']['comparison']['minorChanges']['source']['chars']['lengths'])
        self.assertEqual(result.html.comparison.minorChanges.source.words.starts,
                         json_data['html']['comparison']['minorChanges']['source']['words']['starts'])
        self.assertEqual(result.html.comparison.minorChanges.source.words.lengths,
                         json_data['html']['comparison']['minorChanges']['source']['words']['lengths'])

        self.assertEqual(result.html.comparison.minorChanges.suspected.chars.starts,
                         json_data['html']['comparison']['minorChanges']['suspected']['chars']['starts'])
        self.assertEqual(result.html.comparison.minorChanges.suspected.chars.lengths,
                         json_data['html']['comparison']['minorChanges']['suspected']['chars']['lengths'])
        self.assertEqual(result.html.comparison.minorChanges.suspected.words.starts,
                         json_data['html']['comparison']['minorChanges']['suspected']['words']['starts'])
        self.assertEqual(result.html.comparison.minorChanges.suspected.words.lengths,
                         json_data['html']['comparison']['minorChanges']['suspected']['words']['lengths'])

        # relatedMeaning
        self.assertEqual(result.html.comparison.relatedMeaning.source.chars.starts,
                         json_data['html']['comparison']['relatedMeaning']['source']['chars']['starts'])
        self.assertEqual(result.html.comparison.relatedMeaning.source.chars.lengths,
                         json_data['html']['comparison']['relatedMeaning']['source']['chars']['lengths'])
        self.assertEqual(result.html.comparison.relatedMeaning.source.words.starts,
                         json_data['html']['comparison']['relatedMeaning']['source']['words']['starts'])
        self.assertEqual(result.html.comparison.relatedMeaning.source.words.lengths,
                         json_data['html']['comparison']['relatedMeaning']['source']['words']['lengths'])

        self.assertEqual(result.html.comparison.relatedMeaning.suspected.chars.starts,
                         json_data['html']['comparison']['relatedMeaning']['suspected']['chars']['starts'])
        self.assertEqual(result.html.comparison.relatedMeaning.suspected.chars.lengths,
                         json_data['html']['comparison']['relatedMeaning']['suspected']['chars']['lengths'])
        self.assertEqual(result.html.comparison.relatedMeaning.suspected.words.starts,
                         json_data['html']['comparison']['relatedMeaning']['suspected']['words']['starts'])
        self.assertEqual(result.html.comparison.relatedMeaning.suspected.words.lengths,
                         json_data['html']['comparison']['relatedMeaning']['suspected']['words']['lengths'])
