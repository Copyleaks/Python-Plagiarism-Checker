from datetime import datetime, timedelta
import dateutil.parser
import pytz
from copyleaks.exceptions.auth_expired_error import AuthExipredError

class CopyleaksClientHelper:
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
