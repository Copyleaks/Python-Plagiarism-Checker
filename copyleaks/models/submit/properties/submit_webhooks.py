class SubmitWebhooks:
    def get_new_result(self):
        return self.newResult

    def set_new_result(self, value):
        '''URL called with each new result while the scan runs.'''
        assert value

        self.newResult = value

    def get_status(self):
        return self.status

    def set_status(self, value):
        '''URL called when the scan status changes.'''
        assert value

        self.status = value

    def get_status_headers(self):
        return self.statusHeaders

    def set_status_headers(self, value):
        '''Headers of the status webhook, as [name, value] pairs.'''
        assert isinstance(value, list)
        self.statusHeaders = value

    def get_new_result_headers(self):
        return self.newResultHeaders

    def set_new_result_headers(self, value):
        '''Headers of the new result webhook, as [name, value] pairs.'''
        assert isinstance(value, list)
        self.newResultHeaders = value
