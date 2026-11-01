import json
from datetime import datetime, timedelta, timezone

import dateutil.parser

from copyleaks.consts import Consts
from copyleaks.exceptions.auth_expired_error import AuthExipredError


class CopyleaksClientHelper:
    @staticmethod
    def verify_auth_token(auth_token):
        assert auth_token and auth_token['.expires'] and auth_token['access_token']

        now = datetime.now(timezone.utc) + timedelta(0, 5 * 60)  # 5-minute safety margin
        upTo = dateutil.parser.parse(auth_token['.expires'])
        if upTo.tzinfo is None:
            upTo = upTo.replace(tzinfo=timezone.utc)

        if upTo <= now:
            raise AuthExipredError()

    @staticmethod
    def headers(auth_token=None, content_type='application/json'):
        '''The SDK User-Agent, plus `Authorization` and `Content-Type` when given.'''
        headers = {'User-Agent': Consts.USER_AGENT}
        if content_type:
            headers['Content-Type'] = content_type
        if auth_token is not None:
            headers['Authorization'] = f"Bearer {auth_token['access_token']}"
        return headers

    @staticmethod
    def to_json(obj):
        '''Compact JSON of a request object and its nested objects.'''
        return json.dumps(obj, default=lambda o: o.__dict__, separators=(',', ':'))

    @staticmethod
    def to_json_bytes(obj):
        '''UTF-8 JSON body of a request object; uses its `toJSON()` when it has one.'''
        if hasattr(obj, 'toJSON'):
            text = obj.toJSON()
        else:
            text = CopyleaksClientHelper.to_json(obj)
        return text.encode('utf-8')

    @staticmethod
    def model_to_json_bytes(model):
        '''JSON body of a pydantic request model: camelCase keys, unset optional fields left out.'''
        return model.model_dump_json(by_alias=True, exclude_none=True).encode('utf-8')
