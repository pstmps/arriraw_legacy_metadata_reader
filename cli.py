"""
Command line interface for the arriraw_legacy_metadata_reader package.
"""
import os
import sys
import json
from pathlib import Path

import click
import pandas as pd

from arriraw_legacy_metadata_reader.arriraw_legacy_metadata_reader \
    import ArriRawLegacyMetadataReader


def validate_json(json_object: str, keys: list) -> list:
    """
    Validates a JSON object against a list of keys.
    Args:
        json_object: JSON object to validate.
        keys: List of keys to check for.
    Returns:
        List of missing keys.
    """
    # Check which keys are missing in the JSON object
    missing_keys = [key for key in keys if key not in json_object]
    return missing_keys


def load_config(file: str, keys: list = None) -> dict:
    """
    Loads a JSON config file and validates it against a list of keys.
    Args:
        file: Path to the JSON config file.
        keys: List of keys to check for.
    Returns:
        JSON config file as a dictionary.
    """
    if keys is None:
        keys = []
    try:
        with open(file=file, encoding='UTF8') as f:
            config = json.load(f)
    except Exception as e:
        raise FileNotFoundError(f"Error loading {file}. Original error: {str(e)}") from e
    missing_keys = validate_json(config, keys)
    if missing_keys:
        print("Invalid config file. Missing keys: ", missing_keys)
    return config


def find_files(path: str, extensions: list, ignore_multipart: bool = True) -> list:
    """
    Function to find files with a given extension in a directory.
    Args:
        path: Path to the directory to search.
        extensions: List of extensions to search for.
    Returns:
        Path to the file.
    """
    file_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(tuple(extensions)):
                file_paths.append(os.path.join(root, file))
                if ignore_multipart:
                    break
    if not file_paths:
        raise FileNotFoundError(f"No files with the extensions {' '.join(extensions)} were found.")
    return file_paths


def write_file(outputformat: str, outputfile: str, output: dict) -> None:
    """
    Writes the output to a file.
    Args:
        outputformat: Output format.
        outputfile: Path to the output file.
        output: Output dictionary.
    """
    if outputformat == 'csv':
        df = pd.DataFrame.from_dict(output, orient='index')
        df.to_csv(outputfile, sep='\t')
    elif outputformat == 'xlsx':
        df = pd.DataFrame.from_dict(output, orient='index')
        df.to_excel(outputfile)
    else:
        with open(file=outputfile, mode='w', encoding='UTF8') as f:
            json.dump(output, f, indent=4)


def print_to_console(output: dict) -> None:
    """
    Prints the output to the console.
    Args:
        output: Output dictionary.
    """
    for key, value in output.items():
        click.echo(f'Key: {key:32} -- Value: {value}')

# pylint: disable=E1120


@click.command()
@click.option('--inputpath', '-i',
              help='Path to the directory containing the files to be processed.',
              prompt='Path to the directory containing the files to be processed.')
@click.option('--verbose', '-v',
              help='Verbose output.', is_flag=True)
@click.option('--config', '-c',
              help='Path to the config file.',
              default='defaultconfig')
@click.option('--outputpath', '-o',
              help='Path to the output file.If not specified, pwd.')
@click.option('--outputformat', '-ofmt',
              help='Output format. If not specified, json.',
              type=click.Choice(['json', 'csv', 'xlsx']),
              default='json')
@click.option('--fields', '-f',
              help='Fields to extract. If not specified, default fields will be extracted.',
              type=click.Choice(['all', 'minimal', 'default']),
              default='default')
def run(inputpath, verbose, config, outputpath, outputformat, fields):
    """
    Main function for the CLI.
    Args:
        inputpath: Path to the directory containing the files to be processed.
        verbose: Verbose output.
        config: Path to the config file.
        outputpath: Path to the output file.
        outputformat: Output outputformat.
        fields: Fields to extract.
    """

    if outputpath is None:
        outputpath = os.getcwd()

    if config == 'defaultconfig':
        # Find out if we are ruinning as a PyInstaller bundle or as a standalone script
        if getattr(sys, 'frozen', False):
            # The application is running as a PyInstaller bundle
            config = Path(getattr(sys, '_MEIPASS', Path(sys.executable).parent)) / 'config.json'
        else:
            # The application is running as a standalone Python script
            config = Path('config.json')

    loaded_config = load_config(config, ["supported_files", "defaultfields"])
    supported_files = loaded_config["supported_files"]

    if fields == 'default':
        fields = loaded_config["defaultfields"]
    elif fields == 'minimal':
        fields = loaded_config["minimal"]
    elif fields == 'all':
        fields = None

    output = {}

    inputpath = inputpath.strip('\'').strip('\"')
    click.echo(f'Input path: {inputpath}')

    files = find_files(path=inputpath, extensions=supported_files)
    if not files:
        raise FileNotFoundError("No files with the given extensions were found.")

    for file in files:

        click.echo(f'Processing: {file}')
        filename = os.path.splitext(os.path.basename(file))[0]
        arri = ArriRawLegacyMetadataReader(file, fields_to_extract=fields)
        output[filename] = arri.get_dictionary()

        if verbose:
            print_to_console(output[filename])

        outputfile = os.path.join(outputpath, f'{filename}.{outputformat}')
        write_file(outputformat, outputfile, output[filename])


if __name__ == "__main__":

    run()
