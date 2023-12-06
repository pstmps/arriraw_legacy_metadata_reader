
import struct
import binascii
import uuid
# import pandas as pd
import io

class BinaryFileDTO:
    def __init__(self, file, fields_to_extract=None):
        if isinstance(file, io.BufferedReader):
            self.file = file
        elif isinstance(file, bytes):
            self.file = io.BytesIO(file)
        else:
            raise TypeError('file must be a bytes object or a BufferedReader')
        self.fields_to_extract = fields_to_extract
        self.endianness = self.determine_endianness()

    def list_fields(self) -> list:
        return [field['name'] for field in self.fields]

    def list_data_names(self) -> list:
        return list(self.data.keys())

    def get_data(self) -> dict:
        return self.data

    # moved to ArriRawLegacyMetadataReader
    # def get_dataframe(self) -> pd.DataFrame:
    #     return pd.DataFrame.from_dict(self.data, orient='index').transpose()

    def read_and_unpack(self, format_string: str):
        return struct.unpack(format_string, self.file.read(struct.calcsize(format_string)))[0]

    def determine_endianness(self) -> str:
        self.file.seek(0)
        ariMagic = self.file.read(4)
        ariByteOrder = self.read_and_unpack('<I')
        isLittleEndian = ariByteOrder == 0x12345678
        return '<' if isLittleEndian else '>'

    def read_string(self, file: bytes, length: int, endianness: str) -> str:
        bytes_data = file.read(length)
        bytes_data = bytes_data[::-1] if endianness == '<' else bytes_data
        return bytes_data.decode('utf-8', 'ignore').rstrip('\x00').replace('\x00', '')

    def read_frameline(self, file: bytes, frameline_number: str, endianness: str) -> dict:
        frameline_type = self.read_and_unpack('<I')
        frameline = {}

        if frameline_type == 1:
            frameline[f'FrameLine{frameline_number}Type'] = 'Master'
        elif frameline_type == 2:
            frameline[f'FrameLine{frameline_number}Type'] = 'Aux'
        else:
            frameline[f'FrameLine{frameline_number}Type'] = 'Inactive'

        if frameline[f'FrameLine{frameline_number}Type'] == 'Inactive':
            defaultvalue = '--'
            frameline[f'FrameLine{frameline_number}Name'] = defaultvalue
            frameline[f'FrameLine{frameline_number}Left'] = defaultvalue
            frameline[f'FrameLine{frameline_number}Top'] = defaultvalue
            frameline[f'FrameLine{frameline_number}Width'] = defaultvalue
            frameline[f'FrameLine{frameline_number}Height'] = defaultvalue
        else:
            frameline[f'FrameLine{frameline_number}Name'] = self.read_string(
                file, 32, endianness)
            frameline[f'FrameLine{frameline_number}Left'] = self.read_and_unpack(
                '<H')
            frameline[f'FrameLine{frameline_number}Top'] = self.read_and_unpack(
                '<H')
            frameline[f'FrameLine{frameline_number}Width'] = self.read_and_unpack(
                '<H')
            frameline[f'FrameLine{frameline_number}Height'] = self.read_and_unpack(
                '<H')

        return frameline

    @staticmethod
    def read_tstop(file: bytes, endianness: str) -> str:
        data = int.from_bytes(file.read(4), byteorder=endianness)

        if data == -3:
            tstop = 'NearClose'
        elif data == -2:
            tstop = 'Close'
        elif data == -1:
            tstop = 'Invalid'
        else:
            # Convert to TStop
            tstop = 2 ** (((data/1000) - 1) / 2)
            tstop = str(round(tstop, 2))
        return tstop

    @staticmethod
    def read_bits(file: bytes, endianness: str, bit_position: list) -> int:
        data = int.from_bytes(file.read(4), byteorder=endianness)
        # Create a mask for the specified bits
        mask = sum([2**i for i in bit_position])
        # Use bitwise AND to isolate the specified bits, then right shift to move them to the least significant position
        specific_bits = (data & mask) >> min(bit_position)

        return specific_bits

    @staticmethod
    def bytestoTC(TCbytes: bytes) -> str:
        hex_tc = binascii.hexlify(TCbytes).decode()
        reversed_tc = ''.join([hex_tc[i:i+2]
                              for i in range(0, len(hex_tc), 2)][::-1])
        timecode = ':'.join([reversed_tc[i:i+2]
                            for i in range(0, len(reversed_tc), 2)])
        return timecode

    @staticmethod
    def split_user_string(input_string: str) -> dict:
        pairs = input_string.split(';')
        return {pair.split(':')[0].strip(): pair.split(':')[1].strip() for pair in pairs if ':' in pair}

    def extract_metadata(self) -> dict:
        metadata = {}
        for field in self.fields:
            if self.fields_to_extract is None or field['name'] in self.fields_to_extract:
                self.file.seek(field['offset'])
                endianness = field['endianness'] if field.get(
                    'endianness', None) is not None else self.endianness
                metadata.update(self.handle_field(field, endianness))
        return metadata

    def handle_field(self, field: dict, endianness: str) -> dict:
        field_handlers = {
            'string': self.handle_string_field,
            'UserString': self.handle_user_string_field,
            'timecode': self.handle_timecode_field,
            'TStop': self.handle_tstop_field,
            'frameline': self.handle_frameline_field,
            'uuid': self.handle_uuid_field,
            'bits': self.handle_bits_field,
        }

        handler = field_handlers.get(
            field['datatype'], self.handle_default_field)
        return handler(field, endianness)

    def handle_string_field(self, field: dict, endianness: str) -> dict:
        return {field['name']: self.read_string(self.file, field['length'], endianness)}

    def handle_user_string_field(self, field: dict, endianness: str) -> dict:
        return self.split_user_string(self.read_string(self.file, field['length'], endianness))

    def handle_timecode_field(self, field: dict, endianness: str) -> dict:
        return {field['name']: self.bytestoTC(self.file.read(4))}

    def handle_tstop_field(self, field: dict, endianness: str) -> dict:
        endianness = 'big' if endianness == '>' else 'little'
        return {field['name']: self.read_tstop(self.file, endianness)}

    def handle_frameline_field(self, field: dict, endianness: str) -> dict:
        frameline_number = field['number']
        return self.read_frameline(self.file, frameline_number, endianness)

    def handle_uuid_field(self, field: dict, endianness: str) -> dict:
        return {field['name']: str(uuid.UUID(bytes_le=self.file.read(16)))}

    def handle_bits_field(self, field: dict, endianness: str) -> dict:
        endianness = 'big' if endianness == '>' else 'little'
        return {field['name']: self.read_bits(self.file, endianness, field['bit_position'])}

    def handle_default_field(self, field: dict, endianness: str) -> dict:
        return {field['name']: self.read_and_unpack(endianness + field['datatype'])}
