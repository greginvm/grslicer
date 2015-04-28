from stl import StlAsciiImporter, StlBinImporter

ALL_IMPORTERS = [StlAsciiImporter, StlBinImporter]


class SlicerImportException(Exception):
    pass


def import_file(file_path, settings):
    result = None
    with open(file_path, 'r') as f:
        contents = f.read()

        for importer_cls in ALL_IMPORTERS:
            if importer_cls.can_import(contents):
                importer = importer_cls(contents, settings)
                result = importer.import_contents()
                break
        if result is None:
            raise SlicerImportException('The provided file can not be imported')
        else:
            result.center(settings.printPlateWidth, settings.printPlateLength)
    return result

