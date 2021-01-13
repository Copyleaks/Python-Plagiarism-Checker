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

from copyleaks.models.submit.properties.domains_mode import DomainsMode


class Filters:
    def get_identical_enabled(self):
        '''
            Should enable matching of exact words in the text.
        '''
        return self.identicalEnabled

    def set_identical_enabled(self, value):
        '''
            Should enable matching of exact words in the text.

            Parameters: 
                value: Boolean.
        '''
        assert value is not None

        self.identicalEnabled = value

    def get_minor_changes_enabled(self):
        '''
            Should enable matching of nearly identical words with small differences like "slow" becomes "slowly".
        '''
        return self.minorChangesEnabled

    def set_minor_changes_enabled(self, value):
        '''
            Should enable matching of nearly identical words with small differences like "slow" becomes "slowly".

            Parameters: 
                value: Boolean.
        '''
        assert value is not None

        self.minorChangesEnabled = value

    def get_minor_changes_enabled(self):
        '''
            Should enable matching of paraphrased content stating similar ideas with different words.
        '''
        return self.relatedMeaningEnabled

    def set_related_meaning_enabled(self, value):
        '''
            Should enable matching of paraphrased content stating similar ideas with different words.

            Parameters: 
                value: Boolean.
        '''
        assert value is not None

        self.relatedMeaningEnabled = value

    def get_min_copied_words(self):
        '''
            Select results with at least N copied words.
        '''
        return self.minCopiedWords

    def set_min_copied_words(self, value):
        '''
            Select results with at least N copied words.

            Parameters: 
                value: Unsigned Integer.
        '''
        assert value

        self.minCopiedWords = value

    def get_safe_search(self):
        '''
            Block explicit adult content from the scan results such as web pages containing inappropriate images and videos. 
            `SafeSearch` is not 100% effective with all websites.
        '''
        return self.safeSearch

    def set_safe_search(self, value):
        '''
            Block explicit adult content from the scan results such as web pages containing inappropriate images and videos. 
            `SafeSearch` is not 100% effective with all websites.

            Parameters: 
                value: Boolean.
        '''
        assert value

        self.safeSearch = value

    def get_domains(self):
        '''
            A list of domains to either include or exclude from the scan - depending on the value of `domainsMode`.
        '''
        return self.domains

    def set_domains(self, value):
        '''
            A list of domains to either include or exclude from the scan - depending on the value of `domainsMode`.

            Parameters: 
                value: String array.
        '''
        assert value

        self.domains = value

    def get_domains_mode(self):
        '''
            "Include" or "Exclude" the list of domains you specified under the domains property
        '''
        return self.domainsMode

    def set_domains_mode(self, value):
        '''
            "Include" or "Exclude" the list of domains you specified under the domains property

            Parameters: 
                value: `DomainsMode` enum.
        '''
        assert value in DomainsMode

        self.domainsMode = value
