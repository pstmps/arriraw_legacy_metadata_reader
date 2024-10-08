"""
Defines the IDI class, which defines the IDI metadata block in ARRIRAW files.
"""

from arriraw_legacy_metadata_reader.binaryfiledto import BinaryFileDTO


class Idi(BinaryFileDTO):
    """
    Class to read the IDI information from an ARRIRAW file.
    """

    def __init__(self, file, fields_to_extract=None):
        super().__init__(file, fields_to_extract=fields_to_extract)
        self.fields = [
            {"name": "IDIValid", "offset": 0x0010, "datatype": "I", "endianness": "<"},
            {
                "name": "ImageWidth",
                "offset": 0x0014,
                "datatype": "I",
                "endianness": "<",
            },
            {
                "name": "ImageHeight",
                "offset": 0x0018,
                "datatype": "I",
                "endianness": "<",
            },
            {"name": "DataType", "offset": 0x001C, "datatype": "I", "endianness": "<"},
            {"name": "DataSpace", "offset": 0x0020, "datatype": "I", "endianness": "<"},
            {
                "name": "ActiveImageLeft",
                "offset": 0x0024,
                "datatype": "I",
                "endianness": "<",
            },
            {
                "name": "ActiveImageTop",
                "offset": 0x0028,
                "datatype": "I",
                "endianness": "<",
            },
            {
                "name": "ActiveImageWidth",
                "offset": 0x002C,
                "datatype": "I",
                "endianness": "<",
            },
            {
                "name": "ActiveImageHeight",
                "offset": 0x0030,
                "datatype": "I",
                "endianness": "<",
            },
            {
                "name": "FullImageWidth",
                "offset": 0x003C,
                "datatype": "I",
                "endianness": "<",
            },
            {
                "name": "FullImageHeigth",
                "offset": 0x0040,
                "datatype": "I",
                "endianness": "<",
            },
        ]
        self.data = self.extract_metadata()
