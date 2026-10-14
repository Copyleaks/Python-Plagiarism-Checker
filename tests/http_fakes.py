'''
Test helpers: a fake `requests.Session` that records every request and returns canned responses,
so the unit tests make no network calls.
'''
import json
import unittest

import requests

from copyleaks.helpers.copyleaks_http_client import CopyleaksHttpClient

AUTH_TOKEN = {'access_token': 'test-token', '.expires': '2999-01-01T00:00:00Z'}
API = 'https://api.copyleaks.com'
IDENTITY = 'https://id.copyleaks.com'


class FakeResponse:
    def __init__(self, status_code=200, body=None, headers=None, content=None):
        self.status_code = status_code
        self.headers = requests.structures.CaseInsensitiveDict(headers or {})
        if content is not None:
            self.content = content
        else:
            self.content = b'' if body is None else json.dumps(body).encode('utf-8')
        self._body = body

    @property
    def ok(self):
        return 200 <= self.status_code < 400

    @property
    def text(self):
        return self.content.decode('utf-8', 'replace')

    def json(self):
        if self._body is None:
            return json.loads(self.text or 'null')
        return json.loads(json.dumps(self._body))


class Call:
    def __init__(self, method, url, kwargs):
        self.method = method
        self.url = url
        self.headers = dict(kwargs.get('headers') or {})
        self.data = kwargs.get('data')
        self.files = kwargs.get('files')
        self.timeout = kwargs.get('timeout')
        self.kwargs = kwargs

    def json(self):
        data = self.data
        if isinstance(data, (bytes, bytearray)):
            data = data.decode('utf-8')
        return json.loads(data)

    def prepared(self):
        '''The request as `requests` would put it on the wire.'''
        return requests.Request(self.method, self.url, headers=self.headers, data=self.data, files=self.files).prepare()


class FakeSession:
    def __init__(self):
        self.calls = []
        self.responses = []
        self.default = FakeResponse(200, {})

    def respond(self, *responses):
        self.responses.extend(responses)
        return self

    def request(self, method, url, **kwargs):
        self.calls.append(Call(method, url, kwargs))
        if self.responses:
            return self.responses.pop(0)
        return self.default

    @property
    def last(self):
        return self.calls[-1]


class HttpTestCase(unittest.TestCase):
    '''Installs a fresh FakeSession as the SDK session for each test, and restores the SDK defaults after.'''

    def setUp(self):
        super().setUp()
        self.session = FakeSession()
        CopyleaksHttpClient.set_session(self.session)
        self.addCleanup(CopyleaksHttpClient.set_session, None)
        self.addCleanup(CopyleaksHttpClient.set_timeout, CopyleaksHttpClient.DEFAULT_TIMEOUT)

    def respond(self, body=None, status_code=200, headers=None, content=None):
        self.session.respond(FakeResponse(status_code, body, headers, content))

    def assertCall(self, method, url, auth=True, content_type='application/json'):
        call = self.session.last
        self.assertEqual(call.method, method)
        self.assertEqual(call.url, url)
        self.assertEqual(call.headers.get('User-Agent'), 'python-sdk/3.0')
        if auth:
            self.assertEqual(call.headers.get('Authorization'), 'Bearer test-token')
        else:
            self.assertNotIn('Authorization', call.headers)
        if content_type:
            self.assertEqual(call.headers.get('Content-Type'), content_type)
        else:
            self.assertNotIn('Content-Type', call.headers)
        return call
