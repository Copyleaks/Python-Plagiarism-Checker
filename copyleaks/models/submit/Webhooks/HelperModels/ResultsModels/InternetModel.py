from ..NewResultModels.NewResultInternetModel import NewResultsInternetModel


class InternetModel(NewResultsInternetModel):
    """A result found on the internet, in the completed webhook."""
    # The 5.x positional order. Internet results have no scan id: a `scan_id` passed here is kept as an extra field.
    __positional_fields__ = ('tags', 'id', 'title', 'introduction', 'matched_words', 'scan_id', 'metadata', 'url')
