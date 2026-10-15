class Assignment:
    '''The assignment of the submission, for analytics.'''

    def __init__(self, id=None):
        if id is not None:
            self.set_id(id)

    def get_id(self):
        return self.id

    def set_id(self, value):
        '''A unique assignment ID.'''
        if not value:
            raise ValueError('id is required')
        self.id = value
