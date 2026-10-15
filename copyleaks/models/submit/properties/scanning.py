class Scanning:
    def get_internet(self):
        return self.internet

    def set_internet(self, value):
        '''Compare against online sources.'''
        assert isinstance(value, bool)

        self.internet = value

    def get_exclude(self):
        return self.exclude

    def set_exclude(self, value):
        '''Results to leave out, a `ScanningExclude`.'''
        assert value

        self.exclude = value

    def get_repositories(self):
        return self.repositories

    def set_repositories(self, value):
        '''Repositories to compare against: a list of `SearchRepository`.'''
        assert value

        self.repositories = value

    def get_copyleaks_db(self):
        return self.copyleaksDb

    def set_copyleaks_db(self, value):
        '''Compare against the Copyleaks internal database, a `ScanningCopyleaksDb`.'''
        assert value

        self.copyleaksDb = value

    def get_cross_languages(self):
        return self.crossLanguages

    def set_cross_languages(self, value):
        '''A `CrossLanguages`; get the language codes with `Copyleaks.allowed_cross_languages()`.'''
        assert value

        self.crossLanguages = value

    def get_include(self):
        return self.include

    def set_include(self, value):
        '''A `ScanningInclude`.'''
        if not value:
            raise ValueError('include is required')

        self.include = value

    def get_copylekas_db(self):
        '''Deprecated misspelled name of `get_copyleaks_db`.'''
        return self.get_copyleaks_db()

    def set_copylekas_db(self, value):
        '''Deprecated misspelled name of `set_copyleaks_db`.'''
        self.set_copyleaks_db(value)
