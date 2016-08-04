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

import time
import sys
dirPath = './copyleaks'
if dirPath not in sys.path:
    sys.path.insert(0, dirPath)

from copyleakscloud import CopyleaksCloud
from processoptions import ProcessOptions
from product import Product


if __name__ == '__main__':
    
    #edit your login credentials.
    cloud = CopyleaksCloud(Product.Businesses, '<YOUR_EMAIL_HERE>', '<YOUR_API_KEY_HERE>')
    
    print("You've got %s Copyleaks %s API credits" % (cloud.getCredits(), cloud.getProduct())) #get credit balance
    
    options = ProcessOptions()
    options.setSandboxMode(True) #scan in sandbox mode

    print("Submitting a scan request...")

    process = cloud.createByUrl('http://python.com', options)
    #process = cloud.createByOcr('ocr-example.jpg', eOcrLanguage.English, options)
    #process = cloud.createByFile('test.txt', options)
    
    print ("Submitted. In progress...")
    iscompleted = False
    while not iscompleted:
        [iscompleted, percents] = process.isCompleted() #get process status
        print ('%s%%' % (percents))
        if not iscompleted:
            time.sleep(3)
    
    print ("Finished!")
    
    results = process.getResutls() #get scan results
    print ('\nFound %s results...\n' % (len(results)))
    for result in results:
        print ('URL: %s' % (result.getUrl()))
        print ('NumberOfCopiedWords: %s' % (result.getNumberOfCopiedWords()))
        print ('Percents: %s' % (result.getPercents()))
        print ('')
    
    pass
