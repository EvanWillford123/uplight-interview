import hashlib
import numpy


# TODO: Figure out how best to store this
SHA3_256_BLOCK_SIZE = 136
SHA3_256_OUTPUT_SIZE = 32
STRING_ENCODING = "utf-8"

# TODO: Open question: class or function
# Pros of class: easier to unit test? Less passing of variables. Could have subclasses for different hashing algos?
# Cons of class: more overhead
# class HashGenerator:
#     @staticmethod
#     def generate_hash(input_data: dict) -> str:
#         # ASSUME that the key in the request data dict is the key to the hash function
#         print(f"In generate_hash, with input data {input_data}")
#         key = input_data.keys()
#         return "signatureValue"
#


def generate_hash(input_data: dict) -> str:
    # ASSUME that the key in the request data dict is the key to the hash function
    print(f"In generate_hash, with input data {input_data}")
    key = list(input_data.keys())[0]
    message = input_data[key]

    # Convert key and message to bytearray (advantages: mutable, easier)
    key_byte_array = bytearray(key, encoding=STRING_ENCODING)
    message_byte_array = bytearray(message, encoding=STRING_ENCODING)

    signature = compute_full_hmac(key=key_byte_array, message=message_byte_array)

    return signature  # .decode(encoding=STRING_ENCODING, errors="ignore")


def compute_full_hmac(key: bytearray, message: bytearray):
    # ASSUMPTIONS
    # Using SHA3-256 (latest & greatest)
    # 136-byte internal block length
    # 32-byte output length

    # Compute block-sized key
    block_sized_key = compute_block_sized_key(key=key)

    # Compute outer padded key
    # TODO: enhance to handle different possible lengths
    outer_padding = bytearray(b"0x5c" * 8)  # Duplicate 8 times to get to 32
    outer_key_padded = bytearray_bitwise_xor(block_sized_key, bytearray(outer_padding))

    # Compute inner padded key
    # TODO: enhance to handle different possible lengths
    inner_padding = bytearray(b"0x36" * 8)
    inner_key_padded = bytearray_bitwise_xor(block_sized_key, bytearray(inner_padding))

    # Combine info
    computed_signature = hashlib.sha3_256(outer_key_padded + hashlib.sha3_256(inner_key_padded + message).digest())
    return computed_signature.hexdigest()


def compute_block_sized_key(key: bytearray) -> bytearray:
    # If key is greater than or equal to the internal block size, truncate by hashing the whole thing
    if len(key) >= SHA3_256_BLOCK_SIZE:
        key = hashlib.sha3_256(key)
    else:
        # If it's less than the full block size, pad with 0s to get to the block size before hashing
        key = hashlib.sha3_256(pad_byte_array(value_to_pad=key))

    return bytearray(key.digest())


def bytearray_bitwise_xor(ba1: bytearray, ba2: bytearray) -> bytearray:
    """Given two bytearrays of equal length, perform a bitwise XOR and return a new bytearray with the result"""
    assert len(ba1) == len(ba2)
    xored_bytearray = bytearray()
    for index, byte in enumerate(ba1):
        xored_bytearray.append(byte ^ ba2[index])

    return xored_bytearray


def pad_byte_array(value_to_pad: bytearray) -> bytearray:
    # TODO test around the off-by-one
    zeros_to_pad = SHA3_256_BLOCK_SIZE - len(value_to_pad)
    return value_to_pad.zfill(zeros_to_pad)
