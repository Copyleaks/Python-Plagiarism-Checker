from typing import Optional

from pydantic import BaseModel, PrivateAttr


class CopyleaksDictAccessMixin(BaseModel):
    """
    Read-only dict-style access with the camelCase JSON keys, kept for backward compatibility:
    `response['summary']['ai']`, `response.get('explain')` and `'explain' in response` still work.
    Prefer attributes, e.g. `response.summary.ai`. Only keys the model defines and the response contained are
    available; values are plain dicts and lists. The dict is built on the first dict-style read and reused;
    setting a model attribute rebuilds it, but later changes to nested models are not seen.
    Treat responses as read-only.
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
