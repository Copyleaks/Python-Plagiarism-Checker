from .SharedResultsModel import SharedResultsModel


class BatchModel(SharedResultsModel):
    """A result found in the same batch. `scan_id` is the scan id of the matching document in the batch."""
    __positional_fields__ = ('tags', 'id', 'title', 'introduction', 'matched_words', 'scan_id', 'metadata')
