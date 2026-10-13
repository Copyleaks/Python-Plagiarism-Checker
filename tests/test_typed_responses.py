'''
Unit tests for the typed responses of the AI text detection and Writing Assistant endpoints.
The HTTP layer (`requests`) is mocked, so no network calls are made.

Run from the repository root:
    python -m unittest discover -s tests -v
'''

import copy
import unittest
from unittest.mock import MagicMock, patch

from copyleaks.copyleaks import Copyleaks
from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionResponseModel import CopyleaksAiTextDetectionResponseModel
from copyleaks.models.WritingAssistant.Responses.CopyleaksWritingAssistantResponseModel import CopyleaksWritingAssistantResponseModel

AUTH_TOKEN = {'access_token': 'token', '.expires': '2999-01-01T00:00:00Z'}

# Example response from the API docs (reference/data-types/ai-detector/ai-text-detector-response).
# The docs show `scannedDocument.credits`; the server (ScannedDocumentSection) sends `actualCredits`.
AI_TEXT_RESPONSE = {
    "modelVersion": "v11.0",
    "results": [
        {
            "classification": 2,
            "probability": 0.7316979,
            "matches": [
                {
                    "text": {
                        "chars": {"starts": [0], "lengths": [554]},
                        "words": {"starts": [0], "lengths": [73]}
                    }
                }
            ]
        }
    ],
    "summary": {"human": 0.0, "ai": 1.0},
    "scannedDocument": {
        "scanId": "scan-id",
        "totalWords": 73,
        "totalExcluded": 0,
        "actualCredits": 1,
        "expectedCredits": 1,
        "creationTime": "2025-08-10T08:33:05.22225Z"
    },
    "explain": {
        "patterns": {
            "statistics": {
                "aiCount": [1.2066389, 9.673915, 34.41001],
                "humanCount": [0.18481831, 0.13894142, 0.33555666],
                "proportion": [6.5287843, 69.625854, 102.54607],
                "source": [1, 1, 1]
            },
            "text": {
                "chars": {"starts": [10, 96, 136], "lengths": [25, 33, 33]},
                "words": {"starts": [1, 12, 17], "lengths": [4, 4, 5]}
            }
        }
    }
}

# Example response from the API docs (reference/data-types/writing/writing-assistant).
# The docs show `scannedDocument.credits`; the server (ScannedDocumentSection) sends `actualCredits`.
WRITING_ASSISTANT_RESPONSE = {
    "score": {
        "corrections": {
            "grammarCorrectionsCount": 2,
            "grammarCorrectionsScore": 87,
            "grammarScoreWeight": 1.0,
            "mechanicsCorrectionsCount": 9,
            "mechanicsCorrectionsScore": 38,
            "mechanicsScoreWeight": 1.0,
            "sentenceStructureCorrectionsCount": 0,
            "sentenceStructureCorrectionsScore": 100,
            "sentenceStructureScoreWeight": 1.0,
            "wordChoiceCorrectionsCount": 1,
            "wordChoiceCorrectionsScore": 93,
            "wordChoiceScoreWeight": 1.0,
            "overallScore": 79
        },
        "readability": {
            "score": 59,
            "readabilityLevel": 5,
            "readabilityLevelText": "10th to 12th Grader",
            "readabilityLevelDescription": "Fairly difficult to read"
        },
        "statistics": {
            "sentenceCount": 5,
            "averageSentenceLength": 12.2,
            "averageWordLength": 5.5,
            "readingTimeSeconds": 16.0,
            "speakingTimeSeconds": 28.2
        }
    },
    "corrections": {
        "text": {
            "chars": {
                "types": [5, 18, 3],
                "starts": [13, 22, 61],
                "lengths": [2, 10, 9],
                "operationTexts": ["an ", "plagiarism ", "businesses "]
            }
        }
    },
    "scannedDocument": {
        "scanId": "scan-id",
        "totalWords": 61,
        "totalExcluded": 0,
        "actualCredits": 1,
        "expectedCredits": 1,
        "creationTime": "2025-08-11T06:46:01.2886658Z"
    }
}


class _MockedPostTest(unittest.TestCase):

    def mock_post(self, payload):
        response = MagicMock(ok=True, status_code=200)
        response.json.return_value = copy.deepcopy(payload)
        patcher = patch('requests.post', return_value=response)
        patcher.start()
        self.addCleanup(patcher.stop)


class AiTextDetectionResponseTest(_MockedPostTest):

    def submit(self, payload):
        self.mock_post(payload)
        return Copyleaks.AiDetectionClient.submit_natural_language(AUTH_TOKEN, 'scan-id', MagicMock())

    def test_returns_typed_model(self):
        self.assertIsInstance(self.submit(AI_TEXT_RESPONSE), CopyleaksAiTextDetectionResponseModel)

    def test_fields_parse(self):
        response = self.submit(AI_TEXT_RESPONSE)

        self.assertEqual(response.model_version, 'v11.0')
        self.assertEqual(response.summary.ai, 1.0)
        self.assertEqual(response.summary.human, 0.0)
        self.assertEqual(len(response.results), 1)
        section = response.results[0]
        self.assertEqual(section.classification, 2)
        self.assertAlmostEqual(section.probability, 0.7316979)
        self.assertEqual(section.matches[0].text.chars.starts, [0])
        self.assertEqual(section.matches[0].text.chars.lengths, [554])
        self.assertEqual(section.matches[0].text.words.lengths, [73])
        self.assertEqual(response.scanned_document.scan_id, 'scan-id')
        self.assertEqual(response.scanned_document.total_words, 73)
        self.assertEqual(response.scanned_document.actual_credits, 1)
        self.assertEqual(response.scanned_document.creation_time, '2025-08-10T08:33:05.22225Z')
        self.assertIsNone(response.scan_type)

    def test_explain_patterns_parse(self):
        patterns = self.submit(AI_TEXT_RESPONSE).explain.patterns

        self.assertEqual(patterns.statistics.ai_count, [1.2066389, 9.673915, 34.41001])
        self.assertEqual(patterns.statistics.human_count, [0.18481831, 0.13894142, 0.33555666])
        self.assertEqual(patterns.statistics.proportion, [6.5287843, 69.625854, 102.54607])
        self.assertEqual(patterns.statistics.source, [1, 1, 1])
        self.assertEqual(patterns.text.chars.starts, [10, 96, 136])
        self.assertEqual(patterns.text.chars.lengths, [25, 33, 33])
        self.assertEqual(patterns.text.words.starts, [1, 12, 17])
        self.assertIsNone(patterns.html)

    def test_without_explain(self):
        payload = {k: v for k, v in AI_TEXT_RESPONSE.items() if k != 'explain'}
        response = self.submit(payload)

        self.assertIsNone(response.explain)
        self.assertNotIn('explain', response)
        self.assertIsNone(response.get('explain'))

    def test_sandbox_response_parses(self):
        # Shape of the sandbox response: extra `scanType`, empty `scannedDocument`.
        payload = {
            "results": AI_TEXT_RESPONSE["results"],
            "summary": {"human": 0.0, "ai": 1.0},
            "modelVersion": "v8.0",
            "scanType": "sandbox",
            "scannedDocument": {}
        }
        response = self.submit(payload)

        self.assertEqual(response.summary.ai, 1.0)
        self.assertEqual(response.scan_type, 'sandbox')
        self.assertEqual(response['scanType'], 'sandbox')
        self.assertIsNone(response.scanned_document.scan_id)

    def test_dict_access_is_backward_compatible(self):
        response = self.submit(AI_TEXT_RESPONSE)

        self.assertEqual(response['summary']['ai'], 1.0)
        self.assertEqual(response['results'][0]['matches'][0]['text']['chars']['starts'], [0])
        self.assertEqual(response['explain']['patterns']['statistics']['aiCount'], [1.2066389, 9.673915, 34.41001])
        self.assertEqual(response['scannedDocument']['actualCredits'], 1)
        self.assertEqual(response.get('modelVersion'), 'v11.0')
        self.assertEqual(response.get('missing', 'default'), 'default')
        self.assertIn('summary', response)
        with self.assertRaises(KeyError):
            response['missing']
        # Every key of the JSON response reads back the same value as the old raw dict.
        self.assertEqual({key: response[key] for key in AI_TEXT_RESPONSE}, AI_TEXT_RESPONSE)


class WritingAssistantResponseTest(_MockedPostTest):

    def submit(self, payload):
        self.mock_post(payload)
        return Copyleaks.WritingAssistantClient.submit_text(AUTH_TOKEN, 'scan-id', MagicMock())

    def test_returns_typed_model(self):
        self.assertIsInstance(self.submit(WRITING_ASSISTANT_RESPONSE), CopyleaksWritingAssistantResponseModel)

    def test_fields_parse(self):
        response = self.submit(WRITING_ASSISTANT_RESPONSE)

        corrections_score = response.score.corrections
        self.assertEqual(corrections_score.overall_score, 79)
        self.assertEqual(corrections_score.grammar_corrections_count, 2)
        self.assertEqual(corrections_score.mechanics_corrections_score, 38)
        self.assertEqual(corrections_score.word_choice_score_weight, 1.0)
        self.assertEqual(response.score.readability.readability_level, 5)
        self.assertEqual(response.score.readability.readability_level_text, '10th to 12th Grader')
        self.assertEqual(response.score.statistics.sentence_count, 5)
        self.assertEqual(response.score.statistics.average_sentence_length, 12.2)
        chars = response.corrections.text.chars
        self.assertEqual(chars.types, [5, 18, 3])
        self.assertEqual(chars.starts, [13, 22, 61])
        self.assertEqual(chars.lengths, [2, 10, 9])
        self.assertEqual(chars.operation_texts, ['an ', 'plagiarism ', 'businesses '])
        self.assertEqual(response.scanned_document.total_words, 61)
        self.assertEqual(response.scanned_document.actual_credits, 1)

    def test_sandbox_response_parses(self):
        # The sandbox response adds `scanType`.
        payload = dict(WRITING_ASSISTANT_RESPONSE, scanType='sandbox')
        response = self.submit(payload)

        self.assertEqual(response.score.corrections.overall_score, 79)
        self.assertEqual(response.scan_type, 'sandbox')
        self.assertEqual(response['scanType'], 'sandbox')

    def test_dict_access_is_backward_compatible(self):
        response = self.submit(WRITING_ASSISTANT_RESPONSE)

        self.assertEqual(response['score']['corrections']['overallScore'], 79)
        self.assertEqual(response['corrections']['text']['chars']['operationTexts'], ['an ', 'plagiarism ', 'businesses '])
        self.assertEqual(response.get('scannedDocument')['totalWords'], 61)
        self.assertIn('corrections', response)
        # Every key of the JSON response reads back the same value as the old raw dict.
        self.assertEqual({key: response[key] for key in WRITING_ASSISTANT_RESPONSE}, WRITING_ASSISTANT_RESPONSE)


if __name__ == '__main__':
    unittest.main()
