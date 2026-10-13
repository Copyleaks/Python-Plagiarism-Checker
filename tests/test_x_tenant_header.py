'''
Unit tests for the `x-tenant` header (BAC-6326).
The HTTP layer (`requests`) is mocked, so no network calls are made.

Run from the repository root:
    python -m unittest discover -s tests -v
'''

import inspect
import unittest
from unittest.mock import MagicMock, patch

from copyleaks.consts import Consts
from copyleaks.copyleaks import Copyleaks
from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper

AUTH_TOKEN = {'access_token': 'token', '.expires': '2999-01-01T00:00:00Z'}
SUBMISSION = MagicMock()

# (endpoint name, HTTP verb used by the endpoint, call taking the optional x_tenant keyword)
ENDPOINTS = [
    ('login', 'post', lambda **kw: Copyleaks.login('user@example.com', 'key', **kw)),
    ('submit_file', 'put', lambda **kw: Copyleaks.submit_file(AUTH_TOKEN, 'scan-id', SUBMISSION, **kw)),
    ('submit_file_ocr', 'put', lambda **kw: Copyleaks.submit_file_ocr(AUTH_TOKEN, 'scan-id', SUBMISSION, **kw)),
    ('submit_url', 'put', lambda **kw: Copyleaks.submit_url(AUTH_TOKEN, 'scan-id', SUBMISSION, **kw)),
    ('export', 'post', lambda **kw: Copyleaks.export(AUTH_TOKEN, 'scan-id', 'export-id', SUBMISSION, **kw)),
    ('start', 'patch', lambda **kw: Copyleaks.start(AUTH_TOKEN, SUBMISSION, **kw)),
    ('delete', 'patch', lambda **kw: Copyleaks.delete(AUTH_TOKEN, SUBMISSION, **kw)),
    ('resend_webhook', 'post', lambda **kw: Copyleaks.resend_webhook(AUTH_TOKEN, 'scan-id', **kw)),
    ('credits_balance', 'get', lambda **kw: Copyleaks.credits_balance(AUTH_TOKEN, **kw)),
    ('usages_history_csv', 'get', lambda **kw: Copyleaks.usages_history_csv(AUTH_TOKEN, '01-01-2024', '31-01-2024', **kw)),
    ('release_notes', 'get', lambda **kw: Copyleaks.release_notes(**kw)),
    ('supported_file_types', 'get', lambda **kw: Copyleaks.supported_file_types(**kw)),
    ('ocr_supported_langauges', 'get', lambda **kw: Copyleaks.ocr_supported_langauges(**kw)),
    ('AiDetectionClient.submit_natural_language', 'post',
     lambda **kw: Copyleaks.AiDetectionClient.submit_natural_language(AUTH_TOKEN, 'scan-id', SUBMISSION, **kw)),
    ('WritingAssistantClient.submit_text', 'post',
     lambda **kw: Copyleaks.WritingAssistantClient.submit_text(AUTH_TOKEN, 'scan-id', SUBMISSION, **kw)),
    ('WritingAssistantClient.get_correction_types', 'get',
     lambda **kw: Copyleaks.WritingAssistantClient.get_correction_types('en', **kw)),
    ('TextModerationClient.submit_text', 'post',
     lambda **kw: Copyleaks.TextModerationClient.submit_text(AUTH_TOKEN, 'scan-id', SUBMISSION, **kw)),
    ('ImageDetectionClient.submit', 'post',
     lambda **kw: Copyleaks.ImageDetectionClient.submit(AUTH_TOKEN, 'scan-id', SUBMISSION, **kw)),
]


class XTenantHeaderTest(unittest.TestCase):

    def setUp(self):
        self.saved_tenant = Consts.TENANT
        Consts.TENANT = None

        response = MagicMock(ok=True, status_code=200)
        response.json.return_value = {}
        self.http = {}
        for verb in ('get', 'post', 'put', 'patch', 'delete'):
            patcher = patch(f'requests.{verb}', return_value=response)
            self.http[verb] = patcher.start()
            self.addCleanup(patcher.stop)

        # These clients parse the response into pydantic models; the response content is irrelevant here.
        for target in (
            'copyleaks.clients.TextModerationClient.CopyleaksTextModerationResponseModel',
            'copyleaks.clients.AiImageDetectionClient.CopyleaksAiImageDetectionResponseModel',
        ):
            patcher = patch(target)
            patcher.start()
            self.addCleanup(patcher.stop)

    def tearDown(self):
        Consts.TENANT = self.saved_tenant

    def sent_headers(self, verb):
        mock = self.http[verb]
        mock.assert_called_once()
        headers = mock.call_args.kwargs['headers']
        mock.reset_mock()
        return headers

    def test_process_wide_tenant_is_sent(self):
        Copyleaks.set_tenant('tenant-a')
        for name, verb, call in ENDPOINTS:
            with self.subTest(endpoint=name):
                call()
                self.assertEqual(self.sent_headers(verb).get('x-tenant'), 'tenant-a')

    def test_per_call_tenant_overrides_process_wide(self):
        Copyleaks.set_tenant('tenant-a')
        for name, verb, call in ENDPOINTS:
            with self.subTest(endpoint=name):
                call(x_tenant='tenant-b')
                self.assertEqual(self.sent_headers(verb).get('x-tenant'), 'tenant-b')

    def test_per_call_tenant_without_process_wide(self):
        for name, verb, call in ENDPOINTS:
            with self.subTest(endpoint=name):
                call(x_tenant='tenant-b')
                self.assertEqual(self.sent_headers(verb).get('x-tenant'), 'tenant-b')

    def test_no_header_when_tenant_not_set(self):
        for name, verb, call in ENDPOINTS:
            with self.subTest(endpoint=name):
                call()
                headers = self.sent_headers(verb)
                self.assertNotIn('x-tenant', headers)
                self.assertIn('User-Agent', headers)

    def test_set_tenant_none_stops_sending_header(self):
        Copyleaks.set_tenant('tenant-a')
        Copyleaks.set_tenant(None)
        Copyleaks.release_notes()
        self.assertNotIn('x-tenant', self.sent_headers('get'))

    def test_empty_per_call_tenant_omits_header(self):
        Consts.TENANT = 'tenant-a'
        headers = {}
        CopyleaksClientHelper.add_tenant_header(headers, '')
        self.assertNotIn('x-tenant', headers)


class XTenantSignatureGuardTest(unittest.TestCase):
    '''Fails when a public SDK method is added without the optional `x_tenant` parameter.'''

    # Public methods that send no request and so take no `x_tenant`. Changing this set needs review.
    EXEMPT = {'set_identity_uri', 'set_api_uri', 'set_tenant', 'verify_auth_token'}

    def test_every_public_method_ends_with_optional_x_tenant(self):
        classes = [
            Copyleaks,
            Copyleaks.AiDetectionClient,
            Copyleaks.WritingAssistantClient,
            Copyleaks.TextModerationClient,
            Copyleaks.ImageDetectionClient,
        ]
        exempt_found = set()
        for cls in classes:
            for name, fn in inspect.getmembers(cls, inspect.isfunction):
                if name.startswith('_'):
                    continue
                if name.startswith('set_') or name == 'verify_auth_token':
                    exempt_found.add(name)
                    continue
                with self.subTest(method=f'{cls.__name__}.{name}'):
                    params = list(inspect.signature(fn).parameters.values())
                    last = params[-1] if params else None
                    self.assertTrue(last is not None and last.name == 'x_tenant' and last.default is None,
                                    f'{cls.__name__}.{name} must end with x_tenant=None')

        self.assertEqual(exempt_found, self.EXEMPT,
                         'The set of methods exempt from x_tenant changed; review it and update EXEMPT.')


if __name__ == '__main__':
    unittest.main()
