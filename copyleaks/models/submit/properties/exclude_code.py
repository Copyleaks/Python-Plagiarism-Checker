class ExcludeCode:
    def get_comments(self):
        return self.comments

    def set_comments(self, value):
        '''Exclude code comments.'''
        assert isinstance(value, bool)

        self.comments = value
