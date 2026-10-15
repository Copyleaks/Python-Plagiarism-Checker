class CrossLanguages:
    def get_languages(self):
        return self.languages

    def set_languages(self, value):
        '''
        Extra languages to scan against: a list of `Language`. Each one is charged per page submitted.
        Leave out the document's own language, which is always scanned.
        '''
        assert value

        self.languages = value
