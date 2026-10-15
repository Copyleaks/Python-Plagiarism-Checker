from copyleaks.models.submit.properties.domains_mode import DomainsMode


class Filters:
    def get_identical_enabled(self):
        return self.identicalEnabled

    def set_identical_enabled(self, value):
        '''Match identical words.'''
        assert value is not None

        self.identicalEnabled = value

    def get_minor_changes_enabled(self):
        return self.minorChangesEnabled

    def set_minor_changes_enabled(self, value):
        '''Match nearly identical words, e.g. "slow" and "slowly".'''
        assert value is not None

        self.minorChangesEnabled = value

    def get_related_meaning_enabled(self):
        return self.relatedMeaningEnabled

    def set_related_meaning_enabled(self, value):
        '''Match paraphrased content: similar ideas in different words.'''
        assert value is not None

        self.relatedMeaningEnabled = value

    def get_min_copied_words(self):
        return self.minCopiedWords

    def set_min_copied_words(self, value):
        '''Return only results with at least this many copied words.'''
        assert value

        self.minCopiedWords = value

    def get_safe_search(self):
        return self.safeSearch

    def set_safe_search(self, value):
        '''Block explicit adult content from the results. Not 100% effective on every website.'''
        assert isinstance(value, bool)

        self.safeSearch = value

    def get_domains(self):
        return self.domains

    def set_domains(self, value):
        '''Domains to include or exclude, see `set_domains_mode`.'''
        assert value

        self.domains = value

    def get_domains_mode(self):
        return self.domainsMode

    def set_domains_mode(self, value):
        '''Whether `domains` are included or excluded: a `DomainsMode`.'''
        assert value in DomainsMode

        self.domainsMode = value

    def get_allow_same_domain(self):
        return self.allowSameDomain

    def set_allow_same_domain(self, value):
        '''Allow results from the domain of the submitted URL.'''
        assert value is not None

        self.allowSameDomain = value
