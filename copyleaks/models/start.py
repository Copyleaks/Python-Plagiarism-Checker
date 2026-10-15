from enum import IntEnum
from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper


class Start:
    def get_trigger(self):
        return self.trigger

    def set_trigger(self, value):
        '''IDs of the scans submitted with `SubmitAction.CheckCredits` to start.'''
        assert value
        self.trigger = value

    def get_error_handling(self):
        return self.errorHandling

    def set_error_handling(self, value):
        '''`StartErrorHandling.Ignore` starts the scans even if some have errors; `Cancel` cancels the request.'''
        assert value in StartErrorHandling

        self.errorHandling = value

    def toJSON(self):
        return CopyleaksClientHelper.to_json(self)


class StartErrorHandling(IntEnum):
    Cancel = 0
    Ignore = 1
