from .SharedResultsModel import SharedResultsModel


class DatabaseModel(SharedResultsModel):
    """A result found in the Copyleaks internal database."""
    __positional_fields__ = ('tags', 'id', 'title', 'introduction', 'matched_words', 'scan_id', 'metadata')
