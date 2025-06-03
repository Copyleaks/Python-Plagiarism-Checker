from typing import Optional, Any
from .HelperModels.BaseModels.StatusWebhookModel import StatusWebhookModel
from .HelperModels.ErrorModels.ErrorModel import ErrorModel

class ErrorWebhookModel(StatusWebhookModel):
    """
    Represents a webhook payload indicating an error occurred during processing.
    Inherits from StatusWebhook and contains an Error object.
    """
    error: Optional[ErrorModel] = None

    def __init__(self,
                 error: Optional[ErrorModel] = None,
                 status: Optional[int] = None,
                 **kwargs: Any):
        """
        Initializes an ErrorWebhook object.
        """
        super().__init__(status=status, **kwargs)
        self.error = error