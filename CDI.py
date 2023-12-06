from binaryfiledto import BinaryFileDTO

class CDI(BinaryFileDTO):
    def __init__(self, file, fields_to_extract=None):
        super().__init__(file, fields_to_extract=fields_to_extract)
        self.fields = [
            {'name': 'CDIValid',                    'offset': 0x0160, 'datatype': 'I', 'endianness': '<'},
            {'name': 'CameraTypeId',                'offset': 0x0164, 'datatype': 'I', 'endianness': '<'},
            {'name': 'CameraRevision',              'offset': 0x0168, 'datatype': 'I', 'endianness': '<'},
            {'name': 'CameraSerialNumber',          'offset': 0x0170, 'datatype': 'I', 'endianness': '<'},
            {'name': 'CameraId',                    'offset': 0x0174, 'datatype': 'string', 'length': 4, 'endianness': '<'},
            {'name': 'CameraIndex',                 'offset': 0x0178, 'datatype': 'I', 'endianness': '<'},
            {'name': 'SystemImageCreationDate',     'offset': 0x017C, 'datatype': 'I', 'endianness': '<'},
            {'name': 'SystemImageCreationTime',     'offset': 0x0180, 'datatype': 'I', 'endianness': '<'},
            {'name': 'SystemImageTimeZoneOffset',   'offset': 0x0184, 'datatype': 'I', 'endianness': '<'},
            {'name': 'SystemImageTimeZoneDST',      'offset': 0x0188, 'datatype': 'I', 'endianness': '<'},
            {'name': 'ExposureTime',                'offset': 0x018C, 'datatype': 'I', 'endianness': '<'},
            {'name': 'SystemImageTimeZoneDST',      'offset': 0x0188, 'datatype': 'I', 'endianness': '<'},
            {'name': 'SensorFPS',                   'offset': 0x01A0, 'datatype': 'I', 'endianness': '<'},
            {'name': 'ProjectFPS',                  'offset': 0x01A4, 'datatype': 'I', 'endianness': '<'},
            {'name': 'MasterTC',                    'offset': 0x01A8, 'datatype': 'timecode'},
            {'name': 'MasterTCFrameCount',          'offset': 0x01AC, 'datatype': 'I', 'endianness': '<'},
            {'name': 'MasterTCTimeBase',            'offset': 0x01B0, 'datatype': 'I', 'endianness': '<'},
            {'name': 'StorageMediaSerialNumber',    'offset': 0x0268, 'datatype': 'Q', 'endianness': '<'},
            {'name': 'CameraFamily',                'offset': 0x029C, 'datatype': 'string', 'length': 8, 'endianness': '>'},
            {'name': 'RecorderType',                'offset': 0x02A4, 'datatype': 'string', 'length': 32, 'endianness': '>'},
            {'name': 'MirrorShutterRunning',        'offset': 0x02C4, 'datatype': 'bits', 'endianness': '<', 'bit_position': [0]},
            {'name': 'Vari',                        'offset': 0x02C4, 'datatype': 'bits', 'endianness': '<', 'bit_position': [1]},
            {'name': 'UUID',                        'offset': 0x02D0, 'datatype': 'uuid'},
            {'name': 'CameraModel',                 'offset': 0x02F8, 'datatype': 'string', 'length': 20, 'endianness': '>'},
            {'name': 'CameraProduct',               'offset': 0x030C, 'datatype': 'H', 'endianness': '<'},
            {'name': 'CameraSubProduct',            'offset': 0x030E, 'datatype': 'H', 'endianness': '<'},
        ]
        self.data = self.extract_metadata()

