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
from pydantic import ConfigDict, Field

from copyleaks.helpers.copyleaks_dict_access_mixin import CopyleaksDictAccessMixin


class CopyleaksRepositoryInfoResponseModel(CopyleaksDictAccessMixin):
    """
    Information about a Private Cloud Hub repository. This is the response of `Copyleaks.repository_info`.
    Missing fields are None.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: Optional[str] = Field(
        default=None,
        description="The repository ID.",
        alias="id"
    )

    name: Optional[str] = Field(
        default=None,
        description="The repository name.",
        alias="name"
    )

    description: Optional[str] = Field(
        default=None,
        description="The repository description.",
        alias="description"
    )

    permission: Optional[int] = Field(
        default=None,
        description="Your role in the repository: 1 = Viewer, 2 = Contributor, 3 = Admin, 4 = Super Admin. "
                    "See `CopyleaksRepositoryRoles`.",
        alias="permission"
    )

    status: Optional[int] = Field(
        default=None,
        description="Repository status: 0 = Running, 1 = Pending For Deletion, 2 = Error, 3 = Updating, "
                    "4 = Payment Required. See `CopyleaksRepositoryStatuses`.",
        alias="status"
    )

    max_credits: Optional[int] = Field(
        default=None,
        description="The credit limit of the repository.",
        alias="maxCredits"
    )

    current_credits: Optional[int] = Field(
        default=None,
        description="The credits currently used by the repository.",
        alias="currentCredits"
    )

    masking_policy: Optional[int] = Field(
        default=None,
        description="Masking policy: 0 = No Masking, 1 = Mask Other User Documents, 2 = Mask All Documents. See `MaskingPolicy`.",
        alias="maskingPolicy"
    )

    creation_time: Optional[str] = Field(
        default=None,
        description="When the repository was created.",
        alias="creationTime"
    )
