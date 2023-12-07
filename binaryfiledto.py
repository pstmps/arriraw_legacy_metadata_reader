
import struct
import binascii
import uuid
# import pandas as pd
import io
from typing import Union

class BinaryFileDTO:
    """
    Base class for reading binary ARRIRAW files
    It is not intended to be used directly, but rather to be inherited by other classes
    Implements the following methods:
    - list_fields: returns a list of all the fields in the file
    - list_data_names: returns a list of all the data names in the file
    - get_data: returns a dictionary of all the data in the file

    """
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

    def read_and_unpack(self, input: bytes, format_string: str) -> Union[int, float, str, bytes]:
        """
        Reads and unpacks data from the file
        Args:
            format_string (str): format string for the struct.unpack method containing the datatype and endianness
        Returns:
            Union[int, float, str, bytes]: the data read from the file
        """
        return struct.unpack(format_string, input.read(struct.calcsize(format_string)))[0]

    def determine_endianness(self) -> str:
        """
        Determines the endianness of the file
        Returns:
            str: '<' for little endian, '>' for big endian
        """
        self.file.seek(0)
        ariMagic = self.file.read(4)
        ariByteOrder = self.read_and_unpack(self.file,'<I')
        isLittleEndian = ariByteOrder == 0x12345678
        return '<' if isLittleEndian else '>'

    def read_string(self, input: bytes, length: int, endianness: str) -> str:
        """
        Reads a string from a byte object
        Args:
            input (bytes): the byte object to read from
            length (int): the length of the string to read
            endianness (str): the endianness of the byte object
        Returns:
            str: the string read from the byte object
        """
        bytes_data = input.read(length)
        bytes_data = bytes_data[::-1] if endianness == '<' else bytes_data
        return bytes_data.decode('utf-8', 'ignore').rstrip('\x00').replace('\x00', '')

    def read_frameline(self, input: bytes, frameline_number: str, endianness: str) -> dict:
        """
        Reads a frameline object from a byte object
        Args:
            input (bytes): the byte object to read from
            frameline_number (str): the number of the frameline to read
            endianness (str): the endianness of the byte object
        Returns:
            dict: the frameline object read from the byte object
        """
        frameline_type = self.read_and_unpack(input=input, format_string='<I')
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
                input=input, length=32, endianness=endianness)
            frameline[f'FrameLine{frameline_number}Left'] = self.read_and_unpack(
                input=input,format_string='<H')
            frameline[f'FrameLine{frameline_number}Top'] = self.read_and_unpack(
                input=input,format_string='<H')
            frameline[f'FrameLine{frameline_number}Width'] = self.read_and_unpack(
                input=input,format_string='<H')
            frameline[f'FrameLine{frameline_number}Height'] = self.read_and_unpack(
                input=input,format_string='<H')

        return frameline

    @staticmethod
    def convert_data_to_tstop(data: int) -> str:
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
    def read_tstop(input: bytes, endianness: str) -> str:
        """
        Reads a TStop from a byte object
        Converts the bytes to a float and then to a TStop via the convert_data_to_tstop method
        Args:
            input (bytes): the byte object to read from
            endianness (str): the endianness of the byte object
        Returns:
            str: the TStop read from the byte object
        """
        #TODO: Add conversion to Tstop with n/10th notation (2.0 8/10)
        data = int.from_bytes(input.read(4), byteorder=endianness)
        return BinaryFileDTO.convert_data_to_tstop(data)
    
    @staticmethod
    def create_bit_mask(bit_positions: list) -> int:
        """
        Creates a bit mask for the specified bit positions.
        Args:
            bit_positions (list): the positions of the bits for the mask
        Returns:
            int: the bit mask
        """
        return sum([2**i for i in bit_positions])

    @staticmethod
    def read_bits(input: bytes, endianness: str, bit_position: list) -> int:
        """
        Reads specific bits from a byte object
        Args:
            input (bytes): the byte object to read from
            endianness (str): the endianness of the byte object
            bit_position (list): the position of the bits to read
        Returns:
            int: the bits read from the byte object
        """
        data = int.from_bytes(input.read(4), byteorder=endianness)
        # Create a mask for the specified bits
        mask = BinaryFileDTO.create_bit_mask(bit_position)
        # mask = sum([2**i for i in bit_position])
        # Use bitwise AND to isolate the specified bits, then right shift to move them to the least significant position
        specific_bits = (data & mask) >> min(bit_position)

        return specific_bits

    @staticmethod
    def bytestoTC(TCbytes: bytes) -> str:
        """
        Converts a byte object to a timecode
        Args:
            TCbytes (bytes): the byte object to convert
        Returns:
            str: the timecode converted from the byte object
        """
        hex_tc = binascii.hexlify(TCbytes).decode()
        reversed_tc = ''.join([hex_tc[i:i+2]
                              for i in range(0, len(hex_tc), 2)][::-1])
        timecode = ':'.join([reversed_tc[i:i+2]
                            for i in range(0, len(reversed_tc), 2)])
        return timecode

    @staticmethod
    def split_user_string(input_string: str) -> dict:
        """
        Splits the Arri UserString into a dictionary
        Args:
            input_string (str): the UserString to split
        Returns:
            dict: the UserString split into a dictionary
        """
        pairs = input_string.split(';')
        return {pair.split(':')[0].strip(): pair.split(':')[1].strip() for pair in pairs if ':' in pair}
        
    @staticmethod
    def bcd_to_str(bcd: bytes, format: str, spacer: str, endianness: str, prefix : str= None) -> str:
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

        prefix is prefix if prefix is not None else '' 
        if format == 'date':
            return f"{date_string[:4]}{spacer}{date_string[4:6]}{spacer}{date_string[6:8]}"
        elif format == 'time':
            return f"{date_string[:2]}{spacer}{date_string[2:4]}{spacer}{date_string[4:6]}{spacer}{date_string[6:8]}"
        elif format == 'offset':
            return f"{prefix}{date_string[4:6]}{spacer}{date_string[6:8]}"

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
                    metadata[field['name']] = field['mapping'].get(metadata[field['name']], 'Unknown')

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
            'string': self.handle_string_field,
            'UserString': self.handle_user_string_field,
            'timecode': self.handle_timecode_field,
            'TStop': self.handle_tstop_field,
            'frameline': self.handle_frameline_field,
            'uuid': self.handle_uuid_field,
            'bits': self.handle_bits_field,
            'date': self.handle_date_field,
            'time': self.handle_time_field,
            'offset': self.handle_offset_field,
            'float': self.handle_float_field,
        }

        handler = field_handlers.get(
            field['datatype'], self.handle_default_field)
        return handler(field, endianness)

    def handle_string_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a string field
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        return {field['name']: self.read_string(self.file, field['length'], endianness)}

    def handle_user_string_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a ARRI User string field
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        return self.split_user_string(self.read_string(self.file, field['length'], endianness))

    def handle_timecode_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a timecode field
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        return {field['name']: self.bytestoTC(self.file.read(4))}

    def handle_tstop_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a TStop field
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        endianness = 'big' if endianness == '>' else 'little'
        return {field['name']: self.read_tstop(self.file, endianness)}

    def handle_frameline_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a frameline field
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        frameline_number = field['number']
        return self.read_frameline(self.file, frameline_number, endianness)

    def handle_uuid_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a UUID field
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        return {field['name']: str(uuid.UUID(bytes_le=self.file.read(16)))}

    def handle_bits_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a bits field
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        endianness = 'big' if endianness == '>' else 'little'
        return {field['name']: self.read_bits(self.file, endianness, field['bit_position'])}

    def handle_default_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a default field, format is defined by the datatype
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        return {field['name']: self.read_and_unpack(input=self.file, format_string= endianness + field['datatype'])}

    def handle_date_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a date field, format is defined by the datatype
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        date_bcd = self.file.read(4) # self.read_and_unpack(input=self.file, format_string= endianness + 'B')
        return {field['name']: self.bcd_to_str(bcd=date_bcd, format=field['datatype'], spacer='/', endianness=endianness)}
    
    def handle_time_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a time field, format is defined by the datatype
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        time_bcd = self.file.read(4) # self.read_and_unpack(input=self.file, format_string= endianness + 'B')
        return {field['name']: self.bcd_to_str(bcd=time_bcd, format=field['datatype'], spacer=':', endianness=endianness)}
    
    def handle_offset_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a time offset field, format is defined by the datatype
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        offset_bcd = self.file.read(4)
        return {field['name']: self.bcd_to_str(bcd=offset_bcd, format=field['datatype'], prefix=field['prefix'], spacer=':', endianness=endianness)}
    
    def handle_float_field(self, field: dict, endianness: str) -> dict:
        """
        Handles a float field, format is defined by the datatype
        Args:
            field (dict): the field to handle
            endianness (str): the endianness of the file
        Returns:
            dict: the field handled
        """
        data = self.read_and_unpack(input=self.file, format_string= endianness + 'I')
        data = float(data / 1000)

        if field.get('decimals', None) is not None:
            data = f'{data:.{field["decimals"]}f}'
        if field.get('unit', None) is not None:
            data = f"{data} {field['unit']}"

        return {field['name']: data}