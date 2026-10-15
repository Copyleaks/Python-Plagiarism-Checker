from copyleaks.models.submit.properties.ai_source_match import AISourceMatch


class InternalAISourceMatch(AISourceMatch):
    '''
    Find sources in the Copyleaks internal AI database that contain AI-generated text.
    The matches are in the completed webhook `results.internal_ai_data`.
    '''

    def set_enable(self, value):
        '''Search the Copyleaks internal AI database. Default False.'''
        if not isinstance(value, bool):
            raise TypeError('enable must be True or False')

        self.enable = value
