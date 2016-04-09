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

import unittest

from copyleaks.copyleakscloud import CopyleaksCloud
from copyleaks.models.processoptions import ProcessOptions
from copyleaks.models.eocrlanguage import eOcrLanguage

class CreateProcessTests(unittest.TestCase):


    def setUp(self):
        self.cloud = CopyleaksCloud('<YOUR_EMAIL_HERE>', '<YOUR_API_KEY_HERE>')
        self.options = ProcessOptions()
        self.options.setSandboxMode(True)
        pass


    def tearDown(self):
        pass


    def testCreateByUrl(self):
        proc = self.cloud.createByUrl('http://python.org', self.options)
        self.assertGreater(len(proc.getPID()), 0)
        pass

    def testCreateByFile(self):
        proc = self.cloud.createByFile('files/lorem.txt', self.options)
        self.assertGreater(len(proc.getPID()), 0)
        pass

    def testCreateByOcr(self):
        proc = self.cloud.createByOcr('files/lorem.jpg', eOcrLanguage.English, self.options)
        self.assertGreater(len(proc.getPID()), 0)
        pass



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreateByFile']
    unittest.main()