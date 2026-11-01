class Exclude:
    def get_quotes(self):
        return self.quotes

    def set_quotes(self, value):
        '''Exclude quoted text from the scan.'''
        assert isinstance(value, bool)

        self.quotes = value

    def get_references(self):
        return self.references

    def set_references(self, value):
        '''Exclude referenced text from the scan.'''
        assert isinstance(value, bool)

        self.references = value

    def get_table_of_content(self):
        return self.tableOfContents

    def set_table_of_content(self, value):
        '''Exclude the table of contents from the scan.'''
        assert isinstance(value, bool)

        self.tableOfContents = value

    def get_titles(self):
        return self.titles

    def set_titles(self, value):
        '''Exclude titles from the scan.'''
        assert isinstance(value, bool)

        self.titles = value

    def get_html_template(self):
        return self.htmlTemplate

    def set_html_template(self, value):
        '''For HTML documents, exclude text repeated across the site, such as the header and footer.'''
        assert isinstance(value, bool)

        self.htmlTemplate = value

    def get_citations(self):
        return self.citations

    def set_citations(self, value):
        '''Exclude citations from the scan.'''
        assert isinstance(value, bool)

        self.citations = value


    def get_document_template_ids(self):
        return self.documentTemplateIds

    def set_document_template_ids(self, value):
        '''Exclude the text of these scans: IDs of completed scans that have not expired.'''
        self.documentTemplateIds = value


    def get_code(self):
        return self.code

    def set_code(self, value):
        '''Source code exclusion settings, an `ExcludeCode`.'''
        assert value

        self.code = value
