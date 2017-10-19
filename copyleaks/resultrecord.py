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

class ResultRecord(object):
    '''
    A result which found by Copyleaks cloud
    '''


    def __init__(self, dic):
        self.__setUrl(dic['URL'])
        self.__setPercents(dic['Percents'])
        self.__setNumberOfCopiedWords(dic['NumberOfCopiedWords'])
        self.__setComparisonReport(dic['ComparisonReport'])
        self.__setCachedVersion(dic['CachedVersion'])
        self.__setTitle(dic['Title'])
        self.__setIntroduction(dic['Introduction'])
        self.__setEmbededComparison(dic['EmbededComparison'])
        
    def getUrl(self):
        return self.Url
    def __setUrl(self, value):
        self.Url = value
        
    def getPercents(self):
        return self.Percents
    def __setPercents(self, value):
        self.Percents = value
    
    def getNumberOfCopiedWords(self):
        return self.NumberOfCopiedWords
    def __setNumberOfCopiedWords(self, value):
        self.NumberOfCopiedWords = value
    
    def getComparisonReport(self):
        return self.ComparisonReport
    def __setComparisonReport(self, value):
        self.ComparisonReport = value
    
    def getCachedVersion(self):
        return self.CachedVersion
    def __setCachedVersion(self, value):
        self.CachedVersion = value
        
    def getTitle(self):
        if not hasattr(self, 'Title') or self.Title == None:
            return ""
        else:
            return self.Title
    def __setTitle(self, value):
        self.Title = value
    
    def getIntroduction(self):
        return self.Introduction
    def __setIntroduction(self, value):
        self.Introduction = value

    def getEmbededComparison(self):
        return self.EmbededComparison
    def __setEmbededComparison(self, value):
        self.EmbededComparison = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'URL: %s\n' % (self.getUrl()) +\
               'Title: %s\n' % (self.getTitle()) +\
               'Introduction: %s\n' % (self.getIntroduction()) +\
               'Information: %s copied words (%s%%)\n' % (self.getNumberOfCopiedWords(), self.getPercents()) +\
               'Embed Comparison: %s\n' % (self.getEmbededComparison()) +\
               'Comparison Link: %s\n' % (self.getEmbededComparison()) +\
               'Cached Version: %s' % (self.getCachedVersion())

    @staticmethod
    def parseResults(results):
        lst = []
        for result in results:
            lst.append(ResultRecord(result))
        
        return lst