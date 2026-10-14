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

from typing import Optional
from pydantic import Field

from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel


class ReferencesValidationSummaryModel(CopyleaksWebhookBaseModel):
    """
    Counts of the references that the Citation Checker detected and validated.
    """

    total: Optional[int] = Field(
        default=None,
        description="The total number of references detected in the scanned content.",
        alias="total"
    )

    academic: Optional[int] = Field(
        default=None,
        description="The number of detected references that were identified as academic.",
        alias="academic"
    )

    academic_validated: Optional[int] = Field(
        default=None,
        description="The number of academic references fully corroborated against the Copyleaks academic citation index.",
        alias="academicValidated"
    )

    non_academic_validated: Optional[int] = Field(
        default=None,
        description="The number of non-academic references fully corroborated against their cited source.",
        alias="nonAcademicValidated"
    )


class ReferencesValidationModel(CopyleaksWebhookBaseModel):
    """
    Citation Checker summary of the completed webhook, sent when `references.validate` was enabled for the scan.
    The per-reference results are in the crawled version of the scan.
    """

    summary: Optional[ReferencesValidationSummaryModel] = Field(
        default=None,
        description="An aggregated count of the references that were detected and validated.",
        alias="summary"
    )
