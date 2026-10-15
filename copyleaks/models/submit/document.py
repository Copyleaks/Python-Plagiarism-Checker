from abc import ABC
from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper


class Document(ABC):

    def get_properties(self):
        return self.properties

    def set_properties(self, value):
        self.properties = value

    def toJSON(self):
        return CopyleaksClientHelper.to_json(self)


class FileDocument(Document):
    def __init__(self, base64, filename):
        self.set_base64(base64)
        self.set_filename(filename)

    def get_base64(self):
        return self.base64

    def set_base64(self, value):
        assert value
        self.base64 = value

    def get_filename(self):
        return self.filename

    def set_filename(self, value):
        assert value
        self.filename = value


class OcrFileDocument(FileDocument):
    def get_language(self):
        return self.langCode

    def set_language(self, value):
        self.langCode = value


class UrlDocument(Document):
    def get_url(self):
        return self.url

    def set_url(self, value):
        self.url = value

    def get_verb(self):
        return self.verb

    def set_verb(self, value):
        '''HTTP method Copyleaks uses to fetch the URL: "GET" (default), "POST" or "PUT".'''
        if not isinstance(value, str) or value.upper() not in ('GET', 'POST', 'PUT'):
            raise ValueError('verb must be "GET", "POST" or "PUT"')
        self.verb = value.upper()

    def get_headers(self):
        return self.headers

    def set_headers(self, value):
        '''
        Headers Copyleaks sends when it fetches the URL, as [name, value] pairs; they replace the default headers.
        Use `Set-Cookie` for cookies, e.g. [["Authorization", "Bearer my-token"], ["Set-Cookie", "session=abc"]].
        '''
        if not isinstance(value, list) or not all(isinstance(pair, (list, tuple)) and len(pair) == 2 for pair in value):
            raise ValueError('headers must be a list of [name, value] pairs')
        self.headers = [list(pair) for pair in value]
