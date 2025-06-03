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

from typing import Any, Optional
from .HelperModels.BaseModels.StatusWebhookModel import StatusWebhookModel
from .HelperModels.CompletedModels.ScannedDocumentModel import ScannedDocumentModel

class CreditsCheckedWebhookModel(StatusWebhookModel):
    """
    Represents a webhook payload indicating credits have been checked/charged
    for a scan. Inherits from StatusWebhook.
    Corresponds to the Java class:
    models.submissions.Webhooks.CreditsCheckedWebhook
    """
    credits: Optional[int] = None
    scanned_document: Optional[ScannedDocumentModel] = None

    def __init__(self,
                 credits: Optional[int] = None,
                 scanned_document: Optional[ScannedDocumentModel] = None,
                 status: Optional[int] = None,
                 **kwargs: Any):
        """
        Initializes a CreditsCheckedWebhook object.

        Args:
            credits: Credits charged for the scan.
            scanned_document: A ScannedDocument object with info about the scan.
            status: Status code passed to the StatusWebhook parent.
            **kwargs: Additional keyword arguments passed up to the StatusWebhook
                      (and potentially its base BaseModel) constructor.
                      e.g., developer_payload='...'
        """
        super().__init__(status=status, **kwargs)
        self.credits = credits
        self.scanned_document = scanned_document