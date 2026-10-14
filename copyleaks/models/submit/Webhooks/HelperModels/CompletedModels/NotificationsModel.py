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

from typing import List
from pydantic import Field, field_validator

from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel
from ..NotificationsModels.AlertsModel import AlertsModel


class NotificationsModel(CopyleaksWebhookBaseModel):
    """A list of scan alerts that were detected in the scan."""
    __positional_fields__ = ('alerts',)

    alerts: List[AlertsModel] = Field(
        default_factory=list,
        description="Scan alerts that were detected in the scan.",
        alias="alerts"
    )

    @field_validator('alerts', mode='before')
    @classmethod
    def alerts_drop_none(cls, v):
        """Skip null alert entries, so one null entry does not fail the whole webhook."""
        if v is None:
            return []
        if isinstance(v, (list, tuple)):
            return [alert for alert in v if alert is not None]
        return v
