from abc import ABC
from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper


class Export:
    def get_completion_webhook(self):
        return self.completionWebhook

    def set_completion_webhook(self, value):
        '''URL that gets a POST when the export completes, see `ExportCompletedWebhookModel`.'''

        assert value

        self.completionWebhook = value

    def get_completion_webhook_headers(self):
        return self.completionWebhookHeaders

    def set_completion_webhook_headers(self, value):
        '''Custom headers of the completion webhook, as [name, value] pairs.'''
        if not isinstance(value, list) or not all(isinstance(pair, (list, tuple)) and len(pair) == 2 for pair in value):
            raise ValueError('headers must be a list of [name, value] pairs')

        self.completionWebhookHeaders = [list(pair) for pair in value]

    def get_max_retries(self):
        return self.maxRetries

    def set_max_retries(self, value):
        '''Retries before giving up, 1 to 12. More can delay the completion webhook; fewer can fail on an outage.'''

        assert value and value >= 1 and value <= 12

        self.maxRetries = value

    def get_developer_payload(self):
        return self.developerPayload

    def set_developer_payload(self, value):
        '''Custom string, up to 512 characters, returned in the export completed webhook.'''

        assert value and len(value) <= 512

        self.developerPayload = value

    def get_results(self):
        return self.results

    def set_results(self, value):
        '''Results to export: a list of `ExportResult`.'''

        assert value

        self.results = value

    def get_pdf_report(self):
        return self.pdfReport

    def set_pdf_report(self, value):
        '''Export the PDF report, an `ExportPdf`. Needs `properties.pdf.create` on the submission.'''

        assert value

        self.pdfReport = value

    def get_crawled_version(self):
        return self.crawledVersion

    def set_crawled_version(self, value):
        '''Export the crawled version of the submitted text, an `ExportCrawledVersion`.'''

        assert value

        self.crawledVersion = value

    def get_ai_detection(self):
        return self.aiDetection

    def set_ai_detection(self, value):
        '''Export the AI detection report, an `ExportAiDetection`. Needs `properties.aiGeneratedText.detect`.'''

        if not value:
            raise ValueError('ai_detection is required')

        self.aiDetection = value

    def get_writing_feedback(self):
        return self.writingFeedback

    def set_writing_feedback(self, value):
        '''Export the Grammar Checker report, an `ExportWritingFeedback`. Needs `properties.writingFeedback.enable`.'''

        if not value:
            raise ValueError('writing_feedback is required')

        self.writingFeedback = value

    def get_overview(self):
        return self.overview

    def set_overview(self, value):
        '''Export the Gen-AI Overview report, an `ExportOverview`. Needs `properties.overview.enable`.'''

        if not value:
            raise ValueError('overview is required')

        self.overview = value

    def toJSON(self):
        return CopyleaksClientHelper.to_json(self)


class ExportItem(ABC):
    def get_endpoint(self):
        return self.endpoint

    def set_endpoint(self, value):
        '''URL that Copyleaks uploads the data to.'''

        assert value

        self.endpoint = value

    def get_verb(self):
        return self.verb

    def set_verb(self, value):
        '''HTTP method of the upload to `endpoint`.'''

        assert value

        self.verb = value

    def get_headers(self):
        return self.headers

    def set_headers(self, value):
        '''Headers of the upload request, such as "Authorization", as [name, value] pairs.'''

        assert value

        self.headers = value


class ExportResult(ExportItem):
    def get_id(self):
        return self.id

    def set_id(self, value):
        '''ID of the result to export, from the completed webhook.'''

        assert value

        self.id = value


class ExportPdf(ExportItem):
    def __init__(self):
        pass


class ExportCrawledVersion(ExportItem):
    def __init__(self):
        pass


class ExportAiDetection(ExportItem):
    def __init__(self):
        pass


class ExportWritingFeedback(ExportItem):
    def __init__(self):
        pass


class ExportOverview(ExportItem):
    def __init__(self):
        pass
