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

from copyleaksSdk.models.responses.download.MatchRanges import MatchRanges

class SuspectedComparisonResults:
    '''

    Attributes:
    -----------
        groupId: array
            The matches group id
            In case of html the matched text can be seperated by html elements which are not part of the text.
            In order to properly show the compared text the group id is used to get a sequential match.
        source: MatchRanges
            The match ranges of your content
        suspected: MatchRanges
            The match ranges of the suspected result
        
    '''
    def __init__(self, data):
        self.groupId = data.get('groupId', [])
        self.source = MatchRanges(data.get('source', {}))
        self.suspected = MatchRanges(data.get('suspected', {}))
