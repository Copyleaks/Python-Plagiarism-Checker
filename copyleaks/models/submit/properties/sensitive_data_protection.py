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

class SensitiveDataProtection:
    '''
        Mask sensitive data in the scanned document with `#` characters.
        Available for users on a plan of 2500 pages or more. Unset options use the server default (False).
    '''

    @staticmethod
    def _check(value):
        if not isinstance(value, bool):
            raise TypeError('value must be True or False')
        return value

    def get_drivers_license(self):
        return self.driversLicense

    def set_drivers_license(self, value):
        '''
            Mask driver's license numbers.

            Parameters:
                value: Boolean.
        '''
        self.driversLicense = self._check(value)

    def get_credentials(self):
        return self.credentials

    def set_credentials(self, value):
        '''
            Mask credentials such as authentication tokens, cloud keys, JWTs and passwords.

            Parameters:
                value: Boolean.
        '''
        self.credentials = self._check(value)

    def get_passport(self):
        return self.passport

    def set_passport(self, value):
        '''
            Mask passport numbers.

            Parameters:
                value: Boolean.
        '''
        self.passport = self._check(value)

    def get_network(self):
        return self.network

    def set_network(self, value):
        '''
            Mask network identifiers: IP addresses and MAC addresses.

            Parameters:
                value: Boolean.
        '''
        self.network = self._check(value)

    def get_url(self):
        return self.url

    def set_url(self, value):
        '''
            Mask URLs.

            Parameters:
                value: Boolean.
        '''
        self.url = self._check(value)

    def get_email_address(self):
        return self.emailAddress

    def set_email_address(self, value):
        '''
            Mask email addresses.

            Parameters:
                value: Boolean.
        '''
        self.emailAddress = self._check(value)

    def get_credit_card(self):
        return self.creditCard

    def set_credit_card(self, value):
        '''
            Mask credit card numbers and credit card track numbers.

            Parameters:
                value: Boolean.
        '''
        self.creditCard = self._check(value)

    def get_phone_number(self):
        return self.phoneNumber

    def set_phone_number(self, value):
        '''
            Mask phone numbers.

            Parameters:
                value: Boolean.
        '''
        self.phoneNumber = self._check(value)
