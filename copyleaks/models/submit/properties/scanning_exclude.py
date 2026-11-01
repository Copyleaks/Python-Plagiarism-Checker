class ScanningExclude:
    def get_id_pattern(self):
        return self.idPattern

    def set_id_pattern(self, value):
        '''
        Leave out your submissions whose ID matches, e.g. "abc*", from batch, internal database and repository results.
        `*` matches any characters, `.` one non-whitespace character.
        '''
        if not isinstance(value, str):
            raise TypeError('id_pattern must be a string')
        if not value:
            raise ValueError('id_pattern must not be empty')

        self.idPattern = value

    def get_backlinks_domains(self):
        return self.backlinksDomains

    def set_backlinks_domains(self, value):
        '''Leave out results with backlinks to these domains: up to 10, each 1 to 256 characters.'''
        if not isinstance(value, list) or len(value) > 10:
            raise ValueError('backlinks_domains must be a list of up to 10 domains')
        if not all(isinstance(domain, str) and 1 <= len(domain) <= 256 for domain in value):
            raise ValueError('each backlinks domain must be a string of 1 to 256 characters')

        self.backlinksDomains = value

    def get_text(self):
        return self.text

    def set_text(self, value):
        '''Leave out results that contain these phrases: up to 5, each 1 to 30 characters.'''
        if not isinstance(value, list) or len(value) > 5:
            raise ValueError('text must be a list of up to 5 phrases')
        if not all(isinstance(phrase, str) and 1 <= len(phrase) <= 30 for phrase in value):
            raise ValueError('each text phrase must be a string of 1 to 30 characters')

        self.text = value
