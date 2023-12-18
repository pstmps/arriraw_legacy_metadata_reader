import pytest
from arriraw_legacy_metadata_reader.binaryfiledto import BinaryFileDTO

import struct
import io
import os
import binascii

@pytest.fixture
def binary_file():
    filename_binary = 'test.ari'
    # Create a bytes object with 4KB of random binary data
    data = os.urandom(4096)  # 4KB = 4096 bytes
    with open(filename_binary, 'wb') as f:
        f.write(data)
    yield filename_binary
    os.remove(filename_binary)

def test_list_fields(binary_file):
    # Create an instance of BinaryFileDTO with some fields
    with open(binary_file, 'rb') as f:
        binary_file_dto = BinaryFileDTO(f)
        binary_file_dto.fields = [
            {'name': 'field1', 'offset': 0, 'datatype': 'B', 'endianness': '>'},
            {'name': 'field2', 'offset': 1, 'datatype': 'B', 'endianness': '>'},
            {'name': 'field3', 'offset': 2, 'datatype': 'B', 'endianness': '>'},
        ]
        result = binary_file_dto.list_fields()

    assert result == ['field1', 'field2', 'field3']

def test_list_data_names(binary_file):
    # Create an instance of BinaryFileDTO with some fields
    with open(binary_file, 'rb') as f:
        binary_file_dto = BinaryFileDTO(f)
        binary_file_dto.fields = [
            {'name': 'field1', 'offset': 0, 'datatype': 'B', 'endianness': '<'},
            {'name': 'field2', 'offset': 1, 'datatype': 'B', 'endianness': '<'},
            {'name': 'field3', 'offset': 2, 'datatype': 'B', 'endianness': '<'},
        ]
        # Manually add some data to the data dictionary
        binary_file_dto.data = {'field1': 1, 'field2': 2, 'field3': 3}

        # Call list_data_names and check the result
        result = binary_file_dto.list_data_names()
        assert result == ['field1', 'field2', 'field3']

def test_get_data(binary_file):
    # Create an instance of BinaryFileDTO with some fields
    with open(binary_file, 'rb') as f:
        binary_file_dto = BinaryFileDTO(f)
        binary_file_dto.fields = [
            {'name': 'field1', 'offset': 0, 'datatype': 'B', 'endianness': '<'},
            {'name': 'field2', 'offset': 1, 'datatype': 'B', 'endianness': '<'},
            {'name': 'field3', 'offset': 2, 'datatype': 'B', 'endianness': '<'},
        ]
        # Manually add some data to the data dictionary
        binary_file_dto.data = {'field1': 1, 'field2': 2, 'field3': 3}

        # Call get_data and check the result
        result = binary_file_dto.get_data()
        assert result == {'field1': 1, 'field2': 2, 'field3': 3}

@pytest.fixture
def struct_file():
    filename_struct = 'struct.arx'
    # Create a bytes object with the specific binary data
    data = struct.pack('>BHLQfd', 1, 2, 3, 4, 5.0, 6.0)
    with open(filename_struct, 'wb') as f:
        f.write(data)
    yield filename_struct
    os.remove(filename_struct)

def test_read_and_unpack(struct_file):
    # Create an instance of BinaryFileDTO
    with open(struct_file, 'rb') as f:
        binary_file_dto = BinaryFileDTO(f)
        f.seek(0)

        # Test read_and_unpack with different format strings
        assert binary_file_dto._read_and_unpack(f, '>B') == 1  # Unsigned byte
        assert binary_file_dto._read_and_unpack(f, '>H') == 2  # Unsigned short
        assert binary_file_dto._read_and_unpack(f, '>L') == 3  # Unsigned long
        assert binary_file_dto._read_and_unpack(f, '>Q') == 4  # Unsigned long long
        assert binary_file_dto._read_and_unpack(f, '>f') == 5.0  # Float
        assert binary_file_dto._read_and_unpack(f, '>d') == 6.0  # Double

@pytest.fixture
def binary_file_little_endian():
    filename = 'little_endian.ari'
    with open(filename, 'wb') as f:
        f.write(os.urandom(4))
        f.write(b'\x78\x56\x34\x12')  # Little endian magic number
        f.write(os.urandom(1024))
    yield filename
    os.remove(filename)

@pytest.fixture
def binary_file_big_endian():
    filename = 'big_endian.ari'
    with open(filename, 'wb') as f:
        f.write(os.urandom(4))
        f.write(b'\x12\x34\x56\x78')  # Big endian magic number
        f.write(os.urandom(1024))
    yield filename
    os.remove(filename)

def test_determine_endianness_little_endian(binary_file_little_endian):
    with open(binary_file_little_endian, 'rb') as f:
        binary_file_dto = BinaryFileDTO(f)
        assert binary_file_dto._determine_endianness() == '<'

def test_determine_endianness_big_endian(binary_file_big_endian):
    with open(binary_file_big_endian, 'rb') as f:
        binary_file_dto = BinaryFileDTO(f)
        assert binary_file_dto._determine_endianness() == '>'

@pytest.fixture
def binary_file_with_string():
    filename = 'string.ari'
    with open(filename, 'wb') as f:
        f.write(b'Hello, World!\x00')  # Null-terminated string
        f.write(os.urandom(1024))  # 1KB of random data
    yield filename
    os.remove(filename)

def test_read_string(binary_file_with_string):
    with open(binary_file_with_string, 'rb') as f:
        binary_file_dto = BinaryFileDTO(f)
        f.seek(0)
        result = binary_file_dto._read_string(f, 13, '>')
        assert result == 'Hello, World!'

@pytest.fixture
def binary_file_with_frameline():
    filename = 'frameline.ari'
    with open(filename, 'wb') as f:
        f.write(struct.pack('<I', 1))  # Frameline type
        frameline_name = 'MyFrameline'
        # Pad the frameline name with null bytes until it's 32 characters long
        padded_frameline_name = frameline_name.ljust(32, '\x00')
        f.write(padded_frameline_name.encode('utf-8'))
        f.write(struct.pack('<H', 10))  # Left
        f.write(struct.pack('<H', 20))  # Top
        f.write(struct.pack('<H', 30))  # Width
        f.write(struct.pack('<H', 40))  # Height
        f.write(os.urandom(1024))  # 1KB of random data
    yield filename
    os.remove(filename)

def test_read_frameline(binary_file_with_frameline):
    with open(binary_file_with_frameline, 'rb') as f:
        binary_file_dto = BinaryFileDTO(f)
        f.seek(0)
        result = binary_file_dto._read_frameline(f, '1', '>')
        assert result == {
            'FrameLine1Type': 'Master',
            'FrameLine1Name': 'MyFrameline',
            'FrameLine1Left': 10,
            'FrameLine1Top': 20,
            'FrameLine1Width': 30,
            'FrameLine1Height': 40,
        }

@pytest.mark.parametrize("data,expected", [
    (-3, 'NearClose'),
    (-2, 'Close'),
    (-1, 'Invalid'),
    (0, '0.71'),
    (1000, '1.0'),
    (2000, '1.41'),
    (3000, '2.0'),
    (4000, '2.83'),
    (1500, '1.19'),
])
def test_convert_data_to_tstop(data, expected):
    assert  BinaryFileDTO._convert_data_to_tstop(data) == expected

@pytest.fixture
def binary_file_with_tstop():
    filename = 'tstop.ari'
    with open(filename, 'wb') as f:
        f.write(struct.pack('<I', 2000))  # TStop data
        f.write(os.urandom(1024))  # 1KB of random data
    yield filename
    os.remove(filename)

def test_read_tstop(binary_file_with_tstop):
    with open(binary_file_with_tstop, 'rb') as f:
        binary_file_dto = BinaryFileDTO(f)
        f.seek(0)
        result = binary_file_dto._read_tstop(f, 'little')
        assert result == '1.41'

# @pytest.mark.parametrize("bit_positions,expected", [
#     ([0], 1),
#     ([1], 2),
#     ([0, 1], 3),
#     ([2, 3, 4], 28),
#     ([5, 6, 7, 8], 480),
#     ([], 0),
#     ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 2047)
# ])
# def test_create_bit_mask(bit_positions, expected):
#     assert BinaryFileDTO.create_bit_mask(bit_positions) == expected

@pytest.mark.parametrize("data,bit_position,endianness,expected", [
    (b'\x01\x00\x00\x00', 0, 'little', 1),
    (b'\x01\x00\x00\x00', 31, 'little', 0),
    (b'\x00\x00\x00\x01', 0, 'little', 0),
    (b'\x00\x00\x00\x80', 31, 'little', 1),
    (b'\x00\x00\x00\x01', 0, 'big', 1),
    (b'\x7F\xFF\xFF\xFF', 31, 'big', 0),
    (b'\xFF\xFF\xFF\xF0', 0, 'big', 0),
    (b'\x80\x00\x00\x00', 31, 'big', 1),
])
def test_read_bit(data, bit_position, endianness, expected):
    data = io.BytesIO(data)
    result = BinaryFileDTO._read_bit(data, bit_position, endianness)

    assert result == expected

@pytest.mark.parametrize("TCbytes,expected", [
    (binascii.unhexlify('67452301'), '01:23:45:67'),
    (binascii.unhexlify('78563412'), '12:34:56:78'),
    (binascii.unhexlify('00000000'), '00:00:00:00'),
    (binascii.unhexlify('FFFFFFFF'), 'ff:ff:ff:ff')
])
def test_bytestoTC(TCbytes, expected):
    assert BinaryFileDTO._bytes_to_time_code(TCbytes) == expected

@pytest.mark.parametrize("input_string,expected", [
    ("key1:value1;key2:value2", {"key1": "value1", "key2": "value2"}),
    ("key1: value1 ; key2 : value2 ", {"key1": "value1", "key2": "value2"}),
    ("key1:value1;key2:value2;key3:value3", {"key1": "value1", "key2": "value2", "key3": "value3"}),
    ("key1:value1", {"key1": "value1"}),
    ("", {}),
])
def test_split_user_string(input_string, expected):
    result = BinaryFileDTO._split_user_string(input_string)
    assert result == expected

@pytest.mark.parametrize("bcd, format, spacer, endianness, prefix, expected", [
    (b'\x12\x34\x56\x78', 'date', '/', '>', None, '7856/34/12'),
    (b'\x12\x34\x56\x78', 'date', '/', '<', None, '1234/56/78'),
    (b'\x12\x34\x56\x78', 'time', ':', '>', None, '78:56:34:12'),
    (b'\x12\x34\x56\x78', 'time', ':', '<', None, '12:34:56:78'),
])
def test_bcd_to_str(bcd, format, spacer, endianness, prefix, expected):
    result = BinaryFileDTO._bcd_to_str(bcd, format, spacer, endianness, prefix)
    assert result == expected

@pytest.fixture
def binary_file_dto_fields():
    filename = 'fields.ari'
    with open(filename, 'wb') as f:
        f.write(struct.pack('<B', 1))  # Left
        f.write(struct.pack('<B', 2))  # Top
        f.write(struct.pack('<B', 3))  # Width
        f.write(struct.pack('<H', 40))  # Height
        f.write(os.urandom(1024))  # 1KB of random data
    yield filename
    os.remove(filename)

def test_extract_metadata_all_fields(binary_file_dto_fields):
    # Create an instance of BinaryFileDTO with some fields
    with open(binary_file_dto_fields, 'rb') as f:
        binary_file_dto = BinaryFileDTO(f)
        binary_file_dto.fields = [
            {'name': 'field1', 'offset': 0, 'datatype': 'B', 'endianness': '<'},
            {'name': 'field2', 'offset': 1, 'datatype': 'B', 'endianness': '<'},
            {'name': 'field3', 'offset': 2, 'datatype': 'B', 'endianness': '<'},
        ]
        # Manually add some data to the data dictionary
        binary_file_dto.data = {'field1': 1, 'field2': 2, 'field3': 3}
        binary_file_dto.fields_to_extract = None

        # Call extract_metadata and check the result
        result = binary_file_dto.extract_metadata()
        assert result == {'field1': 1, 'field2': 2, 'field3': 3}

def test_extract_metadata_some_fields(binary_file_dto_fields):
    # Create an instance of BinaryFileDTO with some fields
    with open(binary_file_dto_fields, 'rb') as f:
        binary_file_dto = BinaryFileDTO(f)
        binary_file_dto.fields = [
            {'name': 'field1', 'offset': 0, 'datatype': 'B', 'endianness': '<'},
            {'name': 'field2', 'offset': 1, 'datatype': 'B', 'endianness': '<'},
            {'name': 'field3', 'offset': 2, 'datatype': 'B', 'endianness': '<'},
        ]
        # Manually add some data to the data dictionary
        binary_file_dto.data = {'field1': 1, 'field2': 2, 'field3': 3}
        binary_file_dto.fields_to_extract = ['field1', 'field3']

        # Call extract_metadata and check the result
        result = binary_file_dto.extract_metadata()
        assert result == {'field1': 1, 'field3': 3}

def test_extract_metadata_with_mapping(binary_file_dto_fields):
    # Create an instance of BinaryFileDTO with some fields
    with open(binary_file_dto_fields, 'rb') as f:
        binary_file_dto = BinaryFileDTO(f)
        binary_file_dto.fields = [
            {'name': 'field1', 'offset': 0, 'datatype': 'B', 'endianness': '>', 'mapping': {1: 'One'}},
            {'name': 'field2', 'offset': 1, 'datatype': 'B', 'endianness': '>', 'mapping': {2: 'Two'}},
            {'name': 'field3', 'offset': 2, 'datatype': 'B', 'endianness': '>'},
        ]
        # Manually add some data to the data dictionary
        binary_file_dto.data = {'field1': 1, 'field2': 2, 'field3': 3}
        binary_file_dto.fields_to_extract = None

        # Call extract_metadata and check the result
        result = binary_file_dto.extract_metadata()
        assert result

# @pytest.fixture
# def binary_file_dto(binary_file_dto_fields):
#     with open(binary_file_dto_fields, 'rb') as f:
#         return BinaryFileDTO(f)

# @pytest.mark.parametrize("field, endianness, expected", [
#     ({'datatype': 'string', 'value': 'test'}, '<', 'test'),
#     ({'datatype': 'UserString', 'value': 'user;string'}, '<', {'user': 'string'}),
# ])
# def test_handle_field(binary_file_dto, field, endianness, expected):
#     result = binary_file_dto.handle_field(field, endianness)
#     assert result == expected

pytest.main()