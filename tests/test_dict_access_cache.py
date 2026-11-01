'''Unit tests for the dict-style access of the typed responses: the dict is built once and reused.'''
import unittest
from unittest.mock import patch

from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionResponseModel import CopyleaksAiTextDetectionResponseModel
from copyleaks.models.submit.Webhooks.CompletedWebhookModel import CompletedWebhookModel

BODY = {
    "modelVersion": "v11",
    "results": [{"classification": 2, "probability": 1.0,
                 "matches": [{"text": {"chars": {"starts": [i], "lengths": [1]}}} for i in range(50)]}],
    "summary": {"human": 0.0, "ai": 1.0},
}


class DictAccessCacheTest(unittest.TestCase):

    def test_model_is_serialized_once_for_many_reads(self):
        response = CopyleaksAiTextDetectionResponseModel(**BODY)
        original = CopyleaksAiTextDetectionResponseModel.model_dump
        with patch.object(CopyleaksAiTextDetectionResponseModel, 'model_dump', autospec=True,
                          side_effect=original) as dump:
            for i in range(50):
                self.assertEqual(response['results'][0]['matches'][i]['text']['chars']['starts'], [i])
            self.assertEqual(response.get('summary'), {'human': 0.0, 'ai': 1.0})
            self.assertIn('modelVersion', response)
        self.assertEqual(dump.call_count, 1)

    def test_setting_an_attribute_refreshes_the_dict(self):
        response = CopyleaksAiTextDetectionResponseModel(**BODY)
        self.assertEqual(response['modelVersion'], 'v11')
        response.model_version = 'v12'
        self.assertEqual(response['modelVersion'], 'v12')

    def test_copies_do_not_share_a_stale_dict(self):
        response = CopyleaksAiTextDetectionResponseModel(**BODY)
        self.assertEqual(response['modelVersion'], 'v11')
        copied = response.model_copy(update={'model_version': 'v13'})
        self.assertEqual(copied['modelVersion'], 'v13')
        self.assertEqual(response['modelVersion'], 'v11')

    def test_missing_keys(self):
        response = CopyleaksAiTextDetectionResponseModel(**BODY)
        self.assertIsNone(response.get('explain'))
        self.assertNotIn('explain', response)
        with self.assertRaises(KeyError):
            response['explain']

    def test_webhook_models_cache_too(self):
        completed = CompletedWebhookModel(**{"status": 0, "results": {"internet": [{"id": "1", "url": "u"}]}})
        original = type(completed.results).model_dump
        with patch.object(type(completed.results), 'model_dump', autospec=True, side_effect=original) as dump:
            for _ in range(10):
                self.assertEqual(completed.results['internet'][0]['url'], 'u')
        self.assertEqual(dump.call_count, 1)


if __name__ == '__main__':
    unittest.main()
