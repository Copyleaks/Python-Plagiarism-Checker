from copyleaks.models.submit.score_weights import ScoreWeights


class WritingFeedback:
    '''Grammar Checker settings of a scan.'''

    def get_enable(self):
        return self.enable

    def set_enable(self, value):
        '''Run the Grammar Checker: grammar, spelling, sentence structure and word choice. Default False.'''
        if not isinstance(value, bool):
            raise TypeError('enable must be True or False')
        self.enable = value

    def get_score(self):
        return self.score

    def set_score(self, value):
        '''Weight of each correction category in the score, a `ScoreWeights`.'''
        if not isinstance(value, ScoreWeights):
            raise TypeError('value must be a `ScoreWeights`')
        self.score = value
