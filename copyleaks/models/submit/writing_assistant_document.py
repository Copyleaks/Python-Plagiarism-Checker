from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper


class WritingAssistantDocument():

    def __init__(self, text):
        assert text
        self.text = text

    def get_text(self):
        return self.text

    def set_text(self, value):
        assert value
        self.text = value

    def get_sandbox(self):
        return self.sandbox

    def set_sandbox(self, value):
        assert isinstance(value, bool)
        self.sandbox = value

    def get_language(self):
        return self.language

    def set_language(self, value):
        assert value
        self.language = value

    def get_score(self):
        return self.score

    def set_score(self, value):
        assert value is not None
        self.score = value

    def toJSON(self):
        return CopyleaksClientHelper.to_json(self)
