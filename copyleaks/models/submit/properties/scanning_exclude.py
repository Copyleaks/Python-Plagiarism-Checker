'''
 The MIT License(MIT)

 Copyright(c) 2016 Copyleaks LTD (https://copyleaks.com)

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
'''


class ScanningExclude:
    def get_id_pattern(self):
        '''
            Exclude your submissions from results if their id matches the supplied pattern. Matched submissions will be excluded from batch, internal database and repositories results.
        '''
        return self.idPattern

    def set_id_pattern(self, value):
        '''
            Exclude your submissions from results if their id matches the supplied pattern. Matched submissions will be excluded from batch, internal database and repositories results.

            `*` matches any number of characters and `.` matches exactly one non-whitespace character.

            Parameters: 
                value: String. For example "abc*".
        '''
        if not isinstance(value, str):
            raise TypeError('id_pattern must be a string')
        if not value:
            raise ValueError('id_pattern must not be empty')

        self.idPattern = value

    def get_backlinks_domains(self):
        '''
            Domains whose backlinks exclude a result.
        '''
        return self.backlinksDomains

    def set_backlinks_domains(self, value):
        '''
            Exclude results that contain backlinks to these domains.

            Parameters:
                value: List of up to 10 domains, each 1 to 256 characters.
        '''
        if not isinstance(value, list) or len(value) > 10:
            raise ValueError('backlinks_domains must be a list of up to 10 domains')
        if not all(isinstance(domain, str) and 1 <= len(domain) <= 256 for domain in value):
            raise ValueError('each backlinks domain must be a string of 1 to 256 characters')

        self.backlinksDomains = value

    def get_text(self):
        '''
            Phrases that exclude a result.
        '''
        return self.text

    def set_text(self, value):
        '''
            Exclude results that contain text matching these phrases.

            Parameters:
                value: List of up to 5 phrases, each 1 to 30 characters.
        '''
        if not isinstance(value, list) or len(value) > 5:
            raise ValueError('text must be a list of up to 5 phrases')
        if not all(isinstance(phrase, str) and 1 <= len(phrase) <= 30 for phrase in value):
            raise ValueError('each text phrase must be a string of 1 to 30 characters')

        self.text = value
