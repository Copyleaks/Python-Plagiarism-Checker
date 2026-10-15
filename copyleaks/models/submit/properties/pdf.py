class Pdf:

    def get_create(self):
        return self.create

    def set_create(self, value):
        '''Create a PDF report.'''
        assert isinstance(value, bool)

        self.create = value

    def get_title(self):
        return self.title

    def set_title(self, value):
        '''Title of the PDF report.'''
        assert value

        self.title = value

    def get_large_logo_base64(self):
        return self.largeLogo

    def set_large_logo_base64(self, value):
        '''Logo of the PDF report, base64-encoded.'''
        assert value

        self.largeLogo = value
    

    def get_rtl(self):
        return self.rtl

    def set_rtl(self, value):
        '''Align the report text right to left.'''
        assert isinstance(value, bool)

        self.rtl = value


    def get_version(self):
        return self.version

    def set_version(self, value):
        '''Deprecated: use `set_report_version`, which overrides it. A `PdfVersion`.'''
        assert value

        self.version = value


    def get_report_version(self):
        return self.reportVersion

    def set_report_version(self, value):
        '''"v1", "v2", "v3" or "latest": lowercase strings, not `PdfVersion`. Overrides `version`; needs `create`.'''
        assert isinstance(value, str) and value

        self.reportVersion = value


    def get_report_customization_colors(self):
        return self.colors

    def set_report_customization_colors(self, value):
        '''Colors of the PDF report, a `ReportCustomizationColors`. Sent as `pdf.colors`.'''
        assert value

        self.colors = value

    def get_colors(self):
        '''Same as `get_report_customization_colors`.'''
        return self.colors

    def set_colors(self, value):
        '''Same as `set_report_customization_colors`.'''
        self.set_report_customization_colors(value)
