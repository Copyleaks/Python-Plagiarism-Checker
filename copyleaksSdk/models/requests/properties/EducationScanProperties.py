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

from copyleaksSdk.models.requests.properties.ScanProperties import ScanProperties
from copyleaksSdk.models.types.eDomainsFilteringMode import eDomainsFilteringMode
from copyleaksSdk.models.types.eSubmitAction import eSubmitAction
from copyleaksSdk.models.types.eScanPriority import eScanPriority

class EducationScanProperties(ScanProperties):
    '''
    The scan request properties for Education product

    Attributes:
        action: eSubmitAction
            The type of action to submit
        includeHtml: boolean
            When set to true the output mode of the report will be in HTML format
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
        scanning: Scanning
            Defines which mediums to scan.
        exclude: ExcludeSection
            Exclude properties from scan
        filters: Filters
            Customizeable filters
        author: Author
            Represent the author of the submitted content
        pdf: ReportCustomization
            Configuration for the results report
            If left as None a report will not be generated
    '''
    def __init__(self,
                 action=eSubmitAction.Scan,
                 includeHtml=False,
                 developerPayload=None,
                 priority=eScanPriority.Normal,
                 sandbox=False,
                 callbacks=None,
                 expiration=2880,
                 scanning=None,
                 exclude=None,
                 filters=None,
                 author=None,
                 pdf=None):

        self.scanning = scanning
        self.pdf = pdf
        ScanProperties.__init__(self,
                                action,
                                includeHtml,
                                developerPayload,
                                priority,
                                sandbox,
                                callbacks,
                                expiration,
                                exclude,
                                filters,
                                author)
