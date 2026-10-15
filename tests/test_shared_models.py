'''
Unit tests for the models that AI Image and AI Video Detection share: the webhooks, metadata and scan info models,
and the base of the three AI Image Detection requests. The 5.x model names keep working.
'''
import base64
import unittest

from pydantic import ValidationError

from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionAsyncRequestModel import CopyleaksAiImageDetectionAsyncRequestModel
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionBaseRequestModel import CopyleaksAiImageDetectionBaseRequestModel
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionFileRequestModel import CopyleaksAiImageDetectionFileRequestModel
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionRequestModel import CopyleaksAiImageDetectionRequestModel
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageObjectDetectionModel import CopyleaksAiImageObjectDetectionModel
from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionResponseModel import CopyleaksAiImageDetectionResponseModel
from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionScannedDocumentModel import CopyleaksAiImageDetectionScannedDocumentModel
from copyleaks.models.ImageDetection.Responses.CopyleaksImageMetadataModel import CopyleaksImageMetadataModel
from copyleaks.models.VideoDetection.Requests.CopyleaksAiVideoDetectionRequestModel import CopyleaksAiVideoDetectionRequestModel
from copyleaks.models.VideoDetection.Responses.CopyleaksAiVideoDetectionResponseModel import CopyleaksAiVideoDetectionResponseModel
from copyleaks.models.shared.CopyleaksDetectionWebhooksModel import CopyleaksDetectionWebhooksModel
from copyleaks.models.shared.CopyleaksMediaMetadataModel import CopyleaksMediaMetadataModel
from copyleaks.models.shared.CopyleaksScanInfoModel import CopyleaksScanInfoModel

PNG = b'\x89PNG\r\n\x1a\n fake image bytes'
METADATA = {'issuedTime': '2026-03-17T13:14:57+00:00', 'issuedBy': 'OpenAI', 'appOrDeviceUsed': 'Sora',
            'contentSummary': 'Created using generative AI'}
SCAN = {'scanId': 'scan1', 'actualCredits': 1, 'expectedCredits': 2, 'creationTime': '2026-05-05T12:37:50Z'}
WEBHOOKS = {'url': 'https://example.com/webhook', 'headers': [('Authorization', 'Bearer w')]}


def image_request_factories(file_name='a.png', **options):
    '''Callables that build each AI Image Detection request with the same file name and options.'''
    return [
        lambda: CopyleaksAiImageDetectionRequestModel(base64=base64.b64encode(PNG).decode('ascii'),
                                                      file_name=file_name, model='ai-image-1-ultra', **options),
        lambda: CopyleaksAiImageDetectionFileRequestModel(image=PNG, file_name=file_name, model='ai-image-1-ultra',
                                                          **options),
        lambda: CopyleaksAiImageDetectionAsyncRequestModel(url='https://example.com/a.png', file_name=file_name,
                                                           model='ai-image-1-ultra', webhooks={'url': 'https://e/w'},
                                                           **options),
    ]


def image_requests(**options):
    '''One of each AI Image Detection request, with the same options.'''
    return [make() for make in image_request_factories(**options)]


class SharedResponseModelsTest(unittest.TestCase):

    def test_image_and_video_results_use_the_same_models(self):
        video = CopyleaksAiVideoDetectionResponseModel(**{'videoInfo': {'duration': 1.5, 'metadata': METADATA},
                                                          'scannedVideo': SCAN})
        image = CopyleaksAiImageDetectionResponseModel(**{'imageInfo': {'metadata': METADATA},
                                                          'scannedDocument': SCAN})
        self.assertIs(type(video.video_info.metadata), CopyleaksMediaMetadataModel)
        self.assertIs(type(image.image_info.metadata), CopyleaksMediaMetadataModel)
        self.assertIs(type(video.scanned_video), CopyleaksScanInfoModel)
        self.assertIs(type(image.scanned_document), CopyleaksScanInfoModel)
        self.assertEqual(video.video_info.metadata, image.image_info.metadata)
        self.assertEqual(video.scanned_video, image.scanned_document)
        self.assertEqual(video.scanned_video.expected_credits, 2)
        self.assertEqual(image.image_info.metadata.app_or_device_used, 'Sora')

    def test_5x_image_model_names_still_work(self):
        self.assertIs(CopyleaksImageMetadataModel, CopyleaksMediaMetadataModel)
        self.assertIs(CopyleaksAiImageDetectionScannedDocumentModel, CopyleaksScanInfoModel)
        metadata = CopyleaksImageMetadataModel(**METADATA)
        self.assertEqual((metadata.issued_by, metadata.content_summary), ('OpenAI', 'Created using generative AI'))
        scanned = CopyleaksAiImageDetectionScannedDocumentModel(**{'scanId': 's', 'actualCredits': 3})
        self.assertEqual((scanned.scan_id, scanned.actual_credits, scanned.creation_time), ('s', 3, None))
        self.assertEqual(scanned.model_dump(by_alias=True, exclude_unset=True), {'scanId': 's', 'actualCredits': 3})


class SharedWebhooksModelTest(unittest.TestCase):

    def test_image_and_video_requests_use_the_same_webhooks_model(self):
        video = CopyleaksAiVideoDetectionRequestModel(url='https://example.com/v.mp4', file_name='v.mp4',
                                                      model='ai-video-1-pro', webhooks=WEBHOOKS)
        image = CopyleaksAiImageDetectionAsyncRequestModel(url='https://example.com/a.png', file_name='a.png',
                                                           model='ai-image-1-ultra', webhooks=WEBHOOKS)
        for request in (video, image):
            self.assertIs(type(request.webhooks), CopyleaksDetectionWebhooksModel)
            self.assertEqual(request.model_dump(by_alias=True, exclude_none=True)['webhooks'],
                             {'url': 'https://example.com/webhook', 'headers': [['Authorization', 'Bearer w']]})

    def test_webhooks_are_validated(self):
        for webhooks in ({'url': ' '}, {'url': 'https://e/w', 'headers': 'x'},
                         {'url': 'https://e/w', 'headers': [['a']]}):
            with self.assertRaises(ValidationError, msg=repr(webhooks)):
                CopyleaksDetectionWebhooksModel(**webhooks)


class ImageRequestBaseModelTest(unittest.TestCase):

    def test_every_image_request_shares_the_base(self):
        for model in (CopyleaksAiImageDetectionRequestModel, CopyleaksAiImageDetectionFileRequestModel,
                      CopyleaksAiImageDetectionAsyncRequestModel):
            self.assertTrue(issubclass(model, CopyleaksAiImageDetectionBaseRequestModel), model.__name__)
            for name in ('mask_type', 'object_detection'):
                self.assertNotIn(name, model.__annotations__, model.__name__)

    def test_options_parse_and_serialize_the_same_way(self):
        for request in image_requests(mask_type='heatmap', object_detection=['face', {'object': 'hand'}]):
            name = type(request).__name__
            self.assertEqual(request.mask_type, 'heatmap', name)
            self.assertEqual(request.object_detection, [CopyleaksAiImageObjectDetectionModel(object='face'),
                                                        CopyleaksAiImageObjectDetectionModel(object='hand')], name)
            body = request.model_dump(by_alias=True, exclude_none=True)
            self.assertEqual(body['maskType'], 'heatmap', name)
            self.assertEqual(body['objectDetection'], [{'object': 'face'}, {'object': 'hand'}], name)

    def test_file_name_keeps_its_json_name(self):
        sync_json, multipart, async_json = image_requests()
        self.assertEqual(sync_json.model_dump(by_alias=True)['filename'], 'a.png')
        self.assertEqual(multipart.model_dump(by_alias=True)['filename'], 'a.png')
        self.assertEqual(async_json.model_dump(by_alias=True)['fileName'], 'a.png')
        self.assertNotIn('fileName', sync_json.model_dump(by_alias=True))
        self.assertNotIn('filename', async_json.model_dump(by_alias=True))

    def test_file_name_and_options_are_validated_on_every_request(self):
        bad_values = [{'file_name': 'a.gif'}, {'file_name': ''}, {'file_name': '  '},
                      {'object_detection': ['a', 'b', 'c', 'd']}, {'object_detection': 'face'},
                      {'object_detection': [{'object': ''}]}]
        for bad in bad_values:
            for make in image_request_factories(**bad):
                with self.assertRaises(ValidationError, msg=repr(bad)):
                    make()
        for request in image_requests():
            self.assertIsNone(request.mask_type)
            self.assertIsNone(request.object_detection)
            self.assertNotIn('maskType', request.model_dump(by_alias=True, exclude_none=True))


if __name__ == '__main__':
    unittest.main()
