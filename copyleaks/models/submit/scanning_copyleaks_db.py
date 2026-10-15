class ScanningCopyleaksDb:
    def get_include_my_submissions(self):
        return self.includeMySubmissions

    def set_include_my_submissions(self, value):
        '''Also compare against your submissions in the Copyleaks internal database; the scan is indexed there too.'''
        assert isinstance(value, bool)

        self.includeMySubmissions = value

    def get_include_others_submissions(self):
        return self.includeOthersSubmissions

    def set_include_others_submissions(self, value):
        '''Also compare against other users' submissions in the internal database; the scan is indexed there too.'''
        assert isinstance(value, bool)

        self.includeOthersSubmissions = value
