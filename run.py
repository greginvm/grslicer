import argparse

from grslicer.importers import import_file
from grslicer.slicer import slice_model
from grslicer.gcoder import encode
from grslicer.settings import settings_iter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file')
    parser.add_argument('-o', '--output', help='Output G-Code file')
    help_template = '{}: {} (default: {})'
    for group_key, prop in settings_iter():
        h = help_template.format(group_key, prop.description, prop.default)
        parser.add_argument('-' + prop.arg, '--' + prop.name, type=prop.TYPE, help=h)
    parser.parse_args()


def run(input_file, output_file, settings):
    result = import_file(input_file, settings)
    result = slice_model(result, settings)
    result = encode(result, settings, output_file)


if __name__ == "__main__":
    main()