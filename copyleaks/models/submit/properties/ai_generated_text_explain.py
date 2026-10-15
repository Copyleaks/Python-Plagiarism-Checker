class AIGeneratedTextExplain:
    '''AI Logic settings of AI detection in a scan.'''

    def get_enable(self):
        return self.enable

    def set_enable(self, value):
        '''
        Explain the AI detection with the AI patterns found. Default False. In a language AI Logic does not
        support, the scan completes without explanations and with an `ai-insights-lang-unsupported` scan alert.
        '''
        if not isinstance(value, bool):
            raise TypeError('enable must be True or False')
        self.enable = value
