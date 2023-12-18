"""
Defines the CID class, which defines the CID metadata block in ARRIRAW files.
"""
from arriraw_legacy_metadata_reader.binaryfiledto import BinaryFileDTO

class CID(BinaryFileDTO):
    """
    Class to read the CID information from an ARRIRAW file.
    """
    def __init__(self, file, fields_to_extract=None):
        super().__init__(file, fields_to_extract=fields_to_extract)
        self.fields = [
            {'name': 'CIDValid',                    'offset': 0x04F0, 'datatype': 'I',
            'endianness': '<'}, # 448
            {'name': 'CircleTake',                  'offset': 0x04F4, 'datatype': 'B',
             'endianness': '<'},
            {'name': 'Reel',                        'offset': 0x04F8, 'datatype': 'string',
             'length': 8 },
            {'name': 'Scene',                       'offset': 0x0500, 'datatype': 'string',
             'length': 16 },
            {'name': 'Take',                        'offset': 0x0510, 'datatype': 'string',
             'length': 8 },
            {'name': 'Director',                    'offset': 0x0518, 'datatype': 'string',
             'length': 24 },
            {'name': 'Cinematographer',             'offset': 0x0538, 'datatype': 'string',
             'length': 24 },
            {'name': 'Production',                  'offset': 0x0558, 'datatype': 'string',
             'length': 24 },
            {'name': 'ProductionCompany',           'offset': 0x0578, 'datatype': 'string',
             'length': 24 },
            {'name': 'VarUserInfoFields',           'offset': 0x0598, 'datatype': 'UserString',
             'length': 256 }, # variable length User Fields
            {'name': 'CameraClipName',              'offset': 0x0698, 'datatype': 'string',
             'length': 20 },
        ]
        self.data = self.extract_metadata()
