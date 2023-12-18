"""
Defines the ICI class, which defines the ICI metadata block in ARRIRAW files.
"""
from arriraw_legacy_metadata_reader.binaryfiledto import BinaryFileDTO

class ICI(BinaryFileDTO):
    """
    Class to read the ICI information from an ARRIRAW file.
    """
    def __init__(self, file, fields_to_extract=None):
        super().__init__(file, fields_to_extract=fields_to_extract)
        self.unit_mapping = {
            'WBAppliedInCamera' : {0: 'no',
                                   1: 'yes'},
            'TargetColorSpace' : {2: 'LogCWGam'},
            'ImageOrientation' : {0: 'No flip',
                                  1: 'H flip',
                                  12: 'H+V flip'},
            'LookLUTMode' : {0: 'ARRI_LOOK_LUT_NO_LUT',
                             1: 'ARRI_LOOK_LUT_MONO',
                             2: 'ARRI_LOOK_LUT_3D'},
            'CDLMode' : {0: 'No Look',
                         1: 'Alexa Look Video',
                         2: 'CDL Video',
                         3: 'CDL LogC'},
        }
        self.fields = [
            {'name': 'ICIValid',                    'offset': 0x0054, 'datatype': 'I',
             'endianness': '<'},
            {'name': 'ColorProcessingVersion',      'offset': 0x0058, 'datatype': 'I',
             'endianness': '<'},
            {'name': 'WhiteBalance',                'offset': 0x005C, 'datatype': 'I',
             'endianness': '<'},
            {'name': 'WhiteBalanceCC',              'offset': 0x0060, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'WBFactorR',                   'offset': 0x0064, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'WBFactorG',                   'offset': 0x0068, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'WBFactorB',                   'offset': 0x006C, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'WBAppliedInCamera',           'offset': 0x0070, 'datatype': 'I',
             'endianness': '<',
             'mapping': self.unit_mapping['WBAppliedInCamera']},
            {'name': 'ExposureIndexASA',            'offset': 0x0074, 'datatype': 'I',
             'endianness': '<'},
            {'name': 'TargetColorSpace',            'offset': 0x00BC, 'datatype': 'I',
             'endianness': '<',
             'mapping': self.unit_mapping['TargetColorSpace']},
            {'name': 'Sharpness',                   'offset': 0x00C0, 'datatype': 'I',
             'endianness': '<'},
            {'name': 'LensSqueezeFactor',           'offset': 0x00C4, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'ImageOrientation',            'offset': 0x00C8, 'datatype': 'I',
             'endianness': '<',
             'mapping': self.unit_mapping['ImageOrientation']},
            {'name': 'LookName',                    'offset': 0x00CC, 'datatype': 'string',
             'length': 32,'endianness': '>'},
            {'name': 'LookLUTMode',                 'offset': 0x00EC, 'datatype': 'I',
             'endianness': '<',
             'mapping': self.unit_mapping['LookLUTMode']},
            {'name': 'LookLUTOffset',               'offset': 0x00F0, 'datatype': 'I',
             'endianness': '<'},
            {'name': 'LookLUTSize',                 'offset': 0x00F4, 'datatype': 'I',
             'endianness': '<'},
            #{'name': 'LookLiveGradingFlags',        'offset': 0x00F4, 'datatype': 'I',
            #'endianness': '<'}, # Documentation unclear, same offset as LookLUTSize
            {'name': 'LookSaturation',              'offset': 0x00F8, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'CDLSaturation',               'offset': 0x00FC, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'CDLSlopeR',                   'offset': 0x0100, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'CDLSlopeG',                   'offset': 0x0104, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'CDLSlopeB',                   'offset': 0x0108, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'CDLOffsetR',                  'offset': 0x010C, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'CDLOffsetG',                  'offset': 0x0110, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'CDLOffsetB',                  'offset': 0x0114, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'CDLPowerR',                   'offset': 0x0118, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'CDLPowerG',                   'offset': 0x011C, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'CDLPowerB',                   'offset': 0x0120, 'datatype': 'f',
             'endianness': '<'},
            {'name': 'CDLMode',                     'offset': 0x0130, 'datatype': 'I',
             'endianness': '<',
             'mapping': self.unit_mapping['CDLMode']},
            {'name': 'ImageDataChecksum',           'offset': 0x0134, 'datatype': 'I',
             'endianness': '<'}, # Documentation unclear
            {'name': 'ColorOrder',                  'offset': 0x0138, 'datatype': 'I',
             'endianness': '<'}, # Documentation unclear
        ]
        self.data = self.extract_metadata()
