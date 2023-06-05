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


class Pdf:

    def get_create(self):
        '''
            Returns whether to create PDF report or not.
        '''
        return self.create

    def set_create(self, value):
        '''
            Set whether to create PDF report or not.

            Parameters: 
                value: Boolean.
        '''
        assert value

        self.create = value

    def get_title(self):
        '''
            Customize the title for the PDF report.
        '''
        return self.title

    def set_title(self, value):
        '''
            Customize the title for the PDF report.

            Parameters: 
                value: String.
        '''
        assert value

        self.title = value

    def get_large_logo_base64(self):
        '''
            Customize the logo image in the PDF report.
        '''
        return self.largeLogo

    def set_large_logo_base64(self, value):
        '''
            Customize the logo image in the PDF report.

            Parameters: 
                value: String.
        '''
        assert value

        self.largeLogo = value
    

    def get_rtl(self):
        '''
            When set to true the text in the report will be aligned from right to left.
        '''
        return self.rtl

    def set_rtl(self, value):
        '''
            When set to true the text in the report will be aligned from right to left.

            Parameters: 
                value: Boolean.
        '''
        assert value

        self.rtl = value


    def get_version(self):
        '''
            Get PDF version to generate
        '''
        return self.version

    def set_version(self, value):
        '''
            Set PDF version to generate

            value: `PdfVersion` enum
        '''
        assert value

        self.version = value


    def get_report_customization_colors(self):
        '''
            Customizable colors
        '''
        return self.report_customization_colors

    def set_report_customization_colors(self, value):
        '''
            Set customizable colors

            value: `ReportCustomizationColors`
        '''
        assert value

        self.report_customization_colors = value
