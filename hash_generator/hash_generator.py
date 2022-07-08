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

    return signature


def compute_full_hmac(key: bytearray, message: bytearray):
    # ASSUMPTIONS
    # Using SHA3-256 (latest & greatest)
    # 136-byte internal block length
    # 32-byte output length

    # Compute block-sized key
    block_sized_key = compute_block_sized_key(key=key)

    # Compute outer padded key
    outer_padding = bytearray(b"0x5c" * int(SHA3_256_BLOCK_SIZE/len(b"0x5c")))
    outer_key_padded = bytearray_bitwise_xor(block_sized_key, bytearray(outer_padding))

    # Compute inner padded key
    inner_padding = bytearray(b"0x36" * int(SHA3_256_BLOCK_SIZE/len(b"0x36")))
    inner_key_padded = bytearray_bitwise_xor(block_sized_key, bytearray(inner_padding))

    # Combine info
    computed_signature = hashlib.sha3_256(outer_key_padded)
    computed_signature.update(hashlib.sha3_256(inner_key_padded + message).digest())
    return computed_signature.hexdigest()


def compute_block_sized_key(key: bytearray) -> bytearray:
    # If key is greater than the internal block size, truncate by hashing the whole thing
    if len(key) > SHA3_256_BLOCK_SIZE:
        key = hashlib.sha3_256(key).digest()
    else:
        # If it's less than the full block size, pad with 0s to get to the block size
        key = key.zfill(SHA3_256_BLOCK_SIZE)

    return key


def bytearray_bitwise_xor(ba1: bytearray, ba2: bytearray) -> bytearray:
    """
    Given two bytearrays, perform a bitwise XOR and return a new bytearray with the result
    If the bytearrays are of different length, left-fill the shortest one with 0s to match the length of the larger one.
    """
    xored_bytearray = bytearray()
    if len(ba1) < len(ba2):
        ba1 = ba1.zfill(len(ba2))
    elif len(ba2) < len(ba1):
        ba2 = ba2.zfill(len(ba1))
    for index, byte in enumerate(ba1):
        xored_bytearray.append(byte ^ ba2[index])

    return xored_bytearray
