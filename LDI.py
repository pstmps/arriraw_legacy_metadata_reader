from binaryfiledto import BinaryFileDTO

class LDI(BinaryFileDTO):
    def __init__(self, file, fields_to_extract=None):
        super().__init__(file, fields_to_extract=fields_to_extract)
        self.fields = [
            {'name': 'LDIValid',                    'offset': 0x0370, 'datatype': 'I', 'endianness': '<'},
            {'name': 'LensDistanceUnit',            'offset': 0x0374, 'datatype': 'I', 'endianness': '<'},
            {'name': 'LensFocusDistance',           'offset': 0x0378, 'datatype': 'I', 'endianness': '<'},
            {'name': 'LensFocalLength',             'offset': 0x037C, 'datatype': 'I', 'endianness': '<'},
            {'name': 'LensSerialNumber',            'offset': 0x0380, 'datatype': 'I', 'endianness': '<'},
            {'name': 'LensLinearIris',              'offset': 0x0384, 'datatype': 'I', 'endianness': '<'},
            {'name': 'LensIris',                    'offset': 0x0384, 'datatype': 'TStop', 'endianness': '<'},
            {'name': 'NDFilterType',                'offset': 0x0388, 'datatype': 'H', 'endianness': '<'},
            {'name': 'NDFilterDensity',             'offset': 0x038A, 'datatype': 'H', 'endianness': '<'},
            {'name': 'LensModel',                   'offset': 0x0398, 'datatype': 'string', 'length': 32, 'endianness': '>'},
            {'name': 'RawEncoderFocusRawLds',       'offset': 0x03B8, 'datatype': 'H', 'endianness': '<'},
            {'name': 'RawEncoderFocusRawMotor',     'offset': 0x03BA, 'datatype': 'H', 'endianness': '<'},
            {'name': 'RawEncoderFocalRawLds',       'offset': 0x03BC, 'datatype': 'H', 'endianness': '<'},
            {'name': 'RawEncoderFocalRawMotor',     'offset': 0x03BE, 'datatype': 'H', 'endianness': '<'},
            {'name': 'RawEncoderIrisRawLds',        'offset': 0x03C0, 'datatype': 'H', 'endianness': '<'},
            {'name': 'RawEncoderIrsRawMotor',       'offset': 0x03C2, 'datatype': 'H', 'endianness': '<'},
            {'name': 'EncoderLimFocusLdsMin',       'offset': 0x03C4, 'datatype': 'H', 'endianness': '<'},
            {'name': 'EncoderLimFocusLdsMax',       'offset': 0x03C6, 'datatype': 'H', 'endianness': '<'},
            {'name': 'EncoderLimFocalLdsMin',       'offset': 0x03C8, 'datatype': 'H', 'endianness': '<'},
            {'name': 'EncoderLimFocalLdsMax',       'offset': 0x03CA, 'datatype': 'H', 'endianness': '<'},
            {'name': 'EncoderLimIrisLdsMin',        'offset': 0x03CC, 'datatype': 'H', 'endianness': '<'},
            {'name': 'EncoderLimIrisLdsMax',        'offset': 0x03CE, 'datatype': 'H', 'endianness': '<'},
            {'name': 'EncoderLimFocusMotorMin',     'offset': 0x03D0, 'datatype': 'H', 'endianness': '<'},
            {'name': 'EncoderLimFocusMotorMax',     'offset': 0x03D2, 'datatype': 'H', 'endianness': '<'},
            {'name': 'EncoderLimFocalMotorMin',     'offset': 0x03D4, 'datatype': 'H', 'endianness': '<'},
            {'name': 'EncoderLimFocalMotorMax',     'offset': 0x03D6, 'datatype': 'H', 'endianness': '<'},
            {'name': 'EncoderLimIrisMotorMin',      'offset': 0x03D8, 'datatype': 'H', 'endianness': '<'},
            {'name': 'EncoderLimIrissMotorMax',     'offset': 0x03DA, 'datatype': 'H', 'endianness': '<'},
            {'name': 'LdsLagType',                  'offset': 0x03DC, 'datatype': 'B', 'endianness': '<'},
            {'name': 'LdsLagValue',                 'offset': 0x03DD, 'datatype': 'B', 'endianness': '<'},
        ]
        self.data = self.extract_metadata()

