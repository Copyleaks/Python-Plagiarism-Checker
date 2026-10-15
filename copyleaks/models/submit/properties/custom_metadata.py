class CustomMetadata:
    def get_key(self):
        return self.key

    def set_key(self, value):
        assert value

        self.key = value

    def get_value(self):
        return self.value

    def set_value(self, value):
        assert value

        self.value = value
        