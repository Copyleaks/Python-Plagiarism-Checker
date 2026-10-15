def _validate_weight(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError('score weights must be numbers')
    if not 0.0 <= value <= 1.0:
        raise ValueError('score weights must be from 0.0 to 1.0')


class ScoreWeights:
    """
    Weights of the correction categories in the overall Grammar Checker score, each from 0.0 to 1.0.
    0.0 ignores the category; unset weights use the server default (1.0).
    """

    def get_grammar_score_weight(self):
        return self.grammarScoreWeight

    def set_grammar_score_weight(self, value):
        _validate_weight(value)
        self.grammarScoreWeight = value

    def get_mechanics_score_weight(self):
        return self.mechanicsScoreWeight

    def set_mechanics_score_weight(self, value):
        _validate_weight(value)
        self.mechanicsScoreWeight = value

    def get_sentence_structure_score_weight(self):
        return self.sentenceStructureScoreWeight

    def set_sentence_structure_score_weight(self, value):
        _validate_weight(value)
        self.sentenceStructureScoreWeight = value

    def get_word_choice_score_weight(self):
        return self.wordChoiceScoreWeight

    def set_word_choice_score_weight(self, value):
        _validate_weight(value)
        self.wordChoiceScoreWeight = value
