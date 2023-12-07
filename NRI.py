from binaryfiledto import BinaryFileDTO

class NRI(BinaryFileDTO):
    def __init__(self, file, fields_to_extract=None):
        super().__init__(file, fields_to_extract=fields_to_extract)
        self.unit_mapping = {
            'NoiseReductionMode' : {0: 'OFF', 1: 'ANR', 65535: 'OFF'},
            'NoiseReductionApplied' : {0: 'OFF', 1: 'ON'},
        }
        self.fields = [
            {'name': 'NoiseReductionMode',          'offset': 0x09D8, 'datatype': 'I', 'endianness': '<', 'mapping': self.unit_mapping['NoiseReductionMode']}, # Documentation unclear
            {'name': 'NoiseReductionStrength',      'offset': 0x09DC, 'datatype': 'f', 'endianness': '<'}, 
            {'name': 'NoiseReductionApplied',       'offset': 0x09E0, 'datatype': 'I', 'endianness': '<', 'mapping': self.unit_mapping['NoiseReductionApplied']}, # Documentation unclear
        ]
        self.data = self.extract_metadata()

