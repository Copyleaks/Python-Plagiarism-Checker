class References:
    '''
    Citation Checker: detect, parse and validate the references in the submitted text.
    The summary is in the completed webhook `references_validation`.
    '''

    def get_validate(self):
        return self.validate

    def set_validate(self, value):
        '''Turn the Citation Checker on. Default False.'''
        if not isinstance(value, bool):
            raise TypeError('validate must be True or False')
        self.validate = value
