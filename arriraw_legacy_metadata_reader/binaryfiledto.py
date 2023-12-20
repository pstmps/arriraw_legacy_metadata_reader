"""
Base class for metadata fields for ARRIRAW file sequences
"""

import struct
import binascii
import uuid
# import pandas as pd
import io
from typing import Union
from abc import ABC

class BinaryFileDTO(ABC):
    """
    Base class for reading binary ARRIRAW files
    It is not intended to be used directly, but rather to be inherited by other classes
    Implements the following methods:
    - list_fields: returns a list of all the fields in the file
    - list_data_names: returns a list of all the data names in the file
    - get_data: returns a dictionary of all the data in the file
    - extract_metadata: extracts the metadata from the file
    - handle_field: handles the field based on its datatype

    """

    def __init__(self, file, fields_to_extract=None):
        if isinstance(file, io.BufferedReader):
            self.file = file
        elif isinstance(file, bytes):
            self.file = io.BytesIO(file)
        else:
            raise TypeError('file must be a bytes object or a BufferedReader')
        self.fields_to_extract = fields_to_extract
        self.endianness = self._determine_endianness()
        # add empty fields and data attributes to the class to make the linter happier
        self.fields = []
        self.data = {}

    def list_fields(self) -> list:
        """
        Returns a list of all the fields in the file
        Returns:
            list: list of all the field names defined in the subclass
        """
        return [field['name'] for field in self.fields]

    def list_data_names(self) -> list:
        """
        Returns a list of all the data names in the file
        Returns:
            list: list of all the data names actually marked for extraction
        """
        return list(self.data.keys())

    def get_data(self) -> dict:
        """
        Returns a dictionary of all the data marked for extraction in the file
        Returns:
            dict: dictionary of all the data marked for extraction
        """
        return self.data

    def _read_and_unpack(self, input_bytes: bytes, format_string: str) \
                        -> Union[int, float, str, bytes]:
        """
        Reads and unpacks data from the file
        Args:
            format_string (str): format string for the struct.unpack 
            method containing the datatype and endianness
        Returns:
            Union[int, float, str, bytes]: the data read from the file
        """
        return struct.unpack(format_string, input_bytes.read(struct.calcsize(format_string)))[0]

    def _determine_endianness(self) -> str:
        """
        Determines the endianness of the file
        Returns:
            str: '<' for little endian, '>' for big endian
        """
        self.file.seek(0)
        ari_magic = self.file.read(4)
        ari_byte_order = self._read_and_unpack(self.file, '<I')
        is_little_endian = ari_byte_order == 0x12345678
        return '<' if is_little_endian else '>'

    def _read_string(self, input_bytes: bytes, length: int, endianness: str) -> str:
        """
        Reads a string from a byte object
        Args:
            input_bytes (bytes): the byte object to read from
            length (int): the length of the string to read
            endianness (str): the endianness of the byte object
        Returns:
            str: the string read from the byte object
        """
        bytes_data = input_bytes.read(length)
        bytes_data = bytes_data[::-1] if endianness == '<' else bytes_data
        return bytes_data.decode('utf-8', 'ignore').rstrip('\x00').replace('\x00', '')

    def _read_frameline(self, input_bytes: bytes, frameline_number: str, endianness: str) -> dict:
        """
        Reads a frameline object from a byte object
        Args:
            input_bytes (bytes): the byte object to read from
            frameline_number (str): the number of the frameline to read
            endianness (str): the endianness of the byte object
        Returns:
            dict: the frameline object read from the byte object
        """
        frameline_type = self._read_and_unpack(input_bytes=input_bytes, format_string='<I')
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
            frameline[f'FrameLine{frameline_number}Name'] = self._read_string(
                input_bytes=input_bytes, length=32, endianness=endianness)
            frameline[f'FrameLine{frameline_number}Left'] = self._read_and_unpack(
                input_bytes=input_bytes, format_string='<H')
            frameline[f'FrameLine{frameline_number}Top'] = self._read_and_unpack(
                input_bytes=input_bytes, format_string='<H')
            frameline[f'FrameLine{frameline_number}Width'] = self._read_and_unpack(
                input_bytes=input_bytes, format_string='<H')
            frameline[f'FrameLine{frameline_number}Height'] = self._read_and_unpack(
                input_bytes=input_bytes, format_string='<H')

        return frameline

    @staticmethod
    def _convert_data_to_tstop(data: int) -> str:
        """
        Converts a data value to a TStop as per the ARRI Documentation
        Args:
            data (int): the data value to convert
        Returns:
            str: the TStop converted from the data value
        """
        tstop_mapping = {
            -3: 'NearClose',
            -2: 'Close',
            -1: 'Invalid'
        }

        if data in tstop_mapping:
            return tstop_mapping[data]

        tstop = 2 ** (((data/1000) - 1) / 2)
        return str(round(tstop, 2))

    @staticmethod
    def _read_tstop(input_bytes: bytes, endianness: str) -> str:
        """
        Reads a TStop from a byte object
        Converts the bytes to a float and then to a TStop via the _convert_data_to_tstop method
        Args:
            input_bytes (bytes): the byte object to read from
            endianness (str): the endianness of the byte object
        Returns:
            str: the TStop read from the byte object
        """
        # TODO: Add conversion to Tstop with n/10th notation (2.0 8/10)
        data = int.from_bytes(input_bytes.read(4), byteorder=endianness)
        return BinaryFileDTO._convert_data_to_tstop(data)

    @staticmethod
    def _read_bit(data: bytes, bit_position: int, endianness: str) -> int:
        value = int.from_bytes(data.read(4), byteorder=endianness)
        print(value)
        return (value >> bit_position) & 1

    @staticmethod
    def _bytes_to_time_code(time_code_bytes: bytes) -> str:
        """
        Converts a byte object to a timecode
        Args:
            time_code_bytes (bytes): the byte object to convert
        Returns:
            str: the timecode converted from the byte object
        """
        hex_tc = binascii.hexlify(time_code_bytes).decode()
        reversed_tc = ''.join([hex_tc[i:i+2]
                              for i in range(0, len(hex_tc), 2)][::-1])
        timecode = ':'.join([reversed_tc[i:i+2]
                            for i in range(0, len(reversed_tc), 2)])
        return timecode

    @staticmethod
    def _split_user_string(input_string: str) -> dict:
        """
        Splits the Arri UserString into a dictionary
        Args:
            input_string (str): the UserString to split
        Returns:
            dict: the UserString split into a dictionary
        """
        pairs = input_string.split(';')
        return {pair.split(':')[0].strip(): pair.split(':')[1].strip()
                for pair in pairs if ':' in pair}

    @staticmethod
    def _bcd_to_str(bcd: bytes,
                    format_string: str,
                    spacer: str,
                    endianness: str,
                    prefix: str = None) -> str:
        """
        Converts a byte object in BCD - (Binary Code Decimal;) format to a string
        Args:
            bcd (bytes): the byte object to convert
            format (str): the format of the output string - date, time, or offset
            spacer (str): the spacer between the output elements
            endianness (str): the endianness of the byte object
        Returns:
            str: the byte object converted to a string
        """
        # Convert each nibble in the BCD to a decimal digit
        decimal_digits = [f"{b >> 4}{b & 0x0F}" for b in bcd]
        # Join the decimal digits together and format as a date
        if endianness == '>':
            date_string = "".join(decimal_digits[::-1])
        else:
            date_string = "".join(decimal_digits)

        if prefix is None:
            prefix = ''

        if format_string == 'date':
            return f"{date_string[:4]}{spacer}{date_string[4:6]}{spacer}{date_string[6:8]}"
        if format_string == 'time':
            return (
                f"{date_string[:2]}{spacer}"
                f"{date_string[2:4]}{spacer}"
                f"{date_string[4:6]}{spacer}"
                f"{date_string[6:8]}"
            )
        if format_string == 'offset':
            return f"{prefix}{date_string[4:6]}{spacer}{date_string[6:8]}"

        return date_string

    def extract_metadata(self) -> dict:
        """
        Extracts the metadata from the file
        Returns:
            dict: the metadata extracted from the file
        """
        metadata = {}
        for field in self.fields:
            if self.fields_to_extract is None or field['name'] in self.fields_to_extract:
                self.file.seek(field['offset'])
                endianness = field['endianness'] if field.get(
                    'endianness', None) is not None else self.endianness
                metadata.update(self.handle_field(field, endianness))

                if field.get('mapping', None) is not None:
                    metadata[field['name']] = field['mapping'].get(
                        metadata[field['name']], 'Unknown')

        return metadata

    def handle_field(self, field: dict, endianness: str) -> dict:
        """
        Handles the field based on its datatype
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        field_handlers = {
            'string': self._handle_string_field,
            'UserString': self._handle_user_string_field,
            'timecode': self._handle_timecode_field,
            'TStop': self._handle_tstop_field,
            'frameline': self._handle_frameline_field,
            'uuid': self._handle_uuid_field,
            'bits': self._handle_bits_field,
            'date': self._handle_date_field,
            'time': self._handle_time_field,
            'offset': self._handle_offset_field,
            'float': self._handle_float_field,
        }

        handler = field_handlers.get(
            field['datatype'], self._handle_default_field)
        return handler(field, endianness)

    def _handle_string_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a string field
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        return {field['name']: self._read_string(self.file, field['length'], endianness)}

    def _handle_user_string_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a ARRI User string field
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        return self._split_user_string(self._read_string(self.file, field['length'], endianness))

    def _handle_timecode_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a timecode field
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        return {field['name']: self._bytes_to_time_code(self.file.read(4))}

    def _handle_tstop_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a TStop field
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        endianness = 'big' if endianness == '>' else 'little'
        return {field['name']: self._read_tstop(self.file, endianness)}

    def _handle_frameline_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a frameline field
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        frameline_number = field['number']
        return self._read_frameline(self.file, frameline_number, endianness)

    def _handle_uuid_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a UUID field
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        return {field['name']: str(uuid.UUID(bytes_le=self.file.read(16)))}

    def _handle_bits_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a bits field
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        endianness = 'big' if endianness == '>' else 'little'
        return {field['name']: self._read_bit(data=self.file,
                                              bit_position=field['bit_position'],
                                              endianness=endianness)}

    def _handle_default_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a default field, format is defined by the datatype
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        return {field['name']: self._read_and_unpack(input_bytes=self.file,
                                                     format_string=endianness + field['datatype'])}

    def _handle_date_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a date field, format is defined by the datatype
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        date_bcd = self.file.read(
            4)  # self._read_and_unpack(input_bytes=self.file, format_string= endianness + 'B')
        return {field['name']: self._bcd_to_str(bcd=date_bcd,
                                                format_string=field['datatype'],
                                                spacer='/',
                                                endianness=endianness)}

    def _handle_time_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a time field, format is defined by the datatype
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        time_bcd = self.file.read(
            4)  # self._read_and_unpack(input_bytes=self.file, format_string= endianness + 'B')
        return {field['name']: self._bcd_to_str(bcd=time_bcd,
                                                format_string=field['datatype'],
                                                spacer=':',
                                                endianness=endianness)}

    def _handle_offset_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a time offset field, format is defined by the datatype
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        offset_bcd = self.file.read(4)
        return {field['name']: self._bcd_to_str(bcd=offset_bcd,
                                                format_string=field['datatype'],
                                                prefix=field['prefix'],
                                                spacer=':',
                                                endianness=endianness)}

    def _handle_float_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a float field, format is defined by the datatype
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        data = self._read_and_unpack(
            input_bytes=self.file, format_string=endianness + 'I')
        data = float(data / 1000)

        if field.get('decimals', None) is not None:
            data = f'{data:.{field["decimals"]}f}'
        if field.get('unit', None) is not None:
            data = f"{data} {field['unit']}"

        return {field['name']: data}
