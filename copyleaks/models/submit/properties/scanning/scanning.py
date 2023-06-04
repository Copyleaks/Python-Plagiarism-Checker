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


class Scanning:
    def get_internet(self):
        '''
            Compare your content with online sources.
        '''
        return self.internet

    def set_internet(self, value):
        '''
            Compare your content with online sources.

            Parameters: 
                value: Boolean.
        '''
        assert value

        self.internet = value

    def get_exclude(self):
        '''
            Which results not to include on results.
        '''
        return self.exclude

    def set_exclude(self, value):
        '''
            Which results not to include on results.

            Parameters: 
                value: `ScanningExclude`.
        '''
        assert value

        self.exclude = value

    def get_repositories(self):
        '''
            Specify which repositories to scan the document against.
        '''
        return self.repositories

    def set_repositories(self, value):
        '''
            Specify which repositories to scan the document against.

            Parameters: 
                value: `SearchRepository` list.
        '''
        assert value

        self.repositories = value

    def get_copyleaks_db(self):
        '''
            Searching against Copyleaks DB source policy.
        '''
        return self.copyleaksDb

    def set_copyleaks_db(self, value):
        '''
            Searching against Copyleaks DB source policy.

            Parameters: 
                value: `ScanningCopyleaksDb`.
        '''
        assert value

        self.copyleaksDb = value

    def get_exclude(self):
        '''
            Defines which parts of the document won't be scan.
        '''
        return self.exclude

    def set_exclude(self, value):
        '''
            Defines which parts of the document won't be scan.

            Parameters: 
                value: `Exclude`.
        '''
        assert value

        self.exclude = value


    def get_cross_languages(self):

        return self.cross_languages

    def set_cross_languages(self, value):
        '''
            Cross language plagiarism detection. Choose which languages to scan your content against. 
            For each additional language chosen, your pages will be deducted per page submitted. 
            The language of the original document submitted is always scanned, 
            therefore should not be included in the additional languages chosen.

            value: Language array
        '''
        assert value

        self.cross_languages = value


    def get_copylekas_db(self):

        return self.copyleaksDb

    def set_copylekas_db(self, value):

        assert value

        self.copyleaksDb = value


