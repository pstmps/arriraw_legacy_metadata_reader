"""
Defines the FLI class, which defines the FLI metadata block in ARRIRAW files.
"""
from arriraw_legacy_metadata_reader.binaryfiledto import BinaryFileDTO


class Fli(BinaryFileDTO):
    """
    Class to read the FLI information from an ARRIRAW file.
    """

    def __init__(self, file, fields_to_extract=None):
        super().__init__(file, fields_to_extract=fields_to_extract)
        self.fields = [
            {'name': 'FLIValid', 'offset': 0x0718, 'datatype': 'I',
             'endianness': '<'},  # 188
            {'name': 'FrameLineFile1', 'offset': 0x0850, 'datatype': 'string',
             'length': 32},
            {'name': 'FrameLineFile2', 'offset': 0x0870, 'datatype': 'string',
             'length': 32},
            {'name': 'FrameLine1A', 'offset': 0x0890, 'datatype': 'frameline',
             'number': '1A'},
            {'name': 'FrameLine1B', 'offset': 0x08C0, 'datatype': 'frameline',
             'number': '1B'},
            {'name': 'FrameLine1C', 'offset': 0x08F0, 'datatype': 'frameline',
             'number': '1C'},
            {'name': 'FrameLine2A', 'offset': 0x0920, 'datatype': 'frameline',
             'number': '2A'},
            {'name': 'FrameLine2B', 'offset': 0x0950, 'datatype': 'frameline',
             'number': '2B'},
            {'name': 'FrameLine2C', 'offset': 0x0980, 'datatype': 'frameline',
             'number': '2C'},
        ]
        self.data = self.extract_metadata()
