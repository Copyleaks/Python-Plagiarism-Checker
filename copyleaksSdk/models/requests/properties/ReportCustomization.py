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


class ReportCustomization:
    '''
    Specify customized attributes for Copyleaks scan results report

    Attributes:
    -----------
        Title : string
           Customizable title
        LargeLogo : base64 string
            Customizable logo for the header of the report.
            The logo should be in string base64 format.
        SmallLogo : base64 string
            Customizable logo for the footer of the report.
            The logo should be in string base64 format.
        RTL : boolean
            Customizable direction of text.
            When set to true the direction of the text will be from right to lef
        colors : ReportCustomizationColors
            Customizable colors
    '''
    def __init__(self, create,title, largeLogo, smallLogo, rtl, colors):
        self.Create = create
        self.Title = title
        self.LargeLogo = largeLogo
        self.SmallLogo = smallLogo
        self.RTL = rtl
        if colors:
            self.Colors = colors