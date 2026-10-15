'''Unit tests for the submit properties and request models: JSON names on the wire, new fields, and validation.'''
import json
import unittest

from pydantic import ValidationError

from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionAsyncRequestModel import CopyleaksAiImageDetectionAsyncRequestModel
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionFileRequestModel import CopyleaksAiImageDetectionFileRequestModel
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionRequestModel import CopyleaksAiImageDetectionRequestModel
from copyleaks.models.ImagePlagiarism.Requests.CopyleaksImagePlagiarismRequestModel import CopyleaksImagePlagiarismRequestModel
from copyleaks.models.TextModeration.Requests.CopyleaksTextModerationLabel import CopyleaksTextModerationLabel
from copyleaks.models.TextModeration.Requests.CopyleaksTextModerationRequestModel import CopyleaksTextModerationRequestModel
from copyleaks.models.VideoDetection.Requests.CopyleaksAiVideoDetectionRequestModel import CopyleaksAiVideoDetectionRequestModel
from copyleaks.models.delete import Delete
from copyleaks.models.export import Export
from copyleaks.models.submit.ai_detection_document import NaturalLanguageDocument
from copyleaks.models.submit.document import FileDocument, UrlDocument
from copyleaks.models.submit.properties.ai_generated_text import AIGeneratedText
from copyleaks.models.submit.properties.ai_generated_text_explain import AIGeneratedTextExplain
from copyleaks.models.submit.properties.assignment import Assignment
from copyleaks.models.submit.properties.author import Author
from copyleaks.models.submit.properties.course import Course
from copyleaks.models.submit.properties.cross_languages import CrossLanguages
from copyleaks.models.submit.properties.filters import Filters
from copyleaks.models.submit.properties.indexing import Indexing
from copyleaks.models.submit.properties.institution import Institution
from copyleaks.models.submit.properties.internal_ai_source_match import InternalAISourceMatch
from copyleaks.models.submit.properties.language import Language
from copyleaks.models.submit.properties.masking_policy import MaskingPolicy
from copyleaks.models.submit.properties.overview import Overview
from copyleaks.models.submit.properties.pdf import Pdf
from copyleaks.models.submit.properties.pdf_version import PdfVersion
from copyleaks.models.submit.properties.references import References
from copyleaks.models.submit.properties.report_customization_colors import ReportCustomizationColors
from copyleaks.models.submit.properties.repository import IndexingRepository
from copyleaks.models.submit.properties.scan_properties import ScanProperties
from copyleaks.models.submit.properties.scanning import Scanning
from copyleaks.models.submit.scanning_copyleaks_db import ScanningCopyleaksDb
from copyleaks.models.submit.properties.scanning_exclude import ScanningExclude
from copyleaks.models.submit.properties.scanning_include import ScanningInclude
from copyleaks.models.submit.properties.sensitive_data_protection import SensitiveDataProtection
from copyleaks.models.submit.properties.writing_feedback import WritingFeedback
from copyleaks.models.submit.score_weights import ScoreWeights
from copyleaks.models.submit.writing_assistant_document import WritingAssistantDocument

WEBHOOK = 'https://example.com/webhook/{STATUS}'


def wire(document):
    return json.loads(document.toJSON())


def submitted_properties(properties):
    doc = FileDocument('aGVsbG8=', 'a.txt')
    doc.set_properties(properties)
    return wire(doc)['properties']


class WireNamesTest(unittest.TestCase):

    def test_cross_languages_is_sent_as_crossLanguages(self):
        language = Language()
        language.set_code('fr')
        cross = CrossLanguages()
        cross.set_languages([language])
        scanning = Scanning()
        scanning.set_cross_languages(cross)
        properties = ScanProperties(WEBHOOK)
        properties.set_scanning(scanning)
        sent = submitted_properties(properties)['scanning']
        self.assertEqual(sent, {'crossLanguages': {'languages': [{'code': 'fr'}]}})
        self.assertIs(scanning.get_cross_languages(), cross)

    def test_pdf_colors_are_sent_as_colors(self):
        colors = ReportCustomizationColors()
        colors.set_main_strip('#000001')
        colors.set_titles('#000002')
        colors.set_identical('#000003')
        colors.set_minor_changes('#000004')
        colors.set_related_meaning('#000005')
        colors.set_ai_detection('#000006')
        colors.set_writing_feedback('#000007')
        pdf = Pdf()
        pdf.set_create(True)
        pdf.set_report_customization_colors(colors)
        pdf.set_version(PdfVersion.V3)
        pdf.set_report_version('v3')
        properties = ScanProperties(WEBHOOK)
        properties.set_pdf(pdf)
        sent = submitted_properties(properties)['pdf']
        self.assertEqual(sent, {'create': True, 'version': 3, 'reportVersion': 'v3', 'colors': {
            'mainStrip': '#000001', 'titles': '#000002', 'identical': '#000003', 'minorChanges': '#000004',
            'relatedMeaning': '#000005', 'aiDetection': '#000006', 'writingFeedback': '#000007'}})
        self.assertIs(pdf.get_report_customization_colors(), colors)
        self.assertIs(pdf.get_colors(), colors)

    def test_set_colors_alias(self):
        colors = ReportCustomizationColors()
        colors.set_titles('#040F21')
        pdf = Pdf()
        pdf.set_colors(colors)
        self.assertEqual(json.loads(json.dumps(pdf, default=lambda o: o.__dict__)), {'colors': {'titles': '#040F21'}})

    def test_to_json_is_compact(self):
        doc = FileDocument('aGVsbG8=', 'a.txt')
        self.assertEqual(doc.toJSON(), '{"base64":"aGVsbG8=","filename":"a.txt"}')


class NewScanPropertiesTest(unittest.TestCase):

    def test_all_new_properties(self):
        sdp = SensitiveDataProtection()
        for setter in ('set_drivers_license', 'set_credentials', 'set_passport', 'set_network', 'set_url',
                       'set_email_address', 'set_credit_card', 'set_phone_number'):
            getattr(sdp, setter)(True)
        weights = ScoreWeights()
        weights.set_grammar_score_weight(0.0)
        weights.set_word_choice_score_weight(0.5)
        writing = WritingFeedback()
        writing.set_enable(True)
        writing.set_score(weights)
        overview = Overview()
        overview.set_enable(True)
        overview.set_ignore_ai_detection(True)
        overview.set_ignore_plagiarism_detection(False)
        overview.set_ignore_writing_feedback(True)
        overview.set_ignore_author_data(False)
        internal = InternalAISourceMatch()
        internal.set_enable(True)
        references = References()
        references.set_validate(True)
        explain = AIGeneratedTextExplain()
        explain.set_enable(True)
        ai = AIGeneratedText()
        ai.set_detect(True)
        ai.set_sensitivity(1)
        ai.set_explain(explain)

        properties = ScanProperties(WEBHOOK)
        properties.set_sensitive_data_protection(sdp)
        properties.set_writing_feedback(writing)
        properties.set_overview(overview)
        properties.set_internal_ai_source_match(internal)
        properties.set_references(references)
        properties.set_ai_generated_text(ai)
        properties.set_scan_time_zone('America/New_York')
        properties.set_course(Course('course-1'))
        properties.set_assignment(Assignment('assignment-1'))
        properties.set_institution(Institution('institution-1'))

        sent = submitted_properties(properties)
        self.assertEqual(sent['sensitiveDataProtection'], {
            'driversLicense': True, 'credentials': True, 'passport': True, 'network': True, 'url': True,
            'emailAddress': True, 'creditCard': True, 'phoneNumber': True})
        self.assertEqual(sent['writingFeedback'], {'enable': True,
                                                   'score': {'grammarScoreWeight': 0.0, 'wordChoiceScoreWeight': 0.5}})
        self.assertEqual(sent['overview'], {'enable': True, 'ignoreAIDetection': True, 'ignorePlagiarismDetection': False,
                                            'ignoreWritingFeedback': True, 'ignoreAuthorData': False})
        self.assertEqual(sent['internalAiSourceMatch'], {'enable': True})
        self.assertEqual(sent['references'], {'validate': True})
        self.assertEqual(sent['aiGeneratedText'], {'detect': True, 'sensitivity': 1, 'explain': {'enable': True}})
        self.assertEqual(sent['scanTimeZone'], 'America/New_York')
        self.assertEqual(sent['course'], {'id': 'course-1'})
        self.assertEqual(sent['assignment'], {'id': 'assignment-1'})
        self.assertEqual(sent['institution'], {'id': 'institution-1'})
        self.assertEqual(properties.get_references().get_validate(), True)

    def test_scanning_include_exclude_and_indexing(self):
        exclude = ScanningExclude()
        exclude.set_id_pattern('abc*')
        exclude.set_backlinks_domains(['example.com', 'example.org'])
        exclude.set_text(['lorem ipsum', 'dolor'])
        include = ScanningInclude()
        include.set_id_pattern('course-a-*')
        copyleaks_db = ScanningCopyleaksDb()
        copyleaks_db.set_include_my_submissions(True)
        scanning = Scanning()
        scanning.set_internet(True)
        scanning.set_exclude(exclude)
        scanning.set_include(include)
        scanning.set_copyleaks_db(copyleaks_db)
        indexing = Indexing()
        indexing.set_copyleaks_db(True)
        properties = ScanProperties(WEBHOOK)
        properties.set_scanning(scanning)
        properties.set_indexing(indexing)
        sent = submitted_properties(properties)
        self.assertEqual(sent['scanning'], {
            'internet': True,
            'exclude': {'idPattern': 'abc*', 'backlinksDomains': ['example.com', 'example.org'],
                        'text': ['lorem ipsum', 'dolor']},
            'include': {'idPattern': 'course-a-*'},
            'copyleaksDb': {'includeMySubmissions': True}})
        self.assertEqual(sent['indexing'], {'copyleaksDb': True})

    def test_misspelled_copyleaks_db_setter_still_works(self):
        copyleaks_db = ScanningCopyleaksDb()
        copyleaks_db.set_include_others_submissions(False)
        scanning = Scanning()
        scanning.set_copylekas_db(copyleaks_db)
        self.assertIs(scanning.get_copyleaks_db(), copyleaks_db)
        self.assertIs(scanning.get_copylekas_db(), copyleaks_db)

    def test_limits(self):
        # The setters added in 6.0.0 raise ValueError or TypeError, so they also validate under `python -O`.
        exclude = ScanningExclude()
        with self.assertRaises(ValueError):
            exclude.set_backlinks_domains(['d%d.com' % i for i in range(11)])
        with self.assertRaises(ValueError):
            exclude.set_backlinks_domains([''])
        with self.assertRaises(ValueError):
            exclude.set_text(['x' * 31])
        with self.assertRaises(ValueError):
            exclude.set_text(['a', 'b', 'c', 'd', 'e', 'f'])
        ai = AIGeneratedText()
        for bad in (0, 4):
            with self.assertRaises(ValueError):
                ai.set_sensitivity(bad)
        for bad in (True, '2', 2.0):
            with self.assertRaises(TypeError):
                ai.set_sensitivity(bad)
        properties = ScanProperties(WEBHOOK)
        with self.assertRaises(TypeError):
            properties.set_course('course-1')
        with self.assertRaises(TypeError):
            properties.set_references(True)
        with self.assertRaises(ValueError):
            properties.set_scan_time_zone('')
        with self.assertRaises(ValueError):
            ScanningInclude().set_id_pattern('')
        with self.assertRaises(ValueError):
            Course().set_id('')
        for setter in (Overview().set_enable, SensitiveDataProtection().set_email_address, WritingFeedback().set_enable,
                       References().set_validate, Indexing().set_copyleaks_db, InternalAISourceMatch().set_enable,
                       AIGeneratedTextExplain().set_enable):
            with self.assertRaises(TypeError):
                setter('yes')

    def test_id_pattern_must_be_a_string(self):
        with self.assertRaises(TypeError):
            ScanningExclude().set_id_pattern(True)
        with self.assertRaises(ValueError):
            ScanningExclude().set_id_pattern('')

    def test_score_weights_accept_zero_and_reject_out_of_range(self):
        weights = ScoreWeights()
        for setter in ('set_grammar_score_weight', 'set_mechanics_score_weight',
                       'set_sentence_structure_score_weight', 'set_word_choice_score_weight'):
            getattr(weights, setter)(0.0)
            getattr(weights, setter)(1.0)
            with self.assertRaises(ValueError):
                getattr(weights, setter)(1.5)
            with self.assertRaises(ValueError):
                getattr(weights, setter)(-0.1)
            with self.assertRaises(TypeError):
                getattr(weights, setter)('0.5')


class GetterAndValidationFixesTest(unittest.TestCase):

    def test_filters_getters(self):
        filters = Filters()
        filters.set_identical_enabled(True)
        filters.set_minor_changes_enabled(False)
        filters.set_related_meaning_enabled(True)
        filters.set_allow_same_domain(False)
        self.assertEqual(filters.get_minor_changes_enabled(), False)
        self.assertEqual(filters.get_related_meaning_enabled(), True)
        self.assertEqual(filters.get_allow_same_domain(), False)

    def test_author_get_id(self):
        author = Author()
        author.set_id('author-1')
        self.assertEqual(author.get_id(), 'author-1')

    def test_masking_policy_no_mask(self):
        repository = IndexingRepository()
        repository.set_masking_policy(MaskingPolicy.NoMask)
        self.assertEqual(repository.get_masking_policy(), 0)
        with self.assertRaises(ValueError):
            repository.set_masking_policy(7)

    def test_writing_assistant_sandbox_false(self):
        doc = WritingAssistantDocument('some text')
        doc.set_sandbox(False)
        self.assertEqual(wire(doc), {'text': 'some text', 'sandbox': False})

    def test_url_document_verb_validation(self):
        doc = UrlDocument()
        with self.assertRaises(ValueError):
            doc.set_verb('DELETE')
        with self.assertRaises(ValueError):
            doc.set_headers([['only-a-name']])
        with self.assertRaises(ValueError):
            Delete().set_headers('Authorization: x')
        with self.assertRaises(ValueError):
            Export().set_completion_webhook_headers([('a', 'b', 'c')])

    def test_natural_language_document(self):
        doc = NaturalLanguageDocument('text')
        doc.set_explain(False)
        doc.set_sensitivity(2)
        self.assertEqual(wire(doc), {'text': 'text', 'explain': False, 'sensitivity': 2})
        with self.assertRaises(ValueError):
            doc.set_sensitivity(5)
        with self.assertRaises(TypeError):
            doc.set_sensitivity('2')
        with self.assertRaises(TypeError):
            doc.set_explain('yes')


class PydanticRequestModelsTest(unittest.TestCase):

    def test_moderation_labels_are_required_and_at_most_16(self):
        with self.assertRaises(ValidationError):
            CopyleaksTextModerationRequestModel(text='hello')
        with self.assertRaises(ValidationError):
            CopyleaksTextModerationRequestModel(text='hello', labels=[])
        labels = [CopyleaksTextModerationLabel(id='toxic-v1')] * 16
        self.assertEqual(len(CopyleaksTextModerationRequestModel(text='hello', labels=labels).labels), 16)
        with self.assertRaises(ValidationError):
            CopyleaksTextModerationRequestModel(text='hello', labels=labels + labels[:1])

    def test_moderation_label_id_is_1_to_32_characters(self):
        CopyleaksTextModerationLabel(id='x' * 32)
        with self.assertRaises(ValidationError):
            CopyleaksTextModerationLabel(id='x' * 33)
        with self.assertRaises(ValidationError):
            CopyleaksTextModerationLabel(id='')

    def test_ai_image_object_detection_limits(self):
        def build(objects):
            return CopyleaksAiImageDetectionRequestModel(base64='aGVsbG8=', file_name='a.png', model='m',
                                                         object_detection=objects)
        self.assertEqual(len(build(['face', 'hand', 'car']).object_detection), 3)
        for bad in (['a', 'b', 'c', 'd'], [], ['x' * 33], [''], 'face'):
            with self.assertRaises(ValidationError, msg=repr(bad)):
                build(bad)

    def test_ai_image_accepts_avif(self):
        model = CopyleaksAiImageDetectionRequestModel(base64='aGVsbG8=', file_name='a.avif', model='m')
        self.assertEqual(model.file_name, 'a.avif')
        with self.assertRaises(ValidationError):
            CopyleaksAiImageDetectionRequestModel(base64='aGVsbG8=', file_name='a.gif', model='m')

    def test_ai_image_file_model_validation(self):
        with self.assertRaises(ValidationError):
            CopyleaksAiImageDetectionFileRequestModel(image=b'', file_name='a.png', model='m')
        with self.assertRaises(ValidationError):
            CopyleaksAiImageDetectionFileRequestModel(image='not bytes', file_name='a.png', model='m')
        with self.assertRaises(ValidationError):
            CopyleaksAiImageDetectionFileRequestModel(image=b'x', file_name='a.txt', model='m')

    def test_async_and_video_models_require_webhooks(self):
        with self.assertRaises(ValidationError):
            CopyleaksAiImageDetectionAsyncRequestModel(url='https://e/a.png', file_name='a.png', model='m')
        with self.assertRaises(ValidationError):
            CopyleaksAiVideoDetectionRequestModel(url='https://e/v.mp4', file_name='v.mp4', model='m')
        with self.assertRaises(ValidationError):
            CopyleaksAiVideoDetectionRequestModel(url='https://e/v.mp4', file_name='v.mp4', model='m',
                                                  webhooks={'url': 'https://e/w'}, verb='DELETE')
        with self.assertRaises(ValidationError):
            CopyleaksAiVideoDetectionRequestModel(url='https://e/v.gif', file_name='v.gif', model='m',
                                                  webhooks={'url': 'https://e/w'})
        with self.assertRaises(ValidationError):
            CopyleaksAiVideoDetectionRequestModel(url='https://e/v.mp4', file_name='v.mp4', model='m',
                                                  webhooks={'url': 'https://e/w', 'headers': [['a']]})

    def test_image_plagiarism_model_validation(self):
        model = CopyleaksImagePlagiarismRequestModel(image=b'x', filename='a.ico')
        self.assertEqual(model.file_name, 'a.ico')
        self.assertFalse(model.sandbox)
        with self.assertRaises(ValidationError):
            CopyleaksImagePlagiarismRequestModel(image=b'x', file_name='a.heic')


if __name__ == '__main__':
    unittest.main()
