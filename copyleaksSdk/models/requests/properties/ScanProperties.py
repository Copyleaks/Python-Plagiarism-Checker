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

from copyleaksSdk.models.types.eDomainsFilteringMode import eDomainsFilteringMode
from copyleaksSdk.models.types.eSubmitAction import eSubmitAction
from copyleaksSdk.models.types.eSubmitOutputMode import eSubmitOutputMode
from copyleaksSdk.models.types.eScanPriority import eScanPriority

class ScanProperties:
    '''
    The scan request properties

    Attributes:
        action: eSubmitAction
            The type of action to submit
        outputMode: eSubmitOutputMode
            The output of the scan results
        developerPayload : string
            Custom developer payload that will be attached to the scan results
        priority : eScanPriority
            The priority of the scan, lower priority will consume less credits and take longer to yield results 
        sandbox: boolean
            set true to enable sandbox mode, used for development
        callbacks: CallbacksSection
            Register your HTTP callback endpoints with Copyleaks API
        expiration: int (days)
            The expiration time of the scan, when expired the scan results will be deleted from Copyleak's servers
            The maximum allowed value is 2880 (~ 4 month)
        exclude: ExcludeSection
            Exclude properties from scan
        filters: Filters
            Customizeable filters
        author: Author
            Represent the author of the submitted content
    '''
    def __init__(self, 
                action=eSubmitAction.Scan, 
                outputMode=eSubmitOutputMode.TXT, 
                developerPayload=None,
                priority=eScanPriority.Normal,
                sandbox=False, 
                callbacks=None, 
                expiration=2880, 
                exclude=None, 
                filters=None, 
                author=None, 
                reportExport=None):
        self.action = action
        self.outputMode = outputMode
        self.developerPayload = developerPayload
        self.sandbox = sandbox
        self.priority = priority    
        if callbacks:
            self.callbacks = callbacks
        self.expiration = expiration
        if exclude:
            self.exclude = exclude
        if filters:
            self.filters = filters
        if author:
            self.author = author
