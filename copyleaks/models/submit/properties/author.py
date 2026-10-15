class Author:
    def get_id(self):
        return self.id

    def set_id(self, value):
        '''A unique author ID. Use the same ID for the same author: their writing patterns improve the results.'''

        assert value

        self.id = value
