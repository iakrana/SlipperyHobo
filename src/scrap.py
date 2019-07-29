import gzip
import json
from io import BytesIO


# def decompressBytesToString(inputBytes):
#     """
#     decompress the given byte array (which must be valid
#     compressed gzip data) and return the decoded text (utf-8).
#     """
#     bio = BytesIO()
#     stream = BytesIO(inputBytes)
#     decompressor = gzip.GzipFile(fileobj=stream, mode='r')
#     while True:  # until EOF
#         chunk = decompressor.read(8192)
#         if not chunk:
#             decompressor.close()
#             bio.seek(0)
#             return bio.read().decode("utf-8")
#         bio.write(chunk)
#     return None
#
#
# def compressStringToBytes(inputString):
#     """
#     read the given string, encode it in utf-8,
#     compress the data and return it as a byte array.
#     """
#     bio = BytesIO()
#     bio.write(inputString.encode("utf-8"))
#     bio.seek(0)
#     stream = BytesIO()
#     compressor = gzip.GzipFile(fileobj=stream, mode='w')
#     while True:  # until EOF
#         chunk = bio.read(8192)
#         if not chunk:  # EOF?
#             compressor.close()
#             return stream.getvalue()
#         compressor.write(chunk)


# Read result all_items
with open("../data/items_20190727-100411.json") as json_file:
    data = json.load(json_file)
#
#
# with gzip.GzipFile('data.gz','w') as fid_gz:
#     with open('../test_data/char_item.json', 'r') as fid_json:
#         json_dict = item_data
#         json_str = str(json_dict)
#         # bytes(string, encoding)
#         json_bytes = bytes(json_str,'utf8')
#     fid_gz.write(json_bytes)

jsonfilename = "../data/items_20190727-100411.json.gz"


with gzip.GzipFile(jsonfilename, 'w') as fout:
    fout.write(json.dumps(data).encode('utf-8'))


# with gzip.GzipFile(jsonfilename, 'r') as fin:
#     data = json.loads(fin.read().decode('utf-8'))

# print(data)
# >> > bytearray(newFileBytes)
# bytearray(b'{\x03\xff\x00d')
# >> > bytes(newFileBytes)
# b'{\x03\xff\x00d'
