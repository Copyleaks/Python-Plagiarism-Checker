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
    '''
    Customizable colors for Copyleaks scan result report

    Attributes:
    -----------
        mainStrip : string (HTML color code)
            The color of the main strip in the header
        titles : string (HTML color code)
            The color for titles in copyleaks result report
        identical: string (HTML color code)
            The highlight color for identical matches
        minorChanges: string (HTML color code)
            The highlight color for minor changes matches
        relatedMeaning: string (HTML color code)
            The highlight color for related meaning matches    
    '''
    def __init__(self, mainStrip, titles, identical, minorChanges, relatedMeaning):
        self.mainStrip = mainStrip
        self.titles = titles
        self.identical = identical
        self.minorChanges = minorChanges
        self.relatedMeaning = relatedMeaning