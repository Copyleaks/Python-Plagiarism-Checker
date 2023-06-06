class Language:
    def get_code(self):
        '''
            Get language code for cross language plagiarism detection.
        '''
        return self.code

    def set_code(self, value):
        '''
            Set language code for cross language plagiarism detection.

            value: string
        '''
        assert value

        self.code = value
