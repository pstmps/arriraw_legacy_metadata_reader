# ARRI Raw Metadata Reader

[![Lint with flake8](https://github.com/pstmps/arriraw_legacy_metadata_reader/actions/workflows/lint_flake8.yml/badge.svg)](https://github.com/pstmps/arriraw_legacy_metadata_reader/actions/workflows/lint_flake8.yml)

[![Run tests with pytest](https://github.com/pstmps/arriraw_legacy_metadata_reader/actions/workflows/test_with_pytest.yml/badge.svg)](https://github.com/pstmps/arriraw_legacy_metadata_reader/actions/workflows/test_with_pytest.yml)


A Python package to read legacy ARRI Raw metadata, including a cross-platform demo CLI built with GitHub Actions.

## Features

- Read and parse ARRI Raw metadata
- Cross-platform command-line interface (CLI)
- Continuous integration with GitHub Actions

## Usage

### Command Line Interface
To use the CLI, run the following command - without any options, to enter interactive mode:

```bash
cli.py
```

or specify the following options:

```
    -i, --inputpath TEXT            Path to the directory containing the files
                                    to be processed.
    -v, --verbose                   Verbose output.
    -c, --config TEXT               Path to the config file.
    -o, --outputpath TEXT           Path to the output file.If not specified,
                                    pwd.
    -ofmt, --outputformat [json|csv|xlsx]
                                    Output format. If not specified, json.
    -f, --fields [all|minimal|default]
                                    Fields to extract. If not specified, default
                                    fields will be extracted.
    --help                          Show this message and exit.
```

#### Config file

The default config.json defines options for supported file formats and field configuration:

```json
{
    "supported_files" : ["ari", "arx"],
    "defaultfields" : ["ImageWidth", "ImageHeight", "ActiveImageLeft", "ActiveImageTop", "ActiveImageWidth", "ActiveImageHeight", "FullImageWidth", "FullImageHeigth",
    "ColorProcessingVersion", "WhiteBalance", "WhiteBalanceCC", "WBFactorR", "WBFactorG", "WBFactorB", "WBAppliedInCamera", "ExposureIndexASA", "TargetColorSpace",
    "Sharpness", "LensSqueezeFactor", "ImageOrientation", "LookName", "LookLUTMode", "LookLUTOffset", "LookLUTSize", "LookSaturation",
    "CDLSaturation", "CDLSlopeR", "CDLSlopeG", "CDLSlopeB", "CDLOffsetR", "CDLOffsetG", "CDLOffsetB", "CDLPowerR", "CDLPowerG", "CDLPowerB", "CDLMode",
    "CameraTypeId", "CameraRevision", "CameraSerialNumber", "CameraId", "CameraIndex", "SystemImageCreationDate", "SystemImageCreationTime", "SystemImageTimeZoneOffset",
    "SystemImageTimeZoneDST", "ExposureTime", "ShutterAngle", "SensorFPS", "ProjectFPS", "MasterTC", "MasterTCFrameCount", "MasterTCTimeBase",
    "StorageMediaSerialNumber", "CameraFamily", "RecorderType", "MirrorShutterRunning", "Vari", "UUID", "CameraModel", "CameraProduct", "CameraSubProduct",
    "LensDistanceUnit", "LensFocusDistance", "LensFocalLength", "LensSerialNumber", "LensLinearIris", "LensIris", "NDFilterType", "NDFilterDensity", "LensModel",
    "CameraTilt", "CameraRoll", "CircleTake", "Reel", "Scene", "Take", "Director", "Cinematographer", "Production",
    "ProductionCompany", "VarUserInfoFields", "CameraClipName",
    "FrameLineFile1", "FrameLineFile2", "FrameLine1A", "FrameLine1B", "FrameLine1C", "FrameLine2A", "FrameLine2B", "FrameLine2C"],
    "minimal" : ["ImageWidth", "ImageHeight", "ActiveImageLeft", "ActiveImageTop", "ActiveImageWidth", "ActiveImageHeight", "FullImageWidth", "FullImageHeigth",
    "WhiteBalance", "WhiteBalanceCC", "ExposureIndexASA", "ShutterAngle", "LensSqueezeFactor", "CameraModel", "CameraClipName", "MasterTC"]
}
```



### Python API
You can also use the package in your Python code:

First, instantiate a new Object:

```python
from arriraw_legacy_metadata_reader.arriraw_legacy_metadata_reader \
    import ArriRawLegacyMetadataReader

arri = ArriRawLegacyMetadataReader(file)
```

Then, get the metadata as either a dictionary, dataframe or json with the methods:

```python
metadata = arri.get_dictionary()

metadata = arri.get_dataframe()

metadata = arri.get_json()
```

Alternatively, you can limit the fields extracted by supplying a ```fields_to_extract``` list of metadata fields:

```python
arri = ArriRawLegacyMetadataReader(file, fields_to_extract=["ImageWidth", "ImageHeight", "CameraClipName"])
```





## Whitepaper

Based on the whitepaper:

https://www.arri.com/resource/blob/31912/e30dd1a324dbecbced88fa146d3f88a9/2020-11-arri-metadata-white-paper-en-data.pdf