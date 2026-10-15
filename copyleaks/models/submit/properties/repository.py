from copyleaks.models.submit.properties.masking_policy import MaskingPolicy


class Repository:
    def get_id(self):
        return self.id

    def set_id(self, value):
        '''Repository ID, from the Admin Dashboard.'''
        assert value

        self.id = value


class SearchRepository(Repository):
    def get_include_my_submissions(self):
        return self.includeMySubmissions

    def set_include_my_submissions(self, value):
        '''Compare against your submissions in the repository.'''
        assert isinstance(value, bool)

        self.includeMySubmissions = value

    def get_include_others_submissions(self):
        return self.includeOthersSubmissions

    def set_include_others_submissions(self, value):
        '''Compare against other users' submissions in the repository.'''
        assert isinstance(value, bool)

        self.includeOthersSubmissions = value

class IndexingRepository(Repository):
    def get_masking_policy(self):
        return self.maskingPolicy

    def set_masking_policy(self, value):

        '''A `MaskingPolicy` for this document. If the repository has its own, the stricter one applies.'''
        assert value is not None and not isinstance(value, bool)
        MaskingPolicy(value)  # raises ValueError for an unknown policy

        self.maskingPolicy = value
