'''
 The MIT License(MIT)

 Copyright(c) 2016 Copyleaks LTD (https://copyleaks.com)

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
'''

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
        '''
            Get the selected type of content submission action.

            Returns:
                Selected action from the type `SubmitAction`.
        '''
        return self.action

    def set_action(self, value):
        '''
            Set the submission action type.

            Parameters:
                value: `SubmitAction` enum.
        '''
        assert value != None

        self.action = value

    def get_include_html(self):
        '''
            Whether to include HTML version on the scan artifacts.
        '''
        return self.includeHtml

    def set_include_html(self, value):
        '''
            Change the value of the 'includeHtml' setting.

            Parameters:
                value: Boolean.
        '''

        assert isinstance(value, bool)

        self.includeHtml = value

    def get_developer_payload(self):
        '''
            Getting the developer payload.
        '''
        return self.developerPayload

    def set_developer_payload(self, value):
        '''
            Setting the developer payload parameter. This string must be no longer then 512 characters.
        '''

        assert value and len(value) <= 512

        self.developerPayload = value


    def get_sandbox(self):
        '''
            Get the sandbox mode status.
        '''
        return self.sandbox

    def set_sandbox(self, value):
        '''
            Change sandbox mode.

            Parameters:
                value: Boolean. To turn on, specify `True`. On production, choose `False`.
        '''

        assert value != None and type(value) is Boolean

        self.sandbox = value

    def get_expiration(self):
        '''
            Get the maximum life span of a scan in hours on the Copyleaks servers.
        '''
        return self.expiration

    def set_expiration(self, value):
        '''
            Specify the maximum life span of a scan in hours on the Copyleaks servers.

            Parameters:
                value: Positive integer between 1 to 2880 (4 months).
        '''

        assert value

        self.expiration = value

    def get_author(self):
        '''
            Metadata about the author.
        '''
        return self.author.id

    def set_author(self, value):
        '''
            Metadata about the author.

            Parameters:
                value: `Author`.
        '''

        assert value

        self.author = value

    def get_webhooks(self):
        '''
            Get webhooks configuration.
        '''
        return self.webhooks

    def set_webhooks(self, value):
        '''
            Set webhooks configuration.

            Parameters:
                value: `SubmitWebhooks`.
        '''

        assert value

        self.webhooks = value

    def get_filters(self):
        '''
            Get Copyleaks results filter preferences.
        '''
        return self.filters

    def set_filters(self, value):
        '''
            Set Copyleaks results filter preferences.

            Parameters:
                value: `Filters`.
        '''

        assert value

        self.filters = value

    def get_scanning(self):
        '''
            Get Copyleaks scanning preferences.
        '''
        return self.scanning

    def set_scanning(self, value):
        '''
            Set Copyleaks scanning preferences.

            Parameters:
                value: `Scanning`.
        '''

        assert value

        self.scanning = value

    def get_indexing(self):
        '''
            Get indexing policy settings.
        '''
        return self.indexing

    def set_indexing(self, value):
        '''
            Set indexing policy settings.

            Parameters:
                value: `Indexing`.
        '''

        assert value

        self.indexing = value

    def get_exclude(self):
        '''
            Which parts of the document won't be scanned.
        '''
        return self.exclude

    def set_exclude(self, value):
        '''
            Which parts of the document won't be scanned.

            Parameters:
                value: `Exclude`.
        '''

        assert value

        self.exclude = value

    def get_pdf(self):
        '''
            PDF report generation settings.
        '''
        return self.pdf

    def set_pdf(self, value):
        '''
            PDF report generation settings.

            Parameters:
                value: `Pdf`.
        '''

        assert value

        self.pdf = value

    def get_sensitivity_level(self):
        '''
            PDF report generation settings.
        '''
        return self.sensitivityLevel

    def set_sensitivity_level(self, value):
        '''
            You can control the level of plagiarism sensitivity that will be identified according to the speed of the scan. If you prefer a faster scan with the results that contains the highest amount of plagiarism choose 1, and if a slower, more comprehensive scan, that will also detect the smallest instances choose 5.

            Parameters:
                value: Integer. Values between 1 to 5.
        '''

        assert value and value >= 1 and value <= 5

        self.sensitivityLevel = value

    def get_cheat_detection(self):
        '''
            When set to true the submitted document will be checked for cheating. If a cheating will be detected, a scan alert will be added to the completed webhook.
        '''
        return self.cheatDetection

    def set_cheat_detection(self, value):
        '''
            When set to true the submitted document will be checked for cheating. If a cheating will be detected, a scan alert will be added to the completed webhook.

            Parameters:
                value: Boolean
        '''

        assert isinstance(value, bool)

        self.cheatDetection = value

    def get_scan_method_algorithm(self):
        '''
            Get scan algorithm goal.
        '''
        return self.scanMethodAlgorithm
    
    
    def set_scan_method_algorithm(self, value):
        '''
            Choose the algorithm goal. You can set this value depending on your use-case.

            Parameters:
                value: ScanMethodAlgorithm enum
        '''
        assert 0 <= value <= 1
        
        self.scanMethodAlgorithm = value

    def get_ai_generated_text(self):
        '''
            Ai Generated text settings.
        '''
        return self.aiGeneratedText
    
    def set_ai_generated_text(self, value):
        '''
            Ai Generated text settings.

            Parameters:
                value: `AIGeneratedText`
        '''
        assert value
        self.aiGeneratedText = value

    def get_ai_source_match(self):
        '''
            Ai source match settings.
        '''
        return self.aiSourceMatch

    def set_ai_source_match(self, value):
        '''
            Identify online sources suspected of containing AI generated text.
            Currently only applies to documents detected as English.
            Leave it unset to get the server default (disabled).

            Parameters:
                value: `AISourceMatch`
        '''
        assert isinstance(value, AISourceMatch)
        self.aiSourceMatch = value

    def get_display_language(self):
        '''
            Get the language the PDF report is generated in.
        '''
        return self.displayLanguage

    def set_display_language(self, value):
        '''
            Set the language the PDF report is generated in.
            Only takes effect when `pdf.create` is True.
            Leave it unset to get the server default ("en").

            Parameters:
                value: String. One of "en", "es", "pt", "fr", "de", "it".
                    Values are lowercase and case-sensitive.
        '''
        assert value
        self.displayLanguage = value

    def get_custom_metadata(self):
        '''
            Get custom metadata
        '''
        return self.customMetadata
    
    def set_custom_metadata(self, value):
        '''
            Set custom properties that will be attached to your document in a Copyleaks repository.

            If this document is found as a repository result, your custom properties will be added to the result.

            value: `CustomMetadata` array
        '''
        assert value
        self.customMetadata = value

    def get_scan_time_zone(self):
        '''
            Get the time zone of the scan time shown in the PDF report.
        '''
        return self.scanTimeZone

    def set_scan_time_zone(self, value):
        '''
            Set the time zone of the scan time shown in the PDF report.
            Leave it unset to use the time zone of your account's country, or UTC when it is unknown.

            Parameters:
                value: String. A case-sensitive IANA time zone name, for example "America/New_York".
        '''
        if not isinstance(value, str) or not value:
            raise ValueError('scan_time_zone must be a non-empty string')
        self.scanTimeZone = value

    def get_course(self):
        '''
            Get the course of the submission.
        '''
        return self.course

    def set_course(self, value):
        '''
            Set the course of the submission, for analytics.

            Parameters:
                value: `Course`.
        '''
        if not isinstance(value, Course):
            raise TypeError('value must be a `Course`')
        self.course = value

    def get_assignment(self):
        '''
            Get the assignment of the submission.
        '''
        return self.assignment

    def set_assignment(self, value):
        '''
            Set the assignment of the submission, for analytics.

            Parameters:
                value: `Assignment`.
        '''
        if not isinstance(value, Assignment):
            raise TypeError('value must be an `Assignment`')
        self.assignment = value

    def get_institution(self):
        '''
            Get the institution of the submission.
        '''
        return self.institution

    def set_institution(self, value):
        '''
            Set the institution of the submission, for analytics.

            Parameters:
                value: `Institution`.
        '''
        if not isinstance(value, Institution):
            raise TypeError('value must be an `Institution`')
        self.institution = value

    def get_sensitive_data_protection(self):
        '''
            Get the sensitive data masking settings.
        '''
        return self.sensitiveDataProtection

    def set_sensitive_data_protection(self, value):
        '''
            Mask sensitive data, such as email addresses and credit card numbers, in the scanned document.
            Available for users on a plan of 2500 pages or more.

            Parameters:
                value: `SensitiveDataProtection`.
        '''
        if not isinstance(value, SensitiveDataProtection):
            raise TypeError('value must be a `SensitiveDataProtection`')
        self.sensitiveDataProtection = value

    def get_writing_feedback(self):
        '''
            Get the Grammar Checker settings of the scan.
        '''
        return self.writingFeedback

    def set_writing_feedback(self, value):
        '''
            Run the Grammar Checker as part of the scan.

            Parameters:
                value: `WritingFeedback`.
        '''
        if not isinstance(value, WritingFeedback):
            raise TypeError('value must be a `WritingFeedback`')
        self.writingFeedback = value

    def get_overview(self):
        '''
            Get the Gen-AI Overview settings of the scan.
        '''
        return self.overview

    def set_overview(self, value):
        '''
            Generate a Gen-AI Overview with the key insights of the scan.

            Parameters:
                value: `Overview`.
        '''
        if not isinstance(value, Overview):
            raise TypeError('value must be an `Overview`')
        self.overview = value

    def get_internal_ai_source_match(self):
        '''
            Get the Internal AI Source Match settings.
        '''
        return self.internalAiSourceMatch

    def set_internal_ai_source_match(self, value):
        '''
            Find sources in the Copyleaks internal AI database that contain AI-generated text.
            Leave it unset to get the server default (disabled).

            Parameters:
                value: `InternalAISourceMatch` (an `AISourceMatch` is accepted too).
        '''
        if not isinstance(value, AISourceMatch):
            raise TypeError('value must be an `AISourceMatch`')
        self.internalAiSourceMatch = value

    def get_references(self):
        '''
            Get the Citation Checker settings.
        '''
        return self.references

    def set_references(self, value):
        '''
            Citation Checker: detect, parse and validate the references in the submitted text.

            Parameters:
                value: `References`.
        '''
        if not isinstance(value, References):
            raise TypeError('value must be a `References`')
        self.references = value
