"""
Defines the SID class, which defines the SID metadata block in ARRIRAW files.
"""

from arriraw_legacy_metadata_reader.binaryfiledto import BinaryFileDTO


class Sid(BinaryFileDTO):
    """
    Class to read the SID information from an ARRIRAW file.
    """

    def __init__(self, file, fields_to_extract=None):
        super().__init__(file, fields_to_extract=fields_to_extract)
        self.fields = [
            {
                "name": "SIDValid",
                "offset": 0x0718,
                "datatype": "I",
                "endianness": "<",
            },  # 188
            {
                "name": "SoundTC",
                "offset": 0x071C,
                "datatype": "timecode",
                "endianness": "<",
            },
            {
                "name": "SoundFileName",
                "offset": 0x072C,
                "datatype": "string",
                "length": 32,
            },
            {
                "name": "SoundRollName",
                "offset": 0x074C,
                "datatype": "string",
                "length": 32,
            },
            {
                "name": "SoundSceneName",
                "offset": 0x076C,
                "datatype": "string",
                "length": 32,
            },
            {
                "name": "SoundTakeName",
                "offset": 0x078C,
                "datatype": "string",
                "length": 32,
            },
            {"name": "AudioInfo", "offset": 0x07AC, "datatype": "string", "length": 32},
        ]
        self.data = self.extract_metadata()
