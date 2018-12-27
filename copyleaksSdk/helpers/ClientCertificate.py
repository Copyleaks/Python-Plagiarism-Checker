import os

class ClientCertificate:
    '''
    Create a client certificate to use with CopyleaksIdentityApi and CopyleaksScanApi
    '''
    @staticmethod
    def get_certificate(certificate_file, key_file=None):
        '''
        Return client certificate.
        Incase certificate is stored in *.pem and *.key return certificate_file and key_file
        Incase certificate is stored in one file, return certificate_file
        '''
        assert os.path.isfile(certificate_file), f"certificate file {certificate_file} does not exists"
        if key_file is not None:
            assert os.path.isfile(key_file), f"certificate file {certificate_file} does not exists"
            return (certificate_file, key_file)
        else:
            return certificate_file
