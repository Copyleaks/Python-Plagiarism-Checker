class Language:
    def get_code(self):
        return self.code

    def set_code(self, value):
        '''ISO-639-1 language code, see `Copyleaks.allowed_cross_languages()`.'''
        assert value

        self.code = value
