class ModelImporter(object):
    """
        Interface for importers
    """

    def __init__(self, contents, settings):
        self.contents = contents
        self.merger = None
        self.settings = settings

    @staticmethod
    def can_import(contents):
        return False

    def import_contents(self):
        pass
