from abc import ABC
from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper


class AiDetectionDocument(ABC):
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
        self.sandbox = value

    def toJSON(self):
        return CopyleaksClientHelper.to_json(self)


class NaturalLanguageDocument(AiDetectionDocument):
    def __init__(self, text):
        super().__init__(text)

    def get_language(self):
        return self.language

    def set_language(self, value):
        self.language = value

    def get_explain(self):
        return self.explain

    def set_explain(self, value):
        """AI Logic: the response gets `explain`, the AI patterns found. Supported languages only; default False."""
        if not isinstance(value, bool):
            raise TypeError('explain must be True or False')
        self.explain = value

    def get_sensitivity(self):
        return self.sensitivity

    def set_sensitivity(self, value):
        """1 to 3: 1 finds unedited AI text, 2 (default) also minor edits, 3 also heavily modified text."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError('sensitivity must be an integer')
        if not 1 <= value <= 3:
            raise ValueError('sensitivity must be from 1 to 3')
        self.sensitivity = value
