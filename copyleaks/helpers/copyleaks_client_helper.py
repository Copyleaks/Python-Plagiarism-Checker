from datetime import datetime, timedelta
import dateutil.parser
import pytz
from copyleaks.consts import Consts
from copyleaks.exceptions.auth_expired_error import AuthExipredError

class CopyleaksClientHelper:
    @staticmethod
    def add_tenant_header(headers, x_tenant=None):
        '''
            Add the `x-tenant` header to the request headers, if a tenant is set.
            When no tenant is set, the header is not added.
            Passing `x_tenant=""` skips the header for that call, even when a process-wide tenant is set.

            Parameters:
                headers: dict. The request headers. Updated in place.
                x_tenant: string. Optional per-call tenant. Overrides the process-wide tenant set with `Copyleaks.set_tenant`.
        '''
        tenant = x_tenant if x_tenant is not None else Consts.TENANT
        if tenant:
            headers['x-tenant'] = tenant

    @staticmethod
    def verify_auth_token(auth_token):
        '''
            Verify that Copyleaks authentication token is exists and not expired.

            Parameters:
                auth_token: Copyleaks authentication token

            Raises:
                `AuthExipredError`: authentication expired. Need to login again.
        '''
        assert auth_token and auth_token['.expires'] and auth_token['access_token']

        now = pytz.UTC.localize(datetime.utcnow() + timedelta(0, 5 * 60))  # adds 5 minutes ahead for a safety shield.
        upTo = dateutil.parser.parse(auth_token['.expires'])

        if upTo <= now:
            raise AuthExipredError()  # expired
