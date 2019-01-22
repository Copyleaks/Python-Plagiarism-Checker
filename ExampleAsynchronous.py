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

import sys

dirPath = './copyleaksSdk'
if dirPath not in sys.path:
    sys.path.insert(0, dirPath)

import uuid
import base64

from copyleaksSdk.CopyleaksIdentityApi import CopyleaksIdentityApi
from copyleaksSdk.CopyleaksScansApi import CopyleaksScansApi
from copyleaksSdk.models.types.eProduct import eProduct
from copyleaksSdk.models.requests.properties.ScanProperties import ScanProperties
from copyleaksSdk.models.types.eDomainsFilteringMode import eDomainsFilteringMode
from copyleaksSdk.models.types.eSubmitAction import eSubmitAction
from copyleaksSdk.models.types.eSubmitOutputMode import eSubmitOutputMode
from copyleaksSdk.models.requests.properties.CallbacksSection import CallbacksSection
from copyleaksSdk.models.requests.UrlDocument import UrlDocument
from copyleaksSdk.models.requests.FileDocument import FileDocument
from copyleaksSdk.models.requests.FileOcrDocument import FileOcrDocument

"""
An example of using the Copyleaks Python SDK and receiving a completion callback with the results.
"""

if __name__ == '__main__':
    """
    Change to your account credentials.
    If you don't have an account yet visit https://copyleaks.com/Account/Register
    Your API-KEY is available at your dashboard on http://api.copyleaks.com of the product that you would like to use.
    Currently available products: Businesses, Education and Websites.
    """
    identity = CopyleaksIdentityApi()
    login_response = identity.login('<YOUR_EMAIL_HERE>', '<YOUR_API_KEY_HERE>')
    api = CopyleaksScansApi(eProduct.Education, login_response.access_token)
    print(f"You've got {api.credit_balance()} Copyleaks {api.product} API credits") #get credit balance

    
    # Add the properties to your scan
    scan_properties = ScanProperties(
        # Add this scan option to your process to submit your document to full scan
        # Other possible values:
        #    eSubmitAction.Index: Upload your content to Copyleaks internal database to be compared against in future scans
        #    eSubmitAction.checkCredits: Check the amount of credits your content submit request will consume
        action = eSubmitAction.Scan,
        
        # Add this scan option to your process to use sandbox mode.
        # The process will not consume any credits and will return dummy results.
        # For more info about optional headers visit https://api.copyleaks.com/documentation/headers
        sandbox=True,

        # Add callbacks to specify the address on which you want to receive a completion callback and/or onNewResult callback
        # For testing purposes you can use https://github.com/Runscope/requestbin or any other request test server tool
        callbacks = CallbacksSection(

            # An example callback url that will be called on scan completion
            # Best practices:
            #    - It is recommended to add the scan id in the callback url to be able to match it with the submitted scan
            #    - It is recommended to add the '{STATUS}' placeholder, this placeholder will be replaced by copyleaks API with the process status
            #      Possible process statuses (Also available at enum eScanStatus):
            #        - Scanned
            #        - Failed
            #        - CreditsChecked
            #        - Indexed
            completion="http://yoursite.here/your-scanID/{STATUS}/completed-callback",

            # An example callback url that will be called when a new result is found
            onNewResult="http://yoursite.here/your-scanID/result-callback"
        )
    )
    

    print("Submitting a scan request...")
    """
    Create a scan process using one of the following methods.
    Available methods:
    submit_url, submit_file and submit_ocr
    For more information visit https://api.copyleaks.com/swagger
    """
    # Create a unique scan id
    # The scan id you provide is determined by you it usually matches the scan entity in your system
    # Each scan you submit to Copyleaks must have a unique ID and in the following format:
    #   Allowed characters: all alpha numeric characters and any of the following: !@#$^&*-+%=_()[]{}<>'";:/?.,~`|\
    #   Maximum length: 36 characters
    scan_id = uuid.uuid4()
    
    # Submit url
    url_document = UrlDocument('https://example.com', scan_properties)
    api.submit_url(scan_id, url_document)

    # Submit free text
    #file_document = FileDocument(base64=base64.b64encode(b'hello world').decode(), filename='text.txt', properties=scan_properties)
    #api.submit_file(scan_id, file_document)
    
    # submit file
    #with open('/path/to/file.docx', 'rb') as f:
    #    base64_encoded_file = base64.b64encode(f.read()).decode()
    #file_document = FileDocument(base64_encoded_file, filename="file.docx", properties=scan_properties)
    #api.submit_file(scan_id, file_document)

    # submit image file
    # with open('/path/to/image.png', 'rb') as image:
    #    base64_encoded_image = base64.b64encode(image.read()).decode()
    # file_document = FileDocument(base64_encoded_image, filename="image.png", properties=scan_properties)
    # process = api.submit_file(scan_id, file_document)

    print ("Submitted. You will receive a callback soon.")
