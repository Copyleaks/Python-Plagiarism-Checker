class SensitiveDataProtection:
    '''
    Mask sensitive data in the scanned document with `#` characters. Needs a plan of 2500 pages or more.
    Unset options use the server default (False).
    '''

    @staticmethod
    def _check(value):
        if not isinstance(value, bool):
            raise TypeError('value must be True or False')
        return value

    def get_drivers_license(self):
        return self.driversLicense

    def set_drivers_license(self, value):
        '''Mask driver's license numbers.'''
        self.driversLicense = self._check(value)

    def get_credentials(self):
        return self.credentials

    def set_credentials(self, value):
        '''Mask credentials such as authentication tokens, cloud keys, JWTs and passwords.'''
        self.credentials = self._check(value)

    def get_passport(self):
        return self.passport

    def set_passport(self, value):
        '''Mask passport numbers.'''
        self.passport = self._check(value)

    def get_network(self):
        return self.network

    def set_network(self, value):
        '''Mask IP and MAC addresses.'''
        self.network = self._check(value)

    def get_url(self):
        return self.url

    def set_url(self, value):
        '''Mask URLs.'''
        self.url = self._check(value)

    def get_email_address(self):
        return self.emailAddress

    def set_email_address(self, value):
        '''Mask email addresses.'''
        self.emailAddress = self._check(value)

    def get_credit_card(self):
        return self.creditCard

    def set_credit_card(self, value):
        '''Mask credit card numbers and credit card track numbers.'''
        self.creditCard = self._check(value)

    def get_phone_number(self):
        return self.phoneNumber

    def set_phone_number(self, value):
        '''Mask phone numbers.'''
        self.phoneNumber = self._check(value)
