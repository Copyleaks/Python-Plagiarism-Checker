class AISourceMatch:
    def get_enable(self):
        return self.enable

    def set_enable(self, value):
        '''Find online sources suspected of AI-generated text. English documents only; default False.'''
        assert isinstance(value, bool)

        self.enable = value
