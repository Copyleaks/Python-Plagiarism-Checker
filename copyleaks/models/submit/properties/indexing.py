class Indexing:
    def get_repositories(self):
        return self.repositories

    def set_repositories(self, value):
        '''Repositories to index the document in: a list of `Repository`.'''

        assert value

        self.repositories = value

    def get_copyleaks_db(self):
        return self.copyleaksDb

    def set_copyleaks_db(self, value):
        '''Add the document to the Copyleaks Shared Data Hub. Default False.'''
        if not isinstance(value, bool):
            raise TypeError('copyleaks_db must be True or False')

        self.copyleaksDb = value
