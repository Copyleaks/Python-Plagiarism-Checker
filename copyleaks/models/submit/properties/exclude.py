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


class Exclude:
    def get_quotes(self):
        '''
            Exclude quoted text from the scan.
        '''
        return self.quotes

    def set_quotes(self, value):
        '''
            Exclude quoted text from the scan.

            Parameters: 
                value: Boolean.
        '''
        assert value

        self.quotes = value

    def get_references(self):
        '''
            Exclude referenced text from the scan.
        '''
        return self.references

    def set_references(self, value):
        '''
            Exclude referenced text from the scan.

            Parameters: 
                value: Boolean.
        '''
        assert value

        self.references = value

    def get_table_of_content(self):
        '''
            Exclude referenced text from the scan.
        '''
        return self.tableOfContents

    def set_table_of_content(self, value):
        '''
            Exclude referenced text from the scan.

            Parameters: 
                value: Boolean.
        '''
        assert value

        self.tableOfContents = value

    def get_titles(self):
        '''
            Exclude titles from the scan.
        '''
        return self.titles

    def set_titles(self, value):
        '''
            Exclude titles from the scan.

            Parameters: 
                value: Boolean.
        '''
        assert value

        self.titles = value

    def get_html_template(self):
        '''
            When the scanned document is an HTML document, exclude irrelevant text that appears across the site like the website footer or header.
        '''
        return self.htmlTemplate

    def set_html_template(self, value):
        '''
            When the scanned document is an HTML document, exclude irrelevant text that appears across the site like the website footer or header.

            Parameters: 
                value: Boolean.
        '''
        assert value

        self.htmlTemplate = value

    def get_citations(self):
        '''
            Get whether citations are excluded from the scan.
        '''
        return self.citations

    def set_citations(self, value):
        '''
            Set exclude citations from the scan.

            value: Boolean
        '''
        assert value

        self.citations = value


    def get_document_template_ids(self):
        '''
            Get document template Ids. 
        '''
        return self.documentTemplateIds

    def set_document_template_ids(self, value):
        '''
            Exclude text based on text found within other documents. 
            Specify an array of scan ids containing text to exclude from your scan's text. 
            Each scan ID specified should be in a completed success state and should not have expired at the time of submission.

            value: String array
        '''
        self.documentTemplateIds = value


    def get_code(self):
        '''
            Exclude sections of source code
        '''
        return self.code

    def set_code(self, value):
        '''
            set exclude code settings

            value: `ExcludeCode`
        '''
        assert value

        self.code = value
