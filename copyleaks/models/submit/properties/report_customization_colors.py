class ReportCustomizationColors:
    def get_main_strip(self):
        return self.mainStrip

    def set_main_strip(self, value):
        '''Color of the main strip in the header.'''
        assert value

        self.mainStrip = value


    def get_titles(self):
        return self.titles

    def set_titles(self, value):
        '''Color of the titles.'''
        assert value

        self.titles = value


    def get_identical(self):
        return self.identical

    def set_identical(self, value):

        '''Highlight color of identical matches.'''
        assert value

        self.identical = value


    def get_minor_changes(self):
        return self.minorChanges

    def set_minor_changes(self, value):
        '''Highlight color of minor-change matches.'''
        assert value

        self.minorChanges = value

    def get_related_meaning(self):
        return self.relatedMeaning


    def set_related_meaning(self, value):
        '''Highlight color of related-meaning matches.'''
        assert value

        self.relatedMeaning = value

    def get_ai_detection(self):
        return self.aiDetection

    def set_ai_detection(self, value):
        '''Highlight color of AI text, in HEX. Default "#FE5758".'''
        if not value:
            raise ValueError('ai_detection is required')

        self.aiDetection = value

    def get_writing_feedback(self):
        return self.writingFeedback

    def set_writing_feedback(self, value):
        '''Highlight color of Grammar Checker corrections, in HEX. Default "#FF9A02".'''
        if not value:
            raise ValueError('writing_feedback is required')

        self.writingFeedback = value
