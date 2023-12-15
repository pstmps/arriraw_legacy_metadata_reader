from arriraw_legacy_metadata_reader.arriraw_legacy_metadata_reader import ArriRawLegacyMetadataReader
import json
import os
import click
import pandas as pd

def validate_json(json_obj, keys):
    # Check which keys are missing in the JSON object
    missing_keys = [key for key in keys if key not in json_obj]
    return missing_keys

def load_config(file, keys=[]):
    try:
        config = json.load(open(file))
    except:
        raise Exception(f"Error loading {file}")
    missing_keys = validate_json(config, keys)
    if missing_keys:
        print("Invalid config file. Missing keys: ", missing_keys)
    return config

def find_files(path, extensions):
    file_found = False
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(tuple(extensions)):
                yield os.path.join(root, file)
                file_found = True
                break
    if not file_found:
        raise FileNotFoundError("No files with the given extensions were found.")

@click.command()
@click.option('--inputpath', '-i', 
              help='Path to the directory containing the files to be processed.', 
              prompt='Path to the directory containing the files to be processed.')
@click.option('--verbose', '-v',
                help='Verbose output.'
                ,is_flag=True)
@click.option('--config', '-c',
                help='Path to the config file.',
                default='config.json')
@click.option('--outputpath', '-o',
                help='Path to the output file.If not specified, pwd.')
@click.option('--format', '-fmt',
                help='Output format. If not specified, json.',
                type=click.Choice(['json', 'csv', 'xlsx']),
                default='json')
@click.option('--fields', '-f',
                help='Fields to extract. If not specified, default fields will be extracted.',
                type=click.Choice(['all', 'minimal', 'default']),
                default='default')
def run(inputpath, verbose, config, outputpath, format, fields):

    if outputpath is None:
        outputpath = os.getcwd()

    outputfile = os.path.join(outputpath, f'metadata.{format}')
    
    loaded_config = load_config(config, ["supported_files", "defaultfields"])

    supported_files = loaded_config["supported_files"]

    if fields == 'default':
        fields = loaded_config["defaultfields"]
    elif fields == 'minimal':
        fields = load_config["minimal"]
    elif fields == 'all':
        fields = None

    output = {}

    for file in find_files(inputpath.strip('\'').strip('\"'), supported_files):

        filename = os.path.splitext(os.path.basename(file))[0]
        arri = ArriRawLegacyMetadataReader(file, fields_to_extract=fields)
        output[filename] = arri.get_dictionary()

    if verbose:
        click.echo(f'Input path: {output}')

    if format == 'csv':
        df = pd.DataFrame.from_dict(output, orient='index')
        df.to_csv(outputfile,sep='\t')
    elif format == 'xlsx':
        df = pd.DataFrame.from_dict(output, orient='index')
        df.to_excel(outputfile)
    else:
        with open(outputfile, 'w') as f:
            json.dump(output, f, indent=4)

if __name__ == "__main__":

    run()
