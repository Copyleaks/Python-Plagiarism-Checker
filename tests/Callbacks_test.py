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

from copyleaksSdk.models.callbacks.CompletedCallback import CompletedCallback
from copyleaksSdk.models.callbacks.CreditsCheckCallback import CreditsCheckCallback
from copyleaksSdk.models.callbacks.IndexOnlyCallback import IndexOnlyCallback
from copyleaksSdk.models.callbacks.NewResultCallback import NewResultCallback


class Callbacks_test(unittest.TestCase):

    def test_CompletedCallback(self):
        
        data = '''{"scannedDocument":{"totalWords":100,"totalExcluded":10,"credits":10,"creationTime":"0001-01-01T00:00:00","cachedVersion":"https://report/url"},"results":{"internet":[{"url":"https://internet1","id":"internet1","title":"internet1 title","introduction":"internet1","matchedWords":1,"comparison":"https://internet1/comperison/result"},{"url":"https://internet2","id":"internet2","title":"internet2 title","introduction":"internet2","matchedWords":2,"comparison":"https://internet2/comperison/result"}],"database":[{"scanId":"scanid1","id":"Database1","title":"Database1 title","introduction":"Database1","matchedWords":1,"comparison":"https://Database1/comperison/result"},{"scanId":"scanid2","id":"Database2","title":"Database2 title","introduction":"Database2","matchedWords":2,"comparison":"https://Database2/comperison/result"}],"batch":[{"scanId":"scanid1","id":"batch1","title":"batch1 title","introduction":"batch1","matchedWords":1,"comparison":"https://batch1/comperison/result"},{"scanId":"scanid2","id":"batch2","title":"batch2 title","introduction":"batch2","matchedWords":2,"comparison":"https://batch2/comperison/result"}],"score":{"identicalWords":10,"minorChangedWords":5,"relatedMeaningWords":3}},"status":4,"error":{"message":"Error meassage","code":1},"developerPayload":"payload"}'''
        json_data = json.loads(data)
        completed_callback = CompletedCallback(json_data)
        
        self.assertEqual(completed_callback.status, json_data['status'])
        self.assertEqual(completed_callback.developerPayload, json_data['developerPayload'])
        self.assertEqual(completed_callback.error.code, json_data['error']['code'])
        self.assertEqual(completed_callback.error.message, json_data['error']['message'])
    
        self.assertEqual(completed_callback.scannedDocument.totalWords, json_data['scannedDocument']['totalWords'])
        self.assertEqual(completed_callback.scannedDocument.totalExcluded, json_data['scannedDocument']['totalExcluded'])
        self.assertEqual(completed_callback.scannedDocument.credits, json_data['scannedDocument']['credits'])
        self.assertEqual(completed_callback.scannedDocument.creationTime, json_data['scannedDocument']['creationTime'])
        self.assertEqual(completed_callback.scannedDocument.cachedVersion, json_data['scannedDocument']['cachedVersion'])
    
        for idx, _ in enumerate(json_data['results']['internet']):
            self.assertEqual(completed_callback.results.internet[idx].url, json_data['results']['internet'][idx]['url'])
            self.assertEqual(completed_callback.results.internet[idx].id, json_data['results']['internet'][idx]['id'])
            self.assertEqual(completed_callback.results.internet[idx].title, json_data['results']['internet'][idx]['title'])
            self.assertEqual(completed_callback.results.internet[idx].introduction, json_data['results']['internet'][idx]['introduction'])
            self.assertEqual(completed_callback.results.internet[idx].matchedWords, json_data['results']['internet'][idx]['matchedWords'])
            self.assertEqual(completed_callback.results.internet[idx].comparison, json_data['results']['internet'][idx]['comparison'])
        for idx, _ in enumerate(json_data['results']['database']):
            self.assertEqual(completed_callback.results.database[idx].scanId, json_data['results']['database'][idx]['scanId'])
            self.assertEqual(completed_callback.results.database[idx].id, json_data['results']['database'][idx]['id'])
            self.assertEqual(completed_callback.results.database[idx].title, json_data['results']['database'][idx]['title'])
            self.assertEqual(completed_callback.results.database[idx].introduction, json_data['results']['database'][idx]['introduction'])
            self.assertEqual(completed_callback.results.database[idx].matchedWords, json_data['results']['database'][idx]['matchedWords'])
            self.assertEqual(completed_callback.results.database[idx].comparison, json_data['results']['database'][idx]['comparison'])
    
        for idx, _ in enumerate(json_data['results']['batch']):
            self.assertEqual(completed_callback.results.batch[idx].scanId, json_data['results']['batch'][idx]['scanId'])
            self.assertEqual(completed_callback.results.batch[idx].id, json_data['results']['batch'][idx]['id'])
            self.assertEqual(completed_callback.results.batch[idx].title, json_data['results']['batch'][idx]['title'])
            self.assertEqual(completed_callback.results.batch[idx].introduction, json_data['results']['batch'][idx]['introduction'])
            self.assertEqual(completed_callback.results.batch[idx].matchedWords, json_data['results']['batch'][idx]['matchedWords'])
            self.assertEqual(completed_callback.results.batch[idx].comparison, json_data['results']['batch'][idx]['comparison'])

        self.assertEqual(completed_callback.results.score.identicalWords, json_data['results']['score']['identicalWords'])
        self.assertEqual(completed_callback.results.score.minorChangedWords, json_data['results']['score']['minorChangedWords'])
        self.assertEqual(completed_callback.results.score.relatedMeaningWords, json_data['results']['score']['relatedMeaningWords'])

    def test_CreditsCheckCallback(self):
        data = '''{"status":4,"error":{"message":"Error meassage","code":1},"developerPayload":"payload"}'''
        json_data = json.loads(data)
        credits_calback = CreditsCheckCallback(json_data)
        self.assertEqual(credits_calback.status, json_data['status'])
        self.assertEqual(credits_calback.developerPayload, json_data['developerPayload'])
        self.assertEqual(credits_calback.error.code, json_data['error']['code'])
        self.assertEqual(credits_calback.error.message, json_data['error']['message'])
    
    def test_IndexOnlyCallback(self):
        data = '''{"status":4,"error":{"message":"Error meassage","code":1},"developerPayload":"payload"}'''
        json_data = json.loads(data)
        index_callback = IndexOnlyCallback(json_data)
        
        self.assertEqual(index_callback.status, json_data['status'])
        self.assertEqual(index_callback.developerPayload, json_data['developerPayload'])
        self.assertEqual(index_callback.error.code, json_data['error']['code'])
        self.assertEqual(index_callback.error.message, json_data['error']['message'])

    def test_NewResultCallback(self):
        data = '''{"internet":[{"url":"https://internet1","id":"internet1","title":"internet1 title","introduction":"internet1","matchedWords":1,"comparison":"https://internet1/comperison/result"},{"url":"https://internet2","id":"internet2","title":"internet2 title","introduction":"internet2","matchedWords":2,"comparison":"https://internet2/comperison/result"}],"database":[{"scanId":"scanid1","id":"Database1","title":"Database1 title","introduction":"Database1","matchedWords":1,"comparison":"https://Database1/comperison/result"},{"scanId":"scanid2","id":"Database2","title":"Database2 title","introduction":"Database2","matchedWords":2,"comparison":"https://Database2/comperison/result"}],"batch":[{"scanId":"scanid1","id":"batch1","title":"batch1 title","introduction":"batch1","matchedWords":1,"comparison":"https://batch1/comperison/result"},{"scanId":"scanid2","id":"batch2","title":"batch2 title","introduction":"batch2","matchedWords":2,"comparison":"https://batch2/comperison/result"}],"score":{"identicalWords":10,"minorChangedWords":5,"relatedMeaningWords":3}}'''
        json_data = json.loads(data)
        new_result_callback = NewResultCallback(json_data)
        
        for idx, _ in enumerate(json_data['internet']):
            self.assertEqual(new_result_callback.internet[idx].url, json_data['internet'][idx]['url'])
            self.assertEqual(new_result_callback.internet[idx].id, json_data['internet'][idx]['id'])
            self.assertEqual(new_result_callback.internet[idx].title, json_data['internet'][idx]['title'])
            self.assertEqual(new_result_callback.internet[idx].introduction, json_data['internet'][idx]['introduction'])
            self.assertEqual(new_result_callback.internet[idx].matchedWords, json_data['internet'][idx]['matchedWords'])
            self.assertEqual(new_result_callback.internet[idx].comparison, json_data['internet'][idx]['comparison'])
        for idx, _ in enumerate(json_data['database']):
            self.assertEqual(new_result_callback.database[idx].scanId, json_data['database'][idx]['scanId'])
            self.assertEqual(new_result_callback.database[idx].id, json_data['database'][idx]['id'])
            self.assertEqual(new_result_callback.database[idx].title, json_data['database'][idx]['title'])
            self.assertEqual(new_result_callback.database[idx].introduction, json_data['database'][idx]['introduction'])
            self.assertEqual(new_result_callback.database[idx].matchedWords, json_data['database'][idx]['matchedWords'])
            self.assertEqual(new_result_callback.database[idx].comparison, json_data['database'][idx]['comparison'])
    
        for idx, _ in enumerate(json_data['batch']):
            self.assertEqual(new_result_callback.batch[idx].scanId, json_data['batch'][idx]['scanId'])
            self.assertEqual(new_result_callback.batch[idx].id, json_data['batch'][idx]['id'])
            self.assertEqual(new_result_callback.batch[idx].title, json_data['batch'][idx]['title'])
            self.assertEqual(new_result_callback.batch[idx].introduction, json_data['batch'][idx]['introduction'])
            self.assertEqual(new_result_callback.batch[idx].matchedWords, json_data['batch'][idx]['matchedWords'])
            self.assertEqual(new_result_callback.batch[idx].comparison, json_data['batch'][idx]['comparison'])

        self.assertEqual(new_result_callback.score.identicalWords, json_data['score']['identicalWords'])
        self.assertEqual(new_result_callback.score.minorChangedWords, json_data['score']['minorChangedWords'])
        self.assertEqual(new_result_callback.score.relatedMeaningWords, json_data['score']['relatedMeaningWords'])
