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

class ReportCustomizationColors:
    def get_main_strip(self):
        return self.main_strip

    def set_main_strip(self, value):
        assert value

        self.main_strip = value


    def get_titles(self):
        return self.titles

    def set_titles(self, value):
        assert value

        self.titles = value


    def get_identical(self):
        return self.identical

    def set_identical(self, value):
        assert value

        self.identical = value


    def get_minor_changes(self):
        return self.minor_changes

    def set_minor_changes(self, value):
        assert value

        self.minor_changes = value

    def get_related_meaning(self):
        return self.related_meaning


    def set_related_meaning(self, value):
        assert value

        self.related_meaning = value