from binaryfiledto import BinaryFileDTO

class NRI(BinaryFileDTO):
    def __init__(self, file, fields_to_extract=None):
        super().__init__(file, fields_to_extract=fields_to_extract)
        self.fields = [
            {'name': 'NoiseReductionMode',          'offset': 0x09D8, 'datatype': 'I', 'endianness': '<'}, # Documentation unclear
            {'name': 'NoiseReductionStrength',      'offset': 0x09DC, 'datatype': 'I', 'endianness': '<'}, # Documentation unclear
            {'name': 'NoiseReductionApplied',       'offset': 0x09E0, 'datatype': 'I', 'endianness': '<'}, # Documentation unclear
        ]
        self.data = self.extract_metadata()