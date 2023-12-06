from binaryfiledto import BinaryFileDTO

class VFX(BinaryFileDTO):
    def __init__(self, file, fields_to_extract=None):
        super().__init__(file, fields_to_extract=fields_to_extract)
        self.fields = [
            {'name': 'VFXValid',                    'offset': 0x0438, 'datatype': 'I', 'endianness': '<'}, # 56
            {'name': 'GPSLatitude',                 'offset': 0x043C, 'datatype': 'q', 'endianness': '<'}, # Documentation unclear
            {'name': 'GPSLongitude',                'offset': 0x0444, 'datatype': 'q', 'endianness': '<'}, # Documentation unclear
            {'name': 'CameraX',                     'offset': 0x044C, 'datatype': 'f', 'endianness': '<'}, # Documentation unclear
            {'name': 'CameraY',                     'offset': 0x0450, 'datatype': 'f', 'endianness': '<'}, # Documentation unclear
            {'name': 'CameraZ',                     'offset': 0x0454, 'datatype': 'f', 'endianness': '<'}, # Documentation unclear
            {'name': 'CameraPan',                   'offset': 0x0458, 'datatype': 'f', 'endianness': '<'}, # Documentation unclear
            {'name': 'CameraTilt',                  'offset': 0x045C, 'datatype': 'l', 'endianness': '<'},
            {'name': 'CameraRoll',                  'offset': 0x0460, 'datatype': 'l', 'endianness': '<'},
            {'name': 'MasterSlaveSetupInfo',        'offset': 0x0464, 'datatype': 'H', 'endianness': '<'},
            {'name': '3DEyeInfo',                   'offset': 0x0468, 'datatype': 'H', 'endianness': '<'},
        ]
        self.data = self.extract_metadata()

