class CopyleaksDb:
    def get_include_my_submissions(self):
        return self.includeMySubmissions

    def set_include_my_submissions(self, value):
        '''Compare against your submissions in the Copyleaks internal database.'''
        assert isinstance(value, bool)

        self.includeMySubmissions = value

    def get_include_others_submissions(self):
        return self.includeOthersSubmissions

    def set_include_others_submissions(self, value):
        '''Compare against other users' submissions in the Copyleaks internal database.'''
        assert isinstance(value, bool)

        self.includeOthersSubmissions = value
