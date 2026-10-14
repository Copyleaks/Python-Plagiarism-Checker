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

from typing import Any, Tuple

from pydantic import ConfigDict

from copyleaks.helpers.copyleaks_dict_access_mixin import CopyleaksDictAccessMixin


def str_or_number_to_str(value):
    """Accept a number where the API documents a string id, and return it as a string."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    return value


def none_to_empty_list(value):
    """Treat a null list as an empty list."""
    return [] if value is None else value


class CopyleaksWebhookBaseModel(CopyleaksDictAccessMixin):
    """
    Base of the webhook models. `Model(**request.json)` parses the camelCase webhook JSON into typed models.

    - Fields are snake_case attributes, for example `scanned_document.scan_id`.
      The snake_case names are accepted as constructor arguments too.
    - Fields that the model does not define are kept, and are returned by `model_dump(by_alias=True)`
      and by dict-style access.
    - Read-only dict-style access with the camelCase JSON keys still works, for example
      `completed.results['internet'][0]['url']`.
    """

    model_config = ConfigDict(populate_by_name=True, extra='allow', protected_namespaces=())

    __positional_fields__: Tuple[str, ...] = ()

    def __init__(self, *args: Any, **data: Any):
        if args:
            names = type(self).__positional_fields__
            if len(args) > len(names):
                raise TypeError(f"{type(self).__name__} takes at most {len(names)} positional arguments "
                                f"({len(args)} given)")
            for name, value in zip(names, args):
                if name in data:
                    raise TypeError(f"{type(self).__name__} got multiple values for argument '{name}'")
                data[name] = value
        super().__init__(**data)
