'''
Unit tests for every API call: exact HTTP method, URL, headers and body. No network calls are made.
Run all the tests from the repository root: python -m unittest discover -s tests -v
'''
import base64
import io
import json
import unittest

from copyleaks.copyleaks import Copyleaks
from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionCreditsResponseModel import CopyleaksAiTextDetectionCreditsResponseModel
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionAsyncRequestModel import CopyleaksAiImageDetectionAsyncRequestModel
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionFileRequestModel import CopyleaksAiImageDetectionFileRequestModel
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionRequestModel import CopyleaksAiImageDetectionRequestModel
from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionResponseModel import CopyleaksAiImageDetectionResponseModel
from copyleaks.models.ImagePlagiarism.Requests.CopyleaksImagePlagiarismRequestModel import CopyleaksImagePlagiarismRequestModel
from copyleaks.models.ImagePlagiarism.Responses.CopyleaksImagePlagiarismResponseModel import CopyleaksImagePlagiarismResponseModel
from copyleaks.models.Miscellaneous.Responses.CopyleaksAllowedCrossLanguagesResponseModel import CopyleaksAllowedCrossLanguagesResponseModel
from copyleaks.models.Miscellaneous.Responses.CopyleaksSupportedAiTextDetectionFileTypesResponseModel import CopyleaksSupportedAiTextDetectionFileTypesResponseModel
from copyleaks.models.PrivateCloudHub.Responses.CopyleaksRepositoryInfoResponseModel import CopyleaksRepositoryInfoResponseModel
from copyleaks.models.TextModeration.Requests.CopyleaksTextModerationLabel import CopyleaksTextModerationLabel
from copyleaks.models.TextModeration.Requests.CopyleaksTextModerationRequestModel import CopyleaksTextModerationRequestModel
from copyleaks.models.VideoDetection.Requests.CopyleaksAiVideoDetectionRequestModel import CopyleaksAiVideoDetectionRequestModel
from copyleaks.models.constants.CopyleaksAiImageDetectionModels import CopyleaksAiImageDetectionModels
from copyleaks.models.constants.CopyleaksAiImageMaskTypes import CopyleaksAiImageMaskTypes
from copyleaks.models.constants.CopyleaksAiVideoDetectionModels import CopyleaksAiVideoDetectionModels
from copyleaks.models.delete import Delete, DeleteScan
from copyleaks.models.export import Export, ExportAiDetection, ExportCrawledVersion, ExportOverview, ExportPdf, ExportResult, ExportWritingFeedback
from copyleaks.models.start import Start, StartErrorHandling
from copyleaks.models.submit.ai_detection_document import NaturalLanguageDocument
from copyleaks.models.submit.document import FileDocument, OcrFileDocument, UrlDocument
from copyleaks.models.submit.properties.scan_properties import ScanProperties
from copyleaks.models.submit.score_weights import ScoreWeights
from copyleaks.models.submit.writing_assistant_document import WritingAssistantDocument

from http_fakes import API, AUTH_TOKEN, IDENTITY, HttpTestCase

TEXT = 'Lions are social animals, living in groups called prides. ' * 6
PNG = b'\x89PNG\r\n\x1a\n fake image bytes'
WEBHOOK = 'https://example.com/webhook/{STATUS}'


def properties():
    p = ScanProperties(WEBHOOK)
    p.set_sandbox(True)
    return p


class AuthenticityEndpointsTest(HttpTestCase):

    def test_login(self):
        self.respond({'access_token': 'abc', '.expires': '2999-01-01T00:00:00Z'})
        token = Copyleaks.login('user@example.com', 'my-key')
        call = self.assertCall('POST', f'{IDENTITY}/v3/account/login/api', auth=False)
        self.assertEqual(call.json(), {'email': 'user@example.com', 'key': 'my-key'})
        self.assertEqual(token['access_token'], 'abc')

    def test_submit_file(self):
        doc = FileDocument('aGVsbG8=', 'a.txt')
        doc.set_properties(properties())
        self.assertIsNone(Copyleaks.submit_file(AUTH_TOKEN, 'scan1', doc))
        call = self.assertCall('PUT', f'{API}/v3/scans/submit/file/scan1')
        self.assertEqual(call.json(), {'base64': 'aGVsbG8=', 'filename': 'a.txt', 'properties': {
            'webhooks': {'status': WEBHOOK}, 'sandbox': True}})
        self.assertIsInstance(call.data, bytes)
        self.assertNotIn(b'\n', call.data)  # compact JSON
        self.assertNotIn(b', ', call.data)

    def test_submit_file_ocr(self):
        doc = OcrFileDocument('aW1hZ2U=', 'a.png')
        doc.set_language('en')
        doc.set_properties(properties())
        Copyleaks.submit_file_ocr(AUTH_TOKEN, 'scan1', doc)
        call = self.assertCall('PUT', f'{API}/v3/scans/submit/ocr/scan1')
        self.assertEqual(call.json()['langCode'], 'en')

    def test_submit_url_with_verb_and_headers(self):
        doc = UrlDocument()
        doc.set_url('https://example.com/private')
        doc.set_verb('post')
        doc.set_headers([['Authorization', 'Bearer abc'], ('Set-Cookie', 'a=b')])
        doc.set_properties(properties())
        Copyleaks.submit_url(AUTH_TOKEN, 'scan1', doc)
        call = self.assertCall('PUT', f'{API}/v3/scans/submit/url/scan1')
        body = call.json()
        self.assertEqual(body['url'], 'https://example.com/private')
        self.assertEqual(body['verb'], 'POST')
        self.assertEqual(body['headers'], [['Authorization', 'Bearer abc'], ['Set-Cookie', 'a=b']])

    def test_export_with_new_targets_and_webhook_headers(self):
        model = Export()
        model.set_completion_webhook('https://example.com/export-done')
        model.set_completion_webhook_headers([['X-Key', 'v']])
        model.set_max_retries(3)
        model.set_developer_payload('payload')
        targets = {}
        for name, cls, setter in (('pdfReport', ExportPdf, model.set_pdf_report),
                                  ('crawledVersion', ExportCrawledVersion, model.set_crawled_version),
                                  ('aiDetection', ExportAiDetection, model.set_ai_detection),
                                  ('writingFeedback', ExportWritingFeedback, model.set_writing_feedback),
                                  ('overview', ExportOverview, model.set_overview)):
            item = cls()
            item.set_endpoint(f'https://example.com/export/{name}')
            item.set_verb('POST')
            item.set_headers([['h', 'v']])
            setter(item)
            targets[name] = {'endpoint': f'https://example.com/export/{name}', 'verb': 'POST', 'headers': [['h', 'v']]}
        result = ExportResult()
        result.set_id('result-1')
        result.set_endpoint('https://example.com/export/result-1')
        result.set_verb('POST')
        model.set_results([result])

        self.assertIsNone(Copyleaks.export(AUTH_TOKEN, 'scan1', 'export1', model))
        call = self.assertCall('POST', f'{API}/v3/downloads/scan1/export/export1')
        body = call.json()
        self.assertEqual(body['completionWebhook'], 'https://example.com/export-done')
        self.assertEqual(body['completionWebhookHeaders'], [['X-Key', 'v']])
        self.assertEqual(body['maxRetries'], 3)
        self.assertEqual(body['developerPayload'], 'payload')
        for name, expected in targets.items():
            self.assertEqual(body[name], expected, name)
        self.assertEqual(body['results'], [{'id': 'result-1', 'endpoint': 'https://example.com/export/result-1', 'verb': 'POST'}])

    def test_export_without_results_or_crawled_version(self):
        model = Export()
        model.set_completion_webhook('https://example.com/export-done')
        pdf = ExportPdf()
        pdf.set_endpoint('https://example.com/pdf')
        pdf.set_verb('POST')
        model.set_pdf_report(pdf)
        Copyleaks.export(AUTH_TOKEN, 'scan1', 'export1', model)
        body = self.session.last.json()
        self.assertEqual(set(body), {'completionWebhook', 'pdfReport'})

    def test_start(self):
        model = Start()
        model.set_trigger(['scan1', 'scan2'])
        model.set_error_handling(StartErrorHandling.Ignore)
        self.respond({'success': [{'id': 'scan1'}], 'failed': []})
        response = Copyleaks.start(AUTH_TOKEN, model)
        call = self.assertCall('PATCH', f'{API}/v3/scans/start')
        self.assertEqual(call.json(), {'trigger': ['scan1', 'scan2'], 'errorHandling': 1})
        self.assertEqual(response['success'], [{'id': 'scan1'}])

    def test_delete_with_headers(self):
        model = Delete()
        model.set_scans([DeleteScan('scan1')])
        model.set_purge(True)
        model.set_completion_webhook('https://example.com/deleted')
        model.set_headers([['X-Key', 'v']])
        Copyleaks.delete(AUTH_TOKEN, model)
        call = self.assertCall('PATCH', f'{API}/v3.1/scans/delete')
        self.assertEqual(call.json(), {'scans': [{'id': 'scan1'}], 'purge': True,
                                       'completionWebhook': 'https://example.com/deleted', 'headers': [['X-Key', 'v']]})
        self.assertIs(model.get_purge(), True)

    def test_resend_webhook(self):
        Copyleaks.resend_webhook(AUTH_TOKEN, 'scan1')
        call = self.assertCall('POST', f'{API}/v3/scans/scan1/webhooks/resend')
        self.assertIsNone(call.data)

    def test_credits_balance(self):
        self.respond({'Amount': 42})
        self.assertEqual(Copyleaks.credits_balance(AUTH_TOKEN), {'Amount': 42})
        self.assertCall('GET', f'{API}/v3/scans/credits', content_type=None)

    def test_usages_history_csv(self):
        self.respond(content=b'a,b\n1,2\n')
        self.assertEqual(Copyleaks.usages_history_csv(AUTH_TOKEN, '01-09-2026', '07-09-2026'), b'a,b\n1,2\n')
        self.assertCall('GET', f'{API}/v3/scans/usages/history?start=01-09-2026&end=07-09-2026')

    def test_repository_info(self):
        body = {'id': 'repo-1', 'name': 'Hub', 'description': 'd', 'permission': 4, 'status': 0,
                'maxCredits': 1000, 'currentCredits': 900, 'maskingPolicy': 1, 'creationTime': '2024-09-09T10:43:52'}
        self.respond(body)
        info = Copyleaks.repository_info(AUTH_TOKEN, 'repo-1')
        self.assertCall('GET', f'{API}/v3/repositories/repository/repo-1/info', content_type=None)
        self.assertIsInstance(info, CopyleaksRepositoryInfoResponseModel)
        self.assertEqual((info.id, info.name, info.description, info.permission, info.status, info.max_credits,
                          info.current_credits, info.masking_policy, info.creation_time),
                         ('repo-1', 'Hub', 'd', 4, 0, 1000, 900, 1, '2024-09-09T10:43:52'))
        self.assertEqual(info['maxCredits'], 1000)


class PublicEndpointsTest(HttpTestCase):

    def test_release_notes(self):
        self.respond([{'version': 1}])
        self.assertEqual(Copyleaks.release_notes(), [{'version': 1}])
        self.assertCall('GET', f'{API}/v3/release-logs.json', auth=False, content_type=None)

    def test_supported_file_types_uses_the_documented_path(self):
        self.respond({'textual': ['pdf'], 'ocr': ['png']})
        self.assertEqual(Copyleaks.supported_file_types(), {'textual': ['pdf'], 'ocr': ['png']})
        self.assertCall('GET', f'{API}/v3/miscellaneous/supported-plagiarism-file-types', auth=False, content_type=None)

    def test_ocr_languages(self):
        self.respond(['en', 'fr'])
        self.assertEqual(Copyleaks.ocr_supported_langauges(), ['en', 'fr'])
        self.assertCall('GET', f'{API}/v3/miscellaneous/ocr-languages-list', auth=False, content_type=None)

    def test_supported_ai_text_detection_file_types(self):
        self.respond({'supportedAiFileTypes': ['pdf', 'docx', 'LaTeX']})
        response = Copyleaks.supported_ai_text_detection_file_types()
        self.assertCall('GET', f'{API}/v3/miscellaneous/supported-ai-text-detection-file-types', auth=False,
                        content_type=None)
        self.assertIsInstance(response, CopyleaksSupportedAiTextDetectionFileTypesResponseModel)
        self.assertEqual(response.supported_ai_file_types, ['pdf', 'docx', 'LaTeX'])
        self.assertEqual(response['supportedAiFileTypes'], ['pdf', 'docx', 'LaTeX'])

    def test_allowed_cross_languages(self):
        # The API returns {language name: code} objects.
        self.respond({'documentLanguages': {'english': 'en', 'spanish': 'es'},
                      'resultLanguages': {'french': 'fr', 'german': 'de'}})
        response = Copyleaks.allowed_cross_languages()
        self.assertCall('GET', f'{API}/v3/miscellaneous/allowed-cross-languages', auth=False, content_type=None)
        self.assertIsInstance(response, CopyleaksAllowedCrossLanguagesResponseModel)
        self.assertEqual(response.document_languages, {'english': 'en', 'spanish': 'es'})
        self.assertEqual(response.document_language_codes, ['en', 'es'])
        self.assertEqual(response.result_language_codes, ['fr', 'de'])
        self.assertEqual(response['resultLanguages'], {'french': 'fr', 'german': 'de'})

    def test_allowed_cross_languages_accepts_lists_of_codes(self):
        self.respond({'documentLanguages': ['en', 'es'], 'resultLanguages': ['fr']})
        response = Copyleaks.allowed_cross_languages()
        self.assertEqual(response.document_language_codes, ['en', 'es'])
        self.assertEqual(response.result_language_codes, ['fr'])

    def test_correction_types(self):
        self.respond({'correctionTypes': [{'id': 1}]})
        self.assertEqual(Copyleaks.WritingAssistantClient.get_correction_types('en'), {'correctionTypes': [{'id': 1}]})
        self.assertCall('GET', f'{API}/v1/writing-feedback/correction-types/en', auth=False, content_type=None)


class AiTextAndWritingTest(HttpTestCase):

    def test_ai_text_with_explain_and_sensitivity(self):
        doc = NaturalLanguageDocument(TEXT)
        doc.set_sandbox(True)
        doc.set_language('en')
        doc.set_explain(True)
        doc.set_sensitivity(3)
        self.respond({'summary': {'ai': 1, 'human': 0}})
        response = Copyleaks.AiDetectionClient.submit_natural_language(AUTH_TOKEN, 'scan1', doc)
        call = self.assertCall('POST', f'{API}/v2/writer-detector/scan1/check')
        self.assertEqual(call.json(), {'text': TEXT, 'sandbox': True, 'language': 'en', 'explain': True, 'sensitivity': 3})
        self.assertEqual(response.summary.ai, 1)

    def test_ai_text_credits_balance(self):
        self.respond({'credits': 382})
        response = Copyleaks.AiDetectionClient.credits_balance(AUTH_TOKEN)
        call = self.assertCall('GET', f'{API}/v2/writer-detector/credits', content_type=None)
        self.assertIsNone(call.data)
        self.assertIsInstance(response, CopyleaksAiTextDetectionCreditsResponseModel)
        self.assertEqual(response.credits, 382)
        self.assertEqual(response['credits'], 382)

    def test_grammar_checker_with_zero_weight(self):
        weights = ScoreWeights()
        weights.set_grammar_score_weight(0.0)
        weights.set_mechanics_score_weight(1)
        doc = WritingAssistantDocument(TEXT)
        doc.set_sandbox(False)
        doc.set_score(weights)
        self.respond({'score': {'corrections': {'overallScore': 90}}})
        response = Copyleaks.WritingAssistantClient.submit_text(AUTH_TOKEN, 'scan1', doc)
        call = self.assertCall('POST', f'{API}/v1/writing-feedback/scan1/check')
        self.assertEqual(call.json(), {'text': TEXT, 'sandbox': False,
                                       'score': {'grammarScoreWeight': 0.0, 'mechanicsScoreWeight': 1}})
        self.assertEqual(response.score.corrections.overall_score, 90)

    def test_text_moderation_body(self):
        model = CopyleaksTextModerationRequestModel(
            text=TEXT, sandbox=True, labels=[CopyleaksTextModerationLabel(id='toxic-v1'), {'id': 'adult-v1'}])
        self.respond({'modelVersion': 'v1', 'moderations': {'text': {'chars': {'labels': [], 'starts': [], 'lengths': []}}},
                      'scannedDocument': {'scanId': 'scan1', 'totalWords': 10, 'creationTime': '2025-08-06T08:05:20Z'}})
        response = Copyleaks.TextModerationClient.submit_text(AUTH_TOKEN, 'scan1', model)
        call = self.assertCall('POST', f'{API}/v1/text-moderation/scan1/check')
        # language is unset, so it is left out instead of being sent as null
        self.assertEqual(call.json(), {'text': TEXT, 'sandbox': True, 'labels': [{'id': 'toxic-v1'}, {'id': 'adult-v1'}]})
        self.assertEqual(response.modelVersion, 'v1')
        self.assertIsNone(response.scannedDocument.actualCredits)


class AiImageTest(HttpTestCase):
    RESPONSE = {'model': 'ai-image-1-ultra', 'summary': {'human': 0.3, 'ai': 0.7}, 'isAiDetected': True,
                'imageInfo': {'shape': {'height': 512, 'width': 512}},
                'scannedDocument': {'scanId': 'scan1', 'actualCredits': 1, 'expectedCredits': 1, 'creationTime': 't'}}

    def test_json_submit_with_mask_type_and_object_detection(self):
        model = CopyleaksAiImageDetectionRequestModel(
            base64='aGVsbG8=', file_name='a.png', model=CopyleaksAiImageDetectionModels.AI_IMAGE_1_ULTRA, sandbox=True,
            mask_type=CopyleaksAiImageMaskTypes.HEATMAP, object_detection=['face', {'object': 'hand'}])
        self.respond(self.RESPONSE)
        response = Copyleaks.ImageDetectionClient.submit(AUTH_TOKEN, 'scan1', model)
        call = self.assertCall('POST', f'{API}/v1/ai-image-detector/scan1/check')
        self.assertEqual(call.json(), {'base64': 'aGVsbG8=', 'filename': 'a.png', 'model': 'ai-image-1-ultra',
                                       'sandbox': True, 'maskType': 'heatmap',
                                       'objectDetection': [{'object': 'face'}, {'object': 'hand'}]})
        self.assertIsInstance(response, CopyleaksAiImageDetectionResponseModel)
        self.assertTrue(response.is_ai_detected)

    def test_json_submit_leaves_out_unset_options(self):
        model = CopyleaksAiImageDetectionRequestModel(base64='aGVsbG8=', file_name='a.png', model='ai-image-1-ultra')
        self.respond(self.RESPONSE)
        Copyleaks.ImageDetectionClient.submit(AUTH_TOKEN, 'scan1', model)
        self.assertEqual(self.session.last.json(), {'base64': 'aGVsbG8=', 'filename': 'a.png',
                                                    'model': 'ai-image-1-ultra', 'sandbox': False})

    def test_multipart_submit_file(self):
        model = CopyleaksAiImageDetectionFileRequestModel(
            image=io.BytesIO(PNG), file_name='a.png', model='ai-image-1-ultra', sandbox=True,
            mask_type='none', object_detection=['face'])
        body = dict(self.RESPONSE)
        self.respond(body)
        response = Copyleaks.ImageDetectionClient.submit_file(AUTH_TOKEN, 'scan1', model)
        call = self.assertCall('POST', f'{API}/v1/ai-image-detector/scan1/check', content_type=None)
        self.assertEqual(call.data, {'filename': 'a.png', 'model': 'ai-image-1-ultra', 'sandbox': 'true',
                                     'maskType': 'none', 'objectDetection': '[{"object":"face"}]'})
        name, content, content_type = call.files['image']
        self.assertEqual((name, content_type), ('a.png', 'image/png'))
        wire = call.prepared()
        self.assertTrue(wire.headers['Content-Type'].startswith('multipart/form-data; boundary='))
        self.assertIn(b'name="image"; filename="a.png"', wire.body)
        self.assertIn(PNG, wire.body)
        self.assertIn(b'name="objectDetection"\r\n\r\n[{"object":"face"}]', wire.body)
        self.assertNotIn(base64.b64encode(PNG), wire.body)
        self.assertIsNone(response.result)

    def test_multipart_submit_file_with_bytes_and_defaults(self):
        model = CopyleaksAiImageDetectionFileRequestModel(image=PNG, file_name='a.jpg', model='ai-image-1-ultra')
        self.respond(self.RESPONSE)
        Copyleaks.ImageDetectionClient.submit_file(AUTH_TOKEN, 'scan1', model)
        call = self.session.last
        self.assertEqual(call.data, {'filename': 'a.jpg', 'model': 'ai-image-1-ultra', 'sandbox': 'false'})
        self.assertEqual(call.files['image'], ('a.jpg', PNG, 'image/jpeg'))

    def test_async_submit(self):
        model = CopyleaksAiImageDetectionAsyncRequestModel(
            url='https://example.com/image1.png', file_name='image1.png', model='ai-image-1-ultra',
            mask_type='heatmap', object_detection=['face'], headers=[['X-Auth', 't']],
            webhooks={'url': 'https://example.com/webhook', 'headers': [('Authorization', 'Bearer w')]},
            sandbox=True, developer_payload='order-1')
        self.respond(None, status_code=201)
        self.assertIsNone(Copyleaks.ImageDetectionClient.submit_async(AUTH_TOKEN, 'scan1', model))
        call = self.assertCall('PUT', f'{API}/v1/ai-image-detector-async/scan1/submit')
        self.assertEqual(call.json(), {
            'url': 'https://example.com/image1.png', 'fileName': 'image1.png', 'model': 'ai-image-1-ultra',
            'webhooks': {'url': 'https://example.com/webhook', 'headers': [['Authorization', 'Bearer w']]},
            'maskType': 'heatmap', 'objectDetection': [{'object': 'face'}], 'headers': [['X-Auth', 't']],
            'sandbox': True, 'developerPayload': 'order-1'})

    def test_async_submit_minimal_body(self):
        model = CopyleaksAiImageDetectionAsyncRequestModel(
            url='https://example.com/image1.png', file_name='image1.png', model='ai-image-1-ultra',
            webhooks={'url': 'https://example.com/webhook'})
        Copyleaks.ImageDetectionClient.submit_async(AUTH_TOKEN, 'scan1', model)
        self.assertEqual(self.session.last.json(), {'url': 'https://example.com/image1.png', 'fileName': 'image1.png',
                                                    'model': 'ai-image-1-ultra',
                                                    'webhooks': {'url': 'https://example.com/webhook'}})


class ImagePlagiarismTest(HttpTestCase):
    RESPONSE = {
        'developerPayload': 'my-custom-data',
        'scannedImage': {'scanId': 'scan1', 'expectedCredits': 1, 'actualCredits': 1,
                         'creationTime': '2026-05-24T10:00:00Z', 'width': 1920, 'height': 1080, 'filename': 'photo.jpg'},
        'matches': {
            'internet': [
                {'url': 'https://example.com/images/photo.jpg', 'matchType': 0,
                 'webPages': [{'url': 'https://example.com/blog/my-post'}, {'url': 'https://example.org/news'}]},
                {'url': 'https://example.org/gallery/photo-sm.jpg', 'matchType': 1}],
            'score': {'totalMatches': 2, 'fullMatches': 1, 'partialMatches': 1}}}

    def test_check_is_multipart(self):
        model = CopyleaksImagePlagiarismRequestModel(image=PNG, file_name='photo.jpg', sandbox=True,
                                                     developer_payload='my-custom-data')
        self.respond(self.RESPONSE)
        response = Copyleaks.ImagePlagiarismClient.check(AUTH_TOKEN, 'scan1', model)
        call = self.assertCall('POST', f'{API}/v1/image-plagiarism-detector/scan1/check', content_type=None)
        self.assertEqual(call.data, {'filename': 'photo.jpg', 'sandbox': 'true', 'developerPayload': 'my-custom-data'})
        self.assertEqual(call.files, {'image': ('photo.jpg', PNG, 'image/jpeg')})
        wire = call.prepared()
        self.assertTrue(wire.headers['Content-Type'].startswith('multipart/form-data; boundary='))
        self.assertIn(b'name="image"; filename="photo.jpg"', wire.body)
        self.assertIn(b'name="sandbox"\r\n\r\ntrue', wire.body)

        self.assertIsInstance(response, CopyleaksImagePlagiarismResponseModel)
        self.assertEqual(response.developer_payload, 'my-custom-data')
        self.assertEqual(response.scanned_image.width, 1920)
        self.assertEqual(response.scanned_image.filename, 'photo.jpg')
        self.assertEqual(response.matches.score.total_matches, 2)
        self.assertEqual(response.matches.internet[0].match_type, 0)
        self.assertEqual(response.matches.internet[0].web_pages[1].url, 'https://example.org/news')
        self.assertEqual(response.matches.internet[1].web_pages, [])
        self.assertEqual(response['matches']['score']['fullMatches'], 1)

    def test_check_without_developer_payload(self):
        model = CopyleaksImagePlagiarismRequestModel(image=io.BytesIO(PNG), filename='photo.png')
        self.respond({'developerPayload': None, 'matches': {'internet': [], 'score': {'totalMatches': 0}}})
        response = Copyleaks.ImagePlagiarismClient.check(AUTH_TOKEN, 'scan1', model)
        self.assertEqual(self.session.last.data, {'filename': 'photo.png', 'sandbox': 'false'})
        self.assertEqual(response.matches.internet, [])


class AiVideoTest(HttpTestCase):

    def test_submit(self):
        model = CopyleaksAiVideoDetectionRequestModel(
            url='https://example.com/my-video.mp4', file_name='my-video.mp4',
            model=CopyleaksAiVideoDetectionModels.AI_VIDEO_1_PRO,
            webhooks={'url': 'https://example.com/webhook/receive-results', 'headers': [['Authorization', 'Bearer w']]},
            headers=[['X-Custom-Auth', 'my-token']], verb='get', sandbox=True, developer_payload='order-id-12345')
        self.respond({}, status_code=201)
        self.assertIsNone(Copyleaks.VideoDetectionClient.submit(AUTH_TOKEN, 'video1', model))
        call = self.assertCall('POST', f'{API}/v1/ai-video-detector/video1/submit')
        self.assertEqual(call.json(), {
            'url': 'https://example.com/my-video.mp4', 'filename': 'my-video.mp4', 'model': 'ai-video-1-pro',
            'webhooks': {'url': 'https://example.com/webhook/receive-results', 'headers': [['Authorization', 'Bearer w']]},
            'headers': [['X-Custom-Auth', 'my-token']], 'verb': 'GET', 'sandbox': True,
            'developerPayload': 'order-id-12345'})

    def test_submit_minimal_body(self):
        model = CopyleaksAiVideoDetectionRequestModel(
            url='https://example.com/v.mp4', filename='v.mp4', model='ai-video-1-pro',
            webhooks={'url': 'https://example.com/webhook'})
        Copyleaks.VideoDetectionClient.submit(AUTH_TOKEN, 'video1', model)
        self.assertEqual(self.session.last.json(), {'url': 'https://example.com/v.mp4', 'filename': 'v.mp4',
                                                    'model': 'ai-video-1-pro',
                                                    'webhooks': {'url': 'https://example.com/webhook'}})


class ExpiredTokenTest(HttpTestCase):

    def test_expired_token_is_rejected_before_any_request(self):
        from copyleaks.exceptions.auth_expired_error import AuthExipredError
        expired = {'access_token': 'x', '.expires': '2000-01-01T00:00:00Z'}
        with self.assertRaises(AuthExipredError):
            Copyleaks.AiDetectionClient.credits_balance(expired)
        with self.assertRaises(AuthExipredError):
            Copyleaks.repository_info(expired, 'repo')
        self.assertEqual(self.session.calls, [])

    def test_naive_expiry_time_is_treated_as_utc(self):
        Copyleaks.verify_auth_token({'access_token': 'x', '.expires': '2999-01-01T00:00:00'})


if __name__ == '__main__':
    unittest.main()
