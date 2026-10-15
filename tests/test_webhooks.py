'''
Unit tests for the webhook models: `Model(**request.json)` parses every documented field into typed models,
and the read-only dict-style access of earlier versions keeps working.
'''
import copy
import json
import unittest

from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionResponseModel import CopyleaksAiImageDetectionResponseModel
from copyleaks.models.VideoDetection.Responses.CopyleaksAiVideoDetectionResponseModel import CopyleaksAiVideoDetectionResponseModel
from copyleaks.models.submit.Webhooks.CompletedWebhookModel import CompletedWebhookModel
from copyleaks.models.submit.Webhooks.CreditsCheckedWebhookModel import CreditsCheckedWebhookModel
from copyleaks.models.submit.Webhooks.ErrorWebhookModel import ErrorWebhookModel
from copyleaks.models.submit.Webhooks.ExportCompletedWebhookModel import ExportCompletedWebhookModel
from copyleaks.models.submit.Webhooks.HelperModels.BaseModels.MetadataModel import MetadataModel
from copyleaks.models.submit.Webhooks.HelperModels.CompletedModels.ResultsModel import ResultsModel
from copyleaks.models.submit.Webhooks.HelperModels.CompletedModels.ScannedDocumentModel import ScannedDocumentModel
from copyleaks.models.submit.Webhooks.HelperModels.ErrorModels.ErrorModel import ErrorModel
from copyleaks.models.submit.Webhooks.HelperModels.ExportModels.TaskModel import TaskModel
from copyleaks.models.submit.Webhooks.HelperModels.ResultsModels.InternetModel import InternetModel
from copyleaks.models.submit.Webhooks.HelperModels.ResultsModels.SharedResultsModel import SharedResultsModel
from copyleaks.models.submit.Webhooks.HelperModels.ResultsModels.TagsModel import TagsModel
from copyleaks.models.submit.Webhooks.IndexedWebhookModel import IndexedWebhookModel
from copyleaks.models.submit.Webhooks.NewResultWebhookModel import NewResultWebhookModel

METADATA = {"finalUrl": "https://example.com/final", "canonicalUrl": "https://example.com/canonical",
            "author": "Jane", "organization": "Org", "filename": "file.txt", "publishDate": "2025-01-01",
            "creationDate": "2025-01-02", "lastModificationDate": "2025-01-03"}

COMPLETED = {
    "status": 0,
    "developerPayload": "Custom developer payload",
    "scannedDocument": {"scanId": "scan1", "totalWords": 120, "totalExcluded": 3, "credits": 1,
                        "creationTime": "2025-01-01T00:00:00Z", "metadata": METADATA,
                        "expectedCredits": 1, "detectedLanguage": "en"},
    "results": {
        "internet": [{"id": "i1", "title": "Internet", "introduction": "intro", "matchedWords": 10,
                      "url": "https://example.com/page", "metadata": METADATA,
                      "tags": [{"code": "c1", "title": "Tag", "description": "desc"}]}],
        "database": [{"id": "d1", "title": "Db", "introduction": "intro", "matchedWords": 5, "scanId": "my-scan",
                      "metadata": METADATA}],
        "batch": [{"id": "b1", "title": "Batch", "introduction": "intro", "matchedWords": 4, "scanId": "batch-scan",
                   "metadata": METADATA}],
        "repositories": [{"id": "r1", "title": "Repo", "introduction": "intro", "matchedWords": 3,
                          "repositoryId": "repo-1", "scanId": "repo-scan",
                          "metadata": dict(METADATA, submittedBy="user@example.com")}],
        "internalAIData": [{"id": "ai1", "title": "AI", "introduction": "intro", "matchedWords": 30,
                            "identicalWords": 20, "similarWords": 6, "paraphrasedWords": 4, "totalWords": 300,
                            "tags": [{"code": "internal-ai-source-match", "title": "AI-Generated",
                                      "description": "This result contains AI-generated text"}]}],
        "score": {"identicalWords": 10, "minorChangedWords": 2, "relatedMeaningWords": 1, "aggregatedScore": 25.5}},
    "referencesValidation": {"summary": {"total": 8, "academic": 5, "academicValidated": 4, "nonAcademicValidated": 2}},
    "notifications": {"alerts": [{"category": 2, "code": "suspected-ai-text", "title": "AI", "message": "m",
                                  "helpLink": "https://example.com/help", "severity": 1,
                                  "additionalData": json.dumps({"summary": {"ai": 0.9, "human": 0.1}})}]},
}


class CompletedWebhookTest(unittest.TestCase):

    def setUp(self):
        self.completed = CompletedWebhookModel(**copy.deepcopy(COMPLETED))

    def test_status_and_developer_payload(self):
        self.assertEqual(self.completed.status, 0)
        self.assertEqual(self.completed.developer_payload, 'Custom developer payload')

    def test_scanned_document(self):
        doc = self.completed.scanned_document
        self.assertIsInstance(doc, ScannedDocumentModel)
        self.assertEqual((doc.scan_id, doc.total_words, doc.total_excluded, doc.credits, doc.creation_time),
                         ('scan1', 120, 3, 1, '2025-01-01T00:00:00Z'))
        self.assertEqual(doc.metadata.final_url, 'https://example.com/final')
        self.assertEqual(doc.metadata.last_modification_date, '2025-01-03')

    def test_results(self):
        results = self.completed.results
        self.assertIsInstance(results, ResultsModel)
        internet = results.internet[0]
        self.assertEqual((internet.id, internet.url, internet.matched_words), ('i1', 'https://example.com/page', 10))
        self.assertEqual(internet.tags[0].description, 'desc')
        self.assertEqual(results.database[0].scan_id, 'my-scan')
        self.assertEqual(results.batch[0].scan_id, 'batch-scan')
        repository = results.repositories[0]
        self.assertEqual(repository.repository_id, 'repo-1')
        self.assertEqual(repository.metadata.submitted_by, 'user@example.com')
        ai = results.internal_ai_data[0]
        self.assertEqual((ai.identical_words, ai.similar_words, ai.paraphrased_words, ai.total_words), (20, 6, 4, 300))
        self.assertEqual(ai.tags[0].code, 'internal-ai-source-match')
        self.assertEqual(results.score.aggregated_score, 25.5)

    def test_references_validation(self):
        summary = self.completed.references_validation.summary
        self.assertEqual((summary.total, summary.academic, summary.academic_validated, summary.non_academic_validated),
                         (8, 5, 4, 2))

    def test_notifications_and_ai_alert(self):
        alert = self.completed.get_ai_detection_alert()
        self.assertEqual(alert.help_link, 'https://example.com/help')
        self.assertEqual(self.completed.get_ai_detection_result().summary.ai, 0.9)

    def test_dict_access_of_earlier_versions_still_works(self):
        results = self.completed.results
        self.assertEqual(results['internet'][0]['url'], 'https://example.com/page')
        self.assertEqual(results.get('score')['aggregatedScore'], 25.5)
        self.assertIn('internalAIData', results)
        self.assertEqual(self.completed.notifications['alerts'][0]['code'], 'suspected-ai-text')
        self.assertEqual(self.completed['scannedDocument']['scanId'], 'scan1')

    def test_undocumented_fields_are_kept(self):
        self.assertEqual(self.completed.scanned_document.model_extra['detectedLanguage'], 'en')
        self.assertEqual(self.completed['scannedDocument']['expectedCredits'], 1)

    def test_null_lists_are_empty(self):
        completed = CompletedWebhookModel(**{"status": 0, "results": {"internet": None, "batch": None}})
        self.assertEqual(completed.results.internet, [])
        self.assertEqual(completed.results.batch, [])
        self.assertIsNone(completed.scanned_document)

    def test_dump_round_trip(self):
        dumped = self.completed.model_dump(by_alias=True, exclude_unset=True)
        self.assertEqual(dumped['results']['internalAIData'][0]['paraphrasedWords'], 4)
        self.assertEqual(CompletedWebhookModel(**dumped).results.score.aggregated_score, 25.5)

    def test_snake_case_and_positional_construction(self):
        completed = CompletedWebhookModel(None, None, ScannedDocumentModel('scan2', 5), 0,
                                          developer_payload='payload')
        self.assertEqual(completed.scanned_document.scan_id, 'scan2')
        self.assertEqual(completed.scanned_document.total_words, 5)
        self.assertEqual(completed.status, 0)
        self.assertEqual(completed.developer_payload, 'payload')
        self.assertEqual(SharedResultsModel(id_val='r1').id, 'r1')
        self.assertEqual(SharedResultsModel(id_val='r1').id_val, 'r1')
        self.assertEqual(TaskModel(endpont='https://e').endpoint, 'https://e')
        with self.assertRaises(TypeError):
            ErrorModel(1, 'm', 'extra')

    def test_internet_result_keeps_the_5x_positional_order(self):
        tag = TagsModel('c1', 'Tag', 'desc')
        result = InternetModel([tag], 'i1', 'Title', 'intro', 10, None, MetadataModel(author='Jane'), 'https://e/p')
        self.assertEqual((result.id, result.title, result.introduction, result.matched_words, result.url),
                         ('i1', 'Title', 'intro', 10, 'https://e/p'))
        self.assertEqual(result.tags[0].code, 'c1')
        self.assertEqual(result.metadata.author, 'Jane')
        with self.assertRaises(TypeError):
            InternetModel([tag], 'i1', 'Title', 'intro', 10, None, None, 'https://e/p', 'extra')

    def test_numeric_result_id_is_a_string(self):
        completed = CompletedWebhookModel(**{"results": {"database": [{"id": 12345}]}})
        self.assertEqual(completed.results.database[0].id, '12345')


class OtherStatusWebhooksTest(unittest.TestCase):

    def test_credits_checked(self):
        webhook = CreditsCheckedWebhookModel(**{"status": 2, "developerPayload": "p", "credits": 3,
                                                "scannedDocument": {"scanId": "s", "totalWords": 700}})
        self.assertEqual((webhook.status, webhook.developer_payload, webhook.credits), (2, 'p', 3))
        self.assertEqual(webhook.scanned_document.total_words, 700)

    def test_indexed(self):
        webhook = IndexedWebhookModel(**{"status": 3, "developerPayload": "p"})
        self.assertEqual((webhook.status, webhook.developer_payload), (3, 'p'))

    def test_error_has_every_documented_field(self):
        webhook = ErrorWebhookModel(**{
            "status": 1, "developerPayload": "p",
            "error": {"type": "invalid_request_error", "id": "missing_parameter", "code": 1,
                      "message": "Bad request.", "url": "https://docs.example.com/errors",
                      "details": [{"param": "filename", "message": "required"}]}})
        error = webhook.error
        self.assertEqual((webhook.status, webhook.developer_payload), (1, 'p'))
        self.assertEqual((error.type, error.id, error.code, error.message, error.url),
                         ('invalid_request_error', 'missing_parameter', 1, 'Bad request.', 'https://docs.example.com/errors'))
        self.assertEqual((error.details[0].param, error.details[0].message), ('filename', 'required'))
        self.assertEqual(webhook.error['code'], 1)

    def test_export_completed_tasks_is_a_list(self):
        webhook = ExportCompletedWebhookModel(**{
            "completed": True, "developerPayload": "p",
            "tasks": [{"endpoint": "https://e/1", "httpStatusCode": 200, "isHealthy": True},
                      {"endpoint": "https://e/2", "httpStatusCode": None, "isHealthy": False}]})
        self.assertTrue(webhook.completed)
        self.assertEqual(webhook.developer_payload, 'p')
        self.assertEqual([t.endpoint for t in webhook.tasks], ['https://e/1', 'https://e/2'])
        self.assertEqual(webhook.tasks[0].http_status_code, 200)
        self.assertFalse(webhook.tasks[1].is_healthy)
        self.assertEqual(webhook.tasks[0]['isHealthy'], True)

    def test_new_result(self):
        webhook = NewResultWebhookModel(**{
            "score": {"aggregatedScore": 12.0}, "developerPayload": "p",
            "internet": [{"id": "i", "url": "https://e", "matchedWords": 4, "metadata": METADATA}],
            "database": [{"id": "d", "scanId": "s"}], "batch": [{"id": "b"}],
            "repositories": [{"id": "r", "repositoryId": "repo", "metadata": {"submittedBy": "u"}}],
            "internalAIData": [{"id": "ai", "totalWords": 9}]})
        self.assertEqual(webhook.score.aggregated_score, 12.0)
        self.assertEqual(webhook.developer_payload, 'p')
        self.assertEqual(webhook.internet[0].metadata.author, 'Jane')
        self.assertEqual(webhook.database[0].scan_id, 's')
        self.assertEqual(webhook.batch[0].id, 'b')
        self.assertEqual(webhook.repositories[0].metadata.submitted_by, 'u')
        self.assertEqual(webhook.internal_ai_data[0].total_words, 9)
        self.assertEqual(webhook.internet[0]['url'], 'https://e')

    def test_new_result_score_as_a_number(self):
        self.assertEqual(NewResultWebhookModel(**{"score": 7}).score.aggregated_score, 7.0)


class AsyncDetectionWebhooksTest(unittest.TestCase):

    def test_ai_video_webhook(self):
        payload = {
            "model": "ai-video-1-pro",
            "audioResult": {"starts": [13000, 45000], "lengths": [14000, 1000],
                            "exclude": {"starts": [0], "lengths": [2950]}},
            "visualResult": {"starts": [11566], "lengths": [6134], "exclude": {"starts": [], "lengths": []}},
            "summary": {"audioAIRatio": 0.4902, "visualAIRatio": 0.5817, "overallAIRatio": 0.7487},
            "isAiDetected": True,
            "videoInfo": {"metadata": {"issuedTime": "2026-03-17T13:14:57+00:00", "issuedBy": "OpenAI",
                                       "appOrDeviceUsed": "Sora", "contentSummary": "Created using generative AI"},
                          "duration": 55.7},
            "scannedVideo": {"scanId": "video1", "actualCredits": 1, "expectedCredits": 1,
                             "creationTime": "2026-05-05T12:37:50Z"},
            "developerPayload": "order-1"}
        result = CopyleaksAiVideoDetectionResponseModel(**payload)
        self.assertEqual(result.model, 'ai-video-1-pro')
        self.assertEqual(result.audio_result.starts, [13000, 45000])
        self.assertEqual(result.audio_result.exclude.lengths, [2950])
        self.assertEqual(result.visual_result.exclude.starts, [])
        self.assertEqual(result.summary.overall_ai_ratio, 0.7487)
        self.assertEqual(result.summary.audio_ai_ratio, 0.4902)
        self.assertTrue(result.is_ai_detected)
        self.assertEqual(result.video_info.duration, 55.7)
        self.assertEqual(result.video_info.metadata.content_summary, 'Created using generative AI')
        self.assertEqual(result.scanned_video.scan_id, 'video1')
        self.assertEqual(result.developer_payload, 'order-1')
        self.assertIsNone(result.error)
        self.assertEqual(result['summary']['visualAIRatio'], 0.5817)

    def test_ai_image_webhook_and_response_fields(self):
        payload = {
            "model": "ai-image-1-ultra",
            "result": {"starts": [0, 512], "lengths": [256, 512], "labels": [4, 2]},
            "summary": {"human": 0.3, "ai": 0.7}, "isAiDetected": True,
            "imageInfo": {"shape": {"height": 1024, "width": 768},
                          "metadata": {"issuedTime": "2025-07-23T12:44:05", "issuedBy": "OpenAI",
                                       "appOrDeviceUsed": "OpenAI-API", "contentSummary": "Created using generative AI"}},
            "detectedObjects": [{"object": "face", "mask": {"starts": [1024], "lengths": [512]}}],
            "scannedDocument": {"scanId": "s", "actualCredits": 1, "expectedCredits": 1, "creationTime": "t"},
            "developerPayload": "order-1", "scanType": "sandbox"}
        result = CopyleaksAiImageDetectionResponseModel(**payload)
        self.assertEqual(result.result.labels, [4, 2])
        self.assertTrue(result.is_ai_detected)
        self.assertEqual(result.image_info.metadata.content_summary, 'Created using generative AI')
        self.assertEqual(result.detected_objects[0].object, 'face')
        self.assertEqual(result.detected_objects[0].mask.lengths, [512])
        self.assertEqual(result.developer_payload, 'order-1')
        self.assertEqual(result.scan_type, 'sandbox')
        self.assertIsNone(result.error)

    def test_ai_video_and_image_failure_webhooks(self):
        payload = {"error": {"type": "invalid_request_error", "id": "unsupported_file", "code": 400,
                             "message": "The file is not supported.", "url": "https://docs.example.com/errors",
                             "details": [{"param": "url", "message": "unsupported format"}]},
                   "developerPayload": "order-2", "undocumented": 7}
        for model in (CopyleaksAiVideoDetectionResponseModel, CopyleaksAiImageDetectionResponseModel):
            result = model(**payload)
            error = result.error
            self.assertEqual((error.type, error.id, error.code, error.message, error.url),
                             ('invalid_request_error', 'unsupported_file', 400, 'The file is not supported.',
                              'https://docs.example.com/errors'), model.__name__)
            self.assertEqual((error.details[0].param, error.details[0].message), ('url', 'unsupported format'))
            self.assertEqual(result.developer_payload, 'order-2')
            self.assertIsNone(result.summary)
            self.assertEqual(result.model_dump(by_alias=True)['undocumented'], 7)
        minimal = CopyleaksAiVideoDetectionResponseModel(**{"error": {"code": 500, "message": "Failed."}})
        self.assertEqual((minimal.error.code, minimal.error.type, minimal.error.details), (500, None, []))
        self.assertIsNone(minimal.developer_payload)
        self.assertEqual(minimal['error']['code'], 500)

    def test_ai_image_without_mask(self):
        result = CopyleaksAiImageDetectionResponseModel(**{"model": "ai-image-1-ultra", "summary": {"human": 1, "ai": 0},
                                                           "isAiDetected": False})
        self.assertIsNone(result.result)
        self.assertIsNone(result.detected_objects)
        self.assertIsNone(result.scanned_document)


if __name__ == '__main__':
    unittest.main()
