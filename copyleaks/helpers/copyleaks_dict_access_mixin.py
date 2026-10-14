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

from pydantic import BaseModel, PrivateAttr


class CopyleaksDictAccessMixin(BaseModel):
    """
    Read-only dict-style access for pydantic response models of endpoints that used to return the raw JSON dict,
    so existing code such as `response['summary']['ai']`, `response.get('explain')` and `'explain' in response`
    keeps working.

    Keys are the camelCase JSON keys. Values are plain dicts and lists, as in the JSON response.
    Only keys that the model defines and that were present in the response are available.
    Kept for backward compatibility; prefer attribute access, e.g. `response.summary.ai`.

    The dict is built once, on the first dict-style read, and reused by later reads. Setting an attribute of
    the model itself rebuilds it on the next read. Treat responses as read-only: changes made to nested
    models after the first dict-style read are not reflected in dict-style reads.
    """

    _dict_access_cache: Optional[dict] = PrivateAttr(default=None)

    def _to_response_dict(self):
        cache = self._dict_access_cache
        if cache is None:
            cache = self.model_dump(by_alias=True, exclude_unset=True)
            self._dict_access_cache = cache
        return cache

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if not name.startswith('_'):
            self._dict_access_cache = None

    def model_copy(self, *, update=None, deep=False):
        copied = super().model_copy(update=update, deep=deep)
        copied._dict_access_cache = None
        return copied

    def __getitem__(self, key):
        return self._to_response_dict()[key]

    def get(self, key, default=None):
        return self._to_response_dict().get(key, default)

    def __contains__(self, key):
        return key in self._to_response_dict()
