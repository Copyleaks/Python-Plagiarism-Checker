from .HelperModels.BaseModels.StatusWebhookModel import StatusWebhookModel


class IndexedWebhookModel(StatusWebhookModel):
    """Indexed webhook. Parse it with `IndexedWebhookModel(**request.json)`."""
    __positional_fields__ = ('status',)
