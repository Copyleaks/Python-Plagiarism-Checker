from xmlrpc.client import Boolean
from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper


class Delete:
    def get_scans(self):
        return self.scans

    def set_scans(self, value):
        '''Scans to delete: a list of `DeleteScan`.'''

        assert value

        self.scans = value

    def get_purge(self):
        return self.purge

    def set_purge(self, value):
        '''Also delete the scans from the internal database, so they are no longer results of other scans.'''

        assert value != None and type(value) is Boolean 

        self.purge = value

    def get_completion_webhook(self):
        return self.completionWebhook

    def set_completion_webhook(self, value):
        '''URL that gets a POST, with no body, when the deletion completes.'''

        assert value

        self.completionWebhook = value

    def get_headers(self):
        return self.headers

    def set_headers(self, value):
        '''Custom headers of the completion webhook, as [name, value] pairs, e.g. [["Authorization", "..."]].'''
        if not isinstance(value, list) or not all(isinstance(pair, (list, tuple)) and len(pair) == 2 for pair in value):
            raise ValueError('headers must be a list of [name, value] pairs')

        self.headers = [list(pair) for pair in value]

    def toJSON(self):
        return CopyleaksClientHelper.to_json(self)


class DeleteScan:
    def __init__(self, id):
        self.set_id(id)

    def get_id(self):
        return self.id

    def set_id(self, value):
        assert value

        self.id = value
