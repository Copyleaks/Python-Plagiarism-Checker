from typing import Any, Tuple

from pydantic import ConfigDict

from copyleaks.helpers.copyleaks_dict_access_mixin import CopyleaksDictAccessMixin


def str_or_number_to_str(value):
    """Accept a number where the API documents a string id, and return it as a string."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    return value


def none_to_empty_list(value):
    return [] if value is None else value


class CopyleaksWebhookBaseModel(CopyleaksDictAccessMixin):
    """
    Base of the webhook models: `Model(**request.json)` parses the camelCase JSON into snake_case attributes, which
    are accepted as constructor arguments too. Undefined fields are kept, in `model_dump(by_alias=True)` and in
    read-only dict-style access with the camelCase keys, e.g. `completed.results['internet'][0]['url']`.
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
