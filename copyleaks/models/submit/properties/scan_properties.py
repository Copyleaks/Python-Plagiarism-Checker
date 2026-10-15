from xmlrpc.client import Boolean
from copyleaks.models.submit.properties.ai_source_match import AISourceMatch
from copyleaks.models.submit.properties.assignment import Assignment
from copyleaks.models.submit.properties.course import Course
from copyleaks.models.submit.properties.institution import Institution
from copyleaks.models.submit.properties.overview import Overview
from copyleaks.models.submit.properties.references import References
from copyleaks.models.submit.properties.sensitive_data_protection import SensitiveDataProtection
from copyleaks.models.submit.properties.writing_feedback import WritingFeedback
from copyleaks.models.submit.properties.submit_action import SubmitAction
from copyleaks.models.submit.properties.submit_webhooks import SubmitWebhooks


class ScanProperties:

    def __init__(self, status_webhook):
        webhooks = SubmitWebhooks()
        webhooks.set_status(status_webhook)
        self.set_webhooks(webhooks)


    def get_action(self):
        return self.action

    def set_action(self, value):
        '''A `SubmitAction`: Scan, CheckCredits or Index.'''
        assert value != None

        self.action = value

    def get_include_html(self):
        return self.includeHtml

    def set_include_html(self, value):
        '''Include an HTML version in the scan artifacts.'''

        assert isinstance(value, bool)

        self.includeHtml = value

    def get_developer_payload(self):
        return self.developerPayload

    def set_developer_payload(self, value):
        '''Custom string, up to 512 characters.'''

        assert value and len(value) <= 512

        self.developerPayload = value


    def get_sandbox(self):
        return self.sandbox

    def set_sandbox(self, value):
        '''Sandbox mode: mock results without using credits. Use False in production.'''

        assert value != None and type(value) is Boolean

        self.sandbox = value

    def get_expiration(self):
        return self.expiration

    def set_expiration(self, value):
        '''Hours the scan is kept on the Copyleaks servers, 1 to 2880 (4 months).'''

        assert value

        self.expiration = value

    def get_author(self):
        return self.author.id

    def set_author(self, value):
        '''An `Author`.'''

        assert value

        self.author = value

    def get_webhooks(self):
        return self.webhooks

    def set_webhooks(self, value):
        '''A `SubmitWebhooks`.'''

        assert value

        self.webhooks = value

    def get_filters(self):
        return self.filters

    def set_filters(self, value):
        '''Result filters, a `Filters`.'''

        assert value

        self.filters = value

    def get_scanning(self):
        return self.scanning

    def set_scanning(self, value):
        '''What to compare against, a `Scanning`.'''

        assert value

        self.scanning = value

    def get_indexing(self):
        return self.indexing

    def set_indexing(self, value):
        '''Where to index the document, an `Indexing`.'''

        assert value

        self.indexing = value

    def get_exclude(self):
        return self.exclude

    def set_exclude(self, value):
        '''Parts of the document not to scan, an `Exclude`.'''

        assert value

        self.exclude = value

    def get_pdf(self):
        return self.pdf

    def set_pdf(self, value):
        '''PDF report settings, a `Pdf`.'''

        assert value

        self.pdf = value

    def get_sensitivity_level(self):
        return self.sensitivityLevel

    def set_sensitivity_level(self, value):
        '''1 to 5: 1 is the fastest scan with the largest matches, 5 the slowest, finding the smallest ones.'''

        assert value and value >= 1 and value <= 5

        self.sensitivityLevel = value

    def get_cheat_detection(self):
        return self.cheatDetection

    def set_cheat_detection(self, value):
        '''Check the document for cheating; a detection adds a scan alert to the completed webhook.'''

        assert isinstance(value, bool)

        self.cheatDetection = value

    def get_scan_method_algorithm(self):
        return self.scanMethodAlgorithm
    
    
    def set_scan_method_algorithm(self, value):
        '''A `ScanMethodAlgorithm`: MaximumCoverage or MaximumResults.'''
        assert 0 <= value <= 1
        
        self.scanMethodAlgorithm = value

    def get_ai_generated_text(self):
        return self.aiGeneratedText
    
    def set_ai_generated_text(self, value):
        '''AI text detection settings, an `AIGeneratedText`.'''
        assert value
        self.aiGeneratedText = value

    def get_ai_source_match(self):
        return self.aiSourceMatch

    def set_ai_source_match(self, value):
        '''An `AISourceMatch`.'''
        assert isinstance(value, AISourceMatch)
        self.aiSourceMatch = value

    def get_display_language(self):
        return self.displayLanguage

    def set_display_language(self, value):
        '''PDF report language: "en" (default), "es", "pt", "fr", "de" or "it", lowercase. Needs `pdf.create`.'''
        assert value
        self.displayLanguage = value

    def get_custom_metadata(self):
        return self.customMetadata
    
    def set_custom_metadata(self, value):
        '''Custom properties of the document in a repository, added to its results: a list of `CustomMetadata`.'''
        assert value
        self.customMetadata = value

    def get_scan_time_zone(self):
        return self.scanTimeZone

    def set_scan_time_zone(self, value):
        '''IANA time zone (case-sensitive) of the scan time in the PDF report, e.g. "America/New_York". Default: account country or UTC.'''
        if not isinstance(value, str) or not value:
            raise ValueError('scan_time_zone must be a non-empty string')
        self.scanTimeZone = value

    def get_course(self):
        return self.course

    def set_course(self, value):
        '''A `Course`.'''
        if not isinstance(value, Course):
            raise TypeError('value must be a `Course`')
        self.course = value

    def get_assignment(self):
        return self.assignment

    def set_assignment(self, value):
        '''An `Assignment`.'''
        if not isinstance(value, Assignment):
            raise TypeError('value must be an `Assignment`')
        self.assignment = value

    def get_institution(self):
        return self.institution

    def set_institution(self, value):
        '''An `Institution`.'''
        if not isinstance(value, Institution):
            raise TypeError('value must be an `Institution`')
        self.institution = value

    def get_sensitive_data_protection(self):
        return self.sensitiveDataProtection

    def set_sensitive_data_protection(self, value):
        '''A `SensitiveDataProtection`.'''
        if not isinstance(value, SensitiveDataProtection):
            raise TypeError('value must be a `SensitiveDataProtection`')
        self.sensitiveDataProtection = value

    def get_writing_feedback(self):
        return self.writingFeedback

    def set_writing_feedback(self, value):
        '''A `WritingFeedback`.'''
        if not isinstance(value, WritingFeedback):
            raise TypeError('value must be a `WritingFeedback`')
        self.writingFeedback = value

    def get_overview(self):
        return self.overview

    def set_overview(self, value):
        '''An `Overview`.'''
        if not isinstance(value, Overview):
            raise TypeError('value must be an `Overview`')
        self.overview = value

    def get_internal_ai_source_match(self):
        return self.internalAiSourceMatch

    def set_internal_ai_source_match(self, value):
        '''An `InternalAISourceMatch` (an `AISourceMatch` works too).'''
        if not isinstance(value, AISourceMatch):
            raise TypeError('value must be an `AISourceMatch`')
        self.internalAiSourceMatch = value

    def get_references(self):
        return self.references

    def set_references(self, value):
        '''A `References`.'''
        if not isinstance(value, References):
            raise TypeError('value must be a `References`')
        self.references = value
