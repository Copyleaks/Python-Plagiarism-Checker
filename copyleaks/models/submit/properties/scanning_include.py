class ScanningInclude:
    '''Which of your submissions to include in the internal database and repository results.'''

    def get_id_pattern(self):
        return self.idPattern

    def set_id_pattern(self, value):
        '''
        Include only your submissions whose ID matches, e.g. "course-a-*".
        `*` matches any characters, `.` one non-whitespace character.
        '''
        if not isinstance(value, str) or not value:
            raise ValueError('id_pattern must be a non-empty string')
        self.idPattern = value
