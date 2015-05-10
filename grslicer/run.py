from grslicer.importers import import_file
from grslicer.slicer import slice_model
from grslicer.gcoder import encode
from grslicer.settings import SlicerSettings
from grslicer.util.progress import progress_log


@progress_log('Slicing')
def slicing(input_file, output_file, input_settings_file, input_settings_dict, output_settings_file, progress):
    progress.set_size(5)

    settings = SlicerSettings(file_name=input_settings_file,
                              flat_settings_dict=input_settings_dict)
    progress.inc()

    if output_settings_file is not None:
        settings.write_file(output_settings_file)

    progress.inc()

    result = import_file(input_file, settings)

    progress.inc()

    result = slice_model(result, settings)

    progress.inc()

    result = encode(result, settings, output_file)

    progress.done()
    return result

