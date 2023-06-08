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

import abc
from xmlrpc.client import Boolean
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

        assert value

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

        assert value

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
