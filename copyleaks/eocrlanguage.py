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

from enum import Enum

"""
Deprecated
Use cloud.getSupportedOcrLanguages() instead to get the update list of ocr languages.
"""


class eOcrLanguage(Enum):
    Afrikaans = 'Afrikaans'
    Albanian = 'Albanian' 
    Basque='Basque' 
    Brazilian='Brazilian'
    Bulgarian='Bulgarian'
    Byelorussian='Byelorussian'
    Catalan='Catalan'
    Chinese_Simplified ='Chinese_Simplified'
    Chinese_Traditional='Chinese_Traditional'
    Croatian='Croatian'
    Czech='Czech'
    Danish='Danish'
    Dutch='Dutch'
    English='English'
    Esperanto='Esperanto'
    Estonian='Estonian'
    Finnish='Finnish'
    French='French'
    Galician='Galician'
    German='German'
    Greek='Greek'
    Hungarian='Hungarian'
    Icelandic='Icelandic'
    Indonesian='Indonesian'
    Italian='Italian'
    Japanese='Japanese'
    Korean='Korean'
    Latin='Latin'
    Latvian='Latvian'
    Lithuanian='Lithuanian'
    Macedonian='Macedonian'
    Malay='Malay'
    Moldavian='Moldavian'
    Norwegian='Norwegian'
    Polish='Polish'
    Portuguese='Portuguese'
    Romanian='Romanian'
    Russian='Russian'
    Serbian='Serbian'
    Slovak='Slovak'
    Slovenian='Slovenian'
    Spanish='Spanish'
    Swedish='Swedish'
    Tagalog='Tagalog'
    Turkish='Turkish'
    Ukrainian='Ukrainian'
