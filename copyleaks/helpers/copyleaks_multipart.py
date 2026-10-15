import mimetypes


class CopyleaksMultipart:
    """Helpers to build multipart/form-data requests with `requests`."""

    @staticmethod
    def bool_field(value):
        """A boolean form field value: "true" or "false"."""
        return 'true' if value else 'false'

    @staticmethod
    def file_part(filename, content):
        """
        The `files=` entry of an upload: (filename, content, content type). `content` is bytes or a binary file object,
        read when the request is sent.
        """
        if isinstance(content, (bytearray, memoryview)):
            content = bytes(content)
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        return (filename, content, content_type)
