from copyleaks.models.submit.properties.ai_generated_text_explain import AIGeneratedTextExplain


class AIGeneratedText:
    def get_detect(self):
        return self.detect
        

    def set_detect(self, value):
        '''Detect AI-generated text.'''
        assert isinstance(value, bool)

        self.detect = value

    def get_sensitivity(self):
        return self.sensitivity

    def set_sensitivity(self, value):
        '''1 to 3: 1 finds unedited AI text, 2 (default) also minor edits, 3 also heavily modified text.'''
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError('sensitivity must be an integer')
        if not 1 <= value <= 3:
            raise ValueError('sensitivity must be from 1 to 3')

        self.sensitivity = value

    def get_explain(self):
        return self.explain

    def set_explain(self, value):
        '''AI Logic settings, an `AIGeneratedTextExplain`.'''
        if not isinstance(value, AIGeneratedTextExplain):
            raise TypeError('value must be an `AIGeneratedTextExplain`')

        self.explain = value
