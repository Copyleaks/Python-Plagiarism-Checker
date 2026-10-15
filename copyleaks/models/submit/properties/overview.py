class Overview:
    '''Gen-AI Overview: key insights from the scan data. Unset options use the server default (False).'''

    @staticmethod
    def _check(value):
        if not isinstance(value, bool):
            raise TypeError('value must be True or False')
        return value

    def get_enable(self):
        return self.enable

    def set_enable(self, value):
        '''Generate the Gen-AI Overview.'''
        self.enable = self._check(value)

    def get_ignore_ai_detection(self):
        return self.ignoreAIDetection

    def set_ignore_ai_detection(self, value):
        '''Leave AI detection out of the overview.'''
        self.ignoreAIDetection = self._check(value)

    def get_ignore_plagiarism_detection(self):
        return self.ignorePlagiarismDetection

    def set_ignore_plagiarism_detection(self, value):
        '''Leave plagiarism detection out of the overview.'''
        self.ignorePlagiarismDetection = self._check(value)

    def get_ignore_writing_feedback(self):
        return self.ignoreWritingFeedback

    def set_ignore_writing_feedback(self, value):
        '''Leave the Grammar Checker out of the overview.'''
        self.ignoreWritingFeedback = self._check(value)

    def get_ignore_author_data(self):
        return self.ignoreAuthorData

    def set_ignore_author_data(self, value):
        '''Leave the author's historical data out of the overview.'''
        self.ignoreAuthorData = self._check(value)
