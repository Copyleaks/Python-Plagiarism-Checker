'''
Unit tests for the shared HTTP layer: keep-alive session, timeouts, error mapping on every endpoint, read timeouts,
fork safety and no output on stdout. The read timeout test uses a local server on 127.0.0.1.
'''
import base64
import contextlib
import io
import os
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

import requests
from requests.adapters import HTTPAdapter

from copyleaks.copyleaks import Copyleaks
from copyleaks.exceptions.command_error import CommandError
from copyleaks.exceptions.rate_limit_error import RateLimitError
from copyleaks.exceptions.under_maintenance_error import UnderMaintenanceError
from copyleaks.helpers.copyleaks_http_client import CopyleaksHttpClient
from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionCreditsResponseModel import CopyleaksAiTextDetectionCreditsResponseModel
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionAsyncRequestModel import CopyleaksAiImageDetectionAsyncRequestModel
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionFileRequestModel import CopyleaksAiImageDetectionFileRequestModel
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionRequestModel import CopyleaksAiImageDetectionRequestModel
from copyleaks.models.ImagePlagiarism.Requests.CopyleaksImagePlagiarismRequestModel import CopyleaksImagePlagiarismRequestModel
from copyleaks.models.TextModeration.Requests.CopyleaksTextModerationLabel import CopyleaksTextModerationLabel
from copyleaks.models.TextModeration.Requests.CopyleaksTextModerationRequestModel import CopyleaksTextModerationRequestModel
from copyleaks.models.VideoDetection.Requests.CopyleaksAiVideoDetectionRequestModel import CopyleaksAiVideoDetectionRequestModel
from copyleaks.models.delete import Delete, DeleteScan
from copyleaks.models.export import Export
from copyleaks.models.start import Start
from copyleaks.models.submit.ai_detection_document import NaturalLanguageDocument
from copyleaks.models.submit.document import FileDocument, OcrFileDocument, UrlDocument
from copyleaks.models.submit.properties.scan_properties import ScanProperties
from copyleaks.models.submit.writing_assistant_document import WritingAssistantDocument

from http_fakes import AUTH_TOKEN, FakeResponse, HttpTestCase

TEXT = 'Lions are social animals, living in groups called prides. ' * 6
PNG = b'\x89PNG\r\n\x1a\n fake image bytes'


def _properties():
    properties = ScanProperties('https://example.com/webhook/{STATUS}')
    properties.set_sandbox(True)
    return properties


def all_endpoint_calls():
    '''(name, callable) for every public method that calls the API.'''
    file_doc = FileDocument(base64.b64encode(b'hello').decode('ascii'), 'a.txt')
    file_doc.set_properties(_properties())
    ocr_doc = OcrFileDocument(base64.b64encode(PNG).decode('ascii'), 'a.png')
    ocr_doc.set_properties(_properties())
    url_doc = UrlDocument()
    url_doc.set_url('https://example.com/')
    url_doc.set_properties(_properties())
    start = Start()
    start.set_trigger(['scan1'])
    delete = Delete()
    delete.set_scans([DeleteScan('scan1')])
    export = Export()
    export.set_completion_webhook('https://example.com/export-done')
    nl_doc = NaturalLanguageDocument(TEXT)
    nl_doc.set_sandbox(True)
    wa_doc = WritingAssistantDocument(TEXT)
    wa_doc.set_sandbox(True)
    moderation = CopyleaksTextModerationRequestModel(
        text=TEXT, sandbox=True, labels=[CopyleaksTextModerationLabel(id='toxic-v1')])
    image_json = CopyleaksAiImageDetectionRequestModel(
        base64=base64.b64encode(PNG).decode('ascii'), file_name='a.png', model='ai-image-1-ultra', sandbox=True)
    image_file = CopyleaksAiImageDetectionFileRequestModel(
        image=PNG, file_name='a.png', model='ai-image-1-ultra', sandbox=True)
    image_async = CopyleaksAiImageDetectionAsyncRequestModel(
        url='https://example.com/a.png', file_name='a.png', model='ai-image-1-ultra',
        webhooks={'url': 'https://example.com/webhook'}, sandbox=True)
    plagiarism = CopyleaksImagePlagiarismRequestModel(image=PNG, file_name='a.png', sandbox=True)
    video = CopyleaksAiVideoDetectionRequestModel(
        url='https://example.com/v.mp4', file_name='v.mp4', model='ai-video-1-pro',
        webhooks={'url': 'https://example.com/webhook'}, sandbox=True)
    T, S = AUTH_TOKEN, 'scan1'
    C = Copyleaks
    return [
        ('login', lambda: C.login('user@example.com', 'not-a-real-key')),
        ('submit_file', lambda: C.submit_file(T, S, file_doc)),
        ('submit_file_ocr', lambda: C.submit_file_ocr(T, S, ocr_doc)),
        ('submit_url', lambda: C.submit_url(T, S, url_doc)),
        ('export', lambda: C.export(T, S, 'export1', export)),
        ('start', lambda: C.start(T, start)),
        ('delete', lambda: C.delete(T, delete)),
        ('resend_webhook', lambda: C.resend_webhook(T, S)),
        ('credits_balance', lambda: C.credits_balance(T)),
        ('usages_history_csv', lambda: C.usages_history_csv(T, '01-09-2026', '07-09-2026')),
        ('release_notes', lambda: C.release_notes()),
        ('supported_file_types', lambda: C.supported_file_types()),
        ('supported_ai_text_detection_file_types', lambda: C.supported_ai_text_detection_file_types()),
        ('allowed_cross_languages', lambda: C.allowed_cross_languages()),
        ('ocr_supported_langauges', lambda: C.ocr_supported_langauges()),
        ('repository_info', lambda: C.repository_info(T, 'repo1')),
        ('AiDetectionClient.submit_natural_language', lambda: C.AiDetectionClient.submit_natural_language(T, S, nl_doc)),
        ('AiDetectionClient.credits_balance', lambda: C.AiDetectionClient.credits_balance(T)),
        ('WritingAssistantClient.submit_text', lambda: C.WritingAssistantClient.submit_text(T, S, wa_doc)),
        ('WritingAssistantClient.get_correction_types', lambda: C.WritingAssistantClient.get_correction_types('en')),
        ('TextModerationClient.submit_text', lambda: C.TextModerationClient.submit_text(T, S, moderation)),
        ('ImageDetectionClient.submit', lambda: C.ImageDetectionClient.submit(T, S, image_json)),
        ('ImageDetectionClient.submit_file', lambda: C.ImageDetectionClient.submit_file(T, S, image_file)),
        ('ImageDetectionClient.submit_async', lambda: C.ImageDetectionClient.submit_async(T, S, image_async)),
        ('ImagePlagiarismClient.check', lambda: C.ImagePlagiarismClient.check(T, S, plagiarism)),
        ('VideoDetectionClient.submit', lambda: C.VideoDetectionClient.submit(T, S, video)),
    ]


class SessionTest(unittest.TestCase):

    def setUp(self):
        CopyleaksHttpClient.set_session(None)
        self.addCleanup(CopyleaksHttpClient.set_session, None)

    def test_one_shared_session_with_keep_alive_pool(self):
        session = Copyleaks.get_session()
        self.assertIsInstance(session, requests.Session)
        self.assertIs(Copyleaks.get_session(), session)
        adapter = session.get_adapter('https://api.copyleaks.com/v3/scans/credits')
        self.assertIsInstance(adapter, HTTPAdapter)
        self.assertGreaterEqual(adapter._pool_maxsize, 10)
        self.assertIs(session.get_adapter('https://id.copyleaks.com/v3/account/login/api'), adapter)

    def test_default_session_retries_only_connection_errors(self):
        retries = Copyleaks.get_session().get_adapter('https://api.copyleaks.com').max_retries
        self.assertIs(retries.read, False)
        self.assertEqual(retries.status, 0)
        self.assertGreater(retries.connect, 0)

    @unittest.skipUnless(hasattr(os, 'fork'), 'needs os.fork')
    def test_forked_child_gets_a_new_default_session(self):
        parent = Copyleaks.get_session()
        self.assertIs(self._in_forked_child(lambda: Copyleaks.get_session() is not parent), True)
        own = requests.Session()
        Copyleaks.set_session(own)
        self.assertIs(self._in_forked_child(lambda: Copyleaks.get_session() is own), True)

    @staticmethod
    def _in_forked_child(check):
        '''Run `check` in a forked child and return its boolean result (None if the child failed).'''
        read_end, write_end = os.pipe()
        pid = os.fork()
        if pid == 0:
            try:
                os.close(read_end)
                os.write(write_end, b'1' if check() else b'0')
            finally:
                os._exit(0)
        os.close(write_end)
        with os.fdopen(read_end, 'rb') as pipe:
            result = pipe.read()
        os.waitpid(pid, 0)
        return {b'1': True, b'0': False}.get(result)

    def test_every_endpoint_uses_the_shared_session(self):
        session = Copyleaks.get_session()
        response = FakeResponse(200, {})
        with patch.object(session, 'request', return_value=response) as request, \
                patch('requests.request', side_effect=AssertionError('module-level requests used')):
            for name, call in all_endpoint_calls():
                request.reset_mock()
                try:
                    call()
                except Exception:  # some typed responses do not accept the empty test body
                    pass
                self.assertEqual(request.call_count, 1, name)

    def test_set_session_injects_and_resets(self):
        own = requests.Session()
        Copyleaks.set_session(own)
        self.assertIs(Copyleaks.get_session(), own)
        Copyleaks.set_session(None)
        self.assertIsNot(Copyleaks.get_session(), own)

    def test_set_session_rejects_other_objects(self):
        with self.assertRaises(TypeError):
            Copyleaks.set_session('not a session')


class TimeoutTest(HttpTestCase):

    def test_default_timeout_is_sent_on_every_call(self):
        self.assertEqual(Copyleaks.get_timeout(), (10, 180))
        for name, call in all_endpoint_calls():
            try:
                call()
            except Exception:
                pass
            self.assertEqual(self.session.last.timeout, (10, 180), name)

    def test_set_timeout_changes_the_default(self):
        Copyleaks.set_timeout(30)
        Copyleaks.release_notes()
        self.assertEqual(self.session.last.timeout, 30)
        Copyleaks.set_timeout((3, 60))
        Copyleaks.credits_balance(AUTH_TOKEN)
        self.assertEqual(self.session.last.timeout, (3, 60))

    def test_per_call_timeout_overrides_the_default(self):
        Copyleaks.set_timeout(30)
        Copyleaks.release_notes(timeout=5)
        self.assertEqual(self.session.last.timeout, 5)
        Copyleaks.AiDetectionClient.credits_balance(AUTH_TOKEN, timeout=(1, 2))
        self.assertEqual(self.session.last.timeout, (1, 2))

    def test_timeout_none_disables_it(self):
        Copyleaks.set_timeout(None)
        Copyleaks.release_notes()
        self.assertIsNone(self.session.last.timeout)

    def test_invalid_timeouts_are_rejected(self):
        for bad in (0, -1, 'ten', (1, 2, 3), True):
            with self.assertRaises(ValueError, msg=repr(bad)):
                Copyleaks.set_timeout(bad)
        with self.assertRaises(ValueError):
            Copyleaks.release_notes(timeout=-5)


class _SlowHandler(BaseHTTPRequestHandler):
    def _respond_late(self):
        length = int(self.headers.get('Content-Length') or 0)
        if length:
            self.rfile.read(length)
        time.sleep(0.5)
        try:
            self.send_response(200)
            self.send_header('Content-Length', '2')
            self.end_headers()
            self.wfile.write(b'{}')
        except OSError:  # the client has already given up
            pass

    do_GET = do_PUT = do_POST = _respond_late

    def log_message(self, *args):
        pass


class ReadTimeoutTest(unittest.TestCase):
    '''A real local server that answers after the read timeout, through the SDK's default session.'''

    def setUp(self):
        CopyleaksHttpClient.set_session(None)
        self.addCleanup(CopyleaksHttpClient.set_session, None)
        server = ThreadingHTTPServer(('127.0.0.1', 0), _SlowHandler)
        server.daemon_threads = True
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        self.url = 'http://127.0.0.1:%d/x' % server.server_address[1]

    def test_read_timeout_raises_timeout_on_every_method(self):
        for method in ('GET', 'PUT', 'POST'):
            data = None if method == 'GET' else b'{}'
            with self.assertRaises(requests.exceptions.Timeout, msg=method):
                CopyleaksHttpClient.request(method, self.url, headers={}, data=data, timeout=(2, 0.1))


class ErrorMappingTest(HttpTestCase):

    def assert_maps(self, status, error_type, headers=None):
        for name, call in all_endpoint_calls():
            self.respond({'error': 'x'}, status_code=status, headers=headers)
            with self.assertRaises(error_type, msg=name) as ctx:
                call()
            self.assertEqual(ctx.exception.get_response().status_code, status, name)
        return ctx.exception

    def test_429_raises_rate_limit_error_on_every_call(self):
        error = self.assert_maps(429, RateLimitError, headers={'Retry-After': '120'})
        self.assertEqual(error.retry_after, 120)
        self.assertEqual(error.status_code, 429)

    def test_503_raises_under_maintenance_error_on_every_call(self):
        error = self.assert_maps(503, UnderMaintenanceError)
        self.assertIsNone(error.retry_after)

    def test_other_errors_raise_command_error_with_the_response(self):
        error = self.assert_maps(400, CommandError)
        self.assertNotIsInstance(error, RateLimitError)
        self.assertEqual(error.status_code, 400)
        self.assertIn('HTTP 400', str(error))

    def test_rate_limit_error_is_still_caught_as_command_error(self):
        # Before 6.0.0 most calls raised CommandError on HTTP 429; that code keeps working.
        self.respond({'error': 'x'}, status_code=429)
        with self.assertRaises(CommandError):
            Copyleaks.supported_file_types()

    def test_correction_types_error_carries_the_response_object(self):
        self.respond({'error': 'bad language'}, status_code=400)
        with self.assertRaises(CommandError) as ctx:
            Copyleaks.WritingAssistantClient.get_correction_types('xx')
        self.assertEqual(ctx.exception.get_response().status_code, 400)

    def test_errors_print_nothing(self):
        image = CopyleaksAiImageDetectionRequestModel(
            base64=base64.b64encode(PNG).decode('ascii'), file_name='a.png', model='ai-image-1-ultra')
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            for status in (400, 503):
                self.respond({'error': 'x'}, status_code=status)
                with self.assertRaises(Exception):
                    Copyleaks.ImageDetectionClient.submit(AUTH_TOKEN, 'scan1', image)
        self.assertEqual(out.getvalue(), '')

    def test_errors_are_logged_at_debug_level(self):
        self.respond({'error': 'details'}, status_code=400)
        with self.assertLogs('copyleaks', level='DEBUG') as logs:
            with self.assertRaises(CommandError):
                Copyleaks.release_notes()
        self.assertIn('HTTP 400', logs.output[0])
        self.assertNotIn('test-token', ''.join(logs.output))


class ExceptionsTest(unittest.TestCase):

    def test_exceptions_still_construct_without_arguments(self):
        self.assertIsNone(RateLimitError().get_response())
        self.assertIsNone(UnderMaintenanceError().get_response())
        self.assertIsNone(RateLimitError().retry_after)

    def test_retry_after_parsing(self):
        self.assertEqual(RateLimitError(FakeResponse(429, headers={'Retry-After': '7'})).retry_after, 7)
        self.assertIsNone(RateLimitError(FakeResponse(429, headers={'Retry-After': 'soon'})).retry_after)

    def test_command_error_message(self):
        self.assertEqual(str(CommandError(FakeResponse(404, {'message': 'nope'}))), 'HTTP 404: {"message": "nope"}')
        self.assertEqual(str(CommandError(b'raw body')), 'raw body')

    def test_response_errors_share_one_implementation(self):
        for name in ('get_response', 'status_code', 'retry_after', '__str__'):
            self.assertIs(getattr(UnderMaintenanceError, name), getattr(CommandError, name), name)
            self.assertIs(getattr(RateLimitError, name), getattr(CommandError, name), name)
        maintenance = UnderMaintenanceError(FakeResponse(503, headers={'Retry-After': '30'}))
        self.assertEqual((maintenance.status_code, maintenance.retry_after, str(maintenance)), (503, 30, 'HTTP 503'))
        self.assertEqual((str(UnderMaintenanceError()), str(RateLimitError()), str(CommandError(None))),
                         ('Under maintenance', 'Too many requests', ''))

    def test_under_maintenance_error_is_still_not_a_command_error(self):
        # As in 5.x: `except CommandError` does not catch HTTP 503, so the order of existing except clauses still works.
        self.assertFalse(issubclass(UnderMaintenanceError, CommandError))
        self.assertTrue(issubclass(RateLimitError, CommandError))


class ExceptClauseTest(HttpTestCase):

    def test_each_except_clause_catches_its_status(self):
        for status, expected in ((503, 'maintenance'), (429, 'rate limit'), (400, 'command')):
            self.respond({'error': 'x'}, status_code=status)
            try:
                Copyleaks.credits_balance(AUTH_TOKEN)
                caught = 'nothing'
            except CommandError as e:
                caught = 'rate limit' if isinstance(e, RateLimitError) else 'command'
            except UnderMaintenanceError:
                caught = 'maintenance'
            self.assertEqual(caught, expected, status)


class SendHelperTest(HttpTestCase):
    '''`CopyleaksHttpClient.send`: the one place that checks the token, builds headers and body, and parses.'''

    def test_every_endpoint_calls_send_once(self):
        with patch.object(CopyleaksHttpClient, 'send', wraps=CopyleaksHttpClient.send) as send:
            for name, call in all_endpoint_calls():
                send.reset_mock()
                try:
                    call()
                except Exception:  # some typed responses do not accept the empty test body
                    pass
                self.assertEqual(send.call_count, 1, name)

    def test_json_body_of_plain_objects_and_pydantic_models(self):
        doc = NaturalLanguageDocument(TEXT)
        CopyleaksHttpClient.send('POST', 'https://api.example.com/a', auth_token=AUTH_TOKEN, json=doc)
        self.assertEqual(self.session.last.data, doc.toJSON().encode('utf-8'))
        moderation = CopyleaksTextModerationRequestModel(text=TEXT, labels=[CopyleaksTextModerationLabel(id='a')])
        CopyleaksHttpClient.send('POST', 'https://api.example.com/b', auth_token=AUTH_TOKEN, json=moderation)
        self.assertEqual(self.session.last.data, moderation.model_dump_json(by_alias=True, exclude_none=True).encode())
        for call in self.session.calls:
            self.assertEqual(call.headers, {'User-Agent': 'python-sdk/3.0', 'Content-Type': 'application/json',
                                            'Authorization': 'Bearer test-token'})

    def test_headers_without_body_and_without_token(self):
        CopyleaksHttpClient.send('GET', 'https://api.example.com/a')
        self.assertEqual(self.session.last.headers, {'User-Agent': 'python-sdk/3.0'})
        CopyleaksHttpClient.send('GET', 'https://api.example.com/b', auth_token=AUTH_TOKEN,
                                 content_type='application/json')
        self.assertEqual(self.session.last.headers, {'User-Agent': 'python-sdk/3.0', 'Content-Type': 'application/json',
                                                     'Authorization': 'Bearer test-token'})
        CopyleaksHttpClient.send('POST', 'https://api.example.com/c', auth_token=AUTH_TOKEN, form={'a': '1'},
                                 files={'image': ('a.png', PNG, 'image/png')})
        call = self.session.last
        self.assertEqual(call.headers, {'User-Agent': 'python-sdk/3.0', 'Authorization': 'Bearer test-token'})
        self.assertEqual((call.data, call.files), ({'a': '1'}, {'image': ('a.png', PNG, 'image/png')}))

    def test_token_is_checked_before_the_request(self):
        from copyleaks.exceptions.auth_expired_error import AuthExipredError
        with self.assertRaises(AuthExipredError):
            CopyleaksHttpClient.send('GET', 'https://api.example.com/a',
                                     auth_token={'access_token': 'x', '.expires': '2000-01-01T00:00:00Z'})
        with self.assertRaises((AssertionError, TypeError)):  # TypeError when Python runs with -O
            CopyleaksHttpClient.send('GET', 'https://api.example.com/a', auth_token=None)
        self.assertEqual(self.session.calls, [])

    def test_returns_the_parsed_model_or_the_response(self):
        self.respond({'credits': 5})
        response = CopyleaksHttpClient.send('GET', 'https://api.example.com/a')
        self.assertEqual(response.json(), {'credits': 5})
        self.respond({'credits': 5})
        model = CopyleaksHttpClient.send('GET', 'https://api.example.com/a',
                                         response_model=CopyleaksAiTextDetectionCreditsResponseModel)
        self.assertIsInstance(model, CopyleaksAiTextDetectionCreditsResponseModel)
        self.assertEqual(model.credits, 5)
        self.assertEqual(self.session.last.timeout, (10, 180))


if __name__ == '__main__':
    unittest.main()
