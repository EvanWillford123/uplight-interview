from hashlib import sha3_256


# TODO: Figure out how best to store this
SHA3_256_BLOCK_SIZE = 136
SHA3_256_OUTPUT_SIZE = 32
STRING_ENCODING = "utf-8"


def generate_hash(input_data: dict) -> str:
    # ASSUME that the key in the request data dict is the key to the hash function
    # We've verified that there's only one dictkey in the input data dict, so grab that for our key
    key = list(input_data.keys())[0]
    message = input_data[key]

    # Convert key and message to bytearray (advantages: mutable, easier)
    key_byte_array = bytearray(key, encoding=STRING_ENCODING)
    message_byte_array = bytearray(message, encoding=STRING_ENCODING)

    # Just return the string; the calling function will do what it needs to with it
    return compute_full_hmac(key=key_byte_array, message=message_byte_array)


def compute_full_hmac(key: bytearray, message: bytearray):
    """Using the HMAC algorithm defined here, https://en.wikipedia.org/wiki/HMAC, generate a signature given a
    key and a message.

    NOTE: this approach uses the SHA3-256 hashing algorithm.

    Args:
        key: the key to use in encrypting the message, in bytarray form.
        message: the message to encrypt, in bytearray form.
    Returns:
        A string representing the computed signature, in hexadecimal form.
    """
    # Compute block-sized key
    block_sized_key = compute_block_sized_key(key=key)

    # Compute outer padded key
    outer_padding = bytearray(b"0x5c" * int(SHA3_256_BLOCK_SIZE/len(b"0x5c")))
    outer_key_padded = bytearray_bitwise_xor(block_sized_key, bytearray(outer_padding))

    # Compute inner padded key
    inner_padding = bytearray(b"0x36" * int(SHA3_256_BLOCK_SIZE/len(b"0x36")))
    inner_key_padded = bytearray_bitwise_xor(block_sized_key, bytearray(inner_padding))

    # Combine info
    computed_signature = sha3_256(outer_key_padded)
    computed_signature.update(sha3_256(inner_key_padded + message).digest())
    return computed_signature.hexdigest()


def compute_block_sized_key(key: bytearray) -> bytearray:
    """
    Given a key as a bytearray, return an appropriately-sized bytearray key.
    If the key is greater than the maximum SHA3-256 block size, then truncate it using the hash function and return the
        hash digest value.
    If the key is less than the maximum block size, left-pad it with zeros until it is the maximum size and return that
        bytearray.
    Else, if the key is exactly the block size, just return it unmodified.

    Args:
        key: A bytearray containing the key provided by the user.
    Returns:
        key: The (potentially) modified key that will either be a hashed value of the original key or a zero-padded
            version of the key.
    """
    # If key is greater than the internal block size, truncate by hashing the whole thing
    if len(key) > SHA3_256_BLOCK_SIZE:
        key = bytearray(sha3_256(key).digest())
    else:
        # If it's less than the full block size, pad with 0s to get to the block size
        key = key.zfill(SHA3_256_BLOCK_SIZE)

    return key


def bytearray_bitwise_xor(ba1: bytearray, ba2: bytearray) -> bytearray:
    """
    Given two bytearrays, perform a bitwise XOR and return a new bytearray with the result.
    If the bytearrays are of different length, left-fill the shortest one with 0s to match the length of the larger one.

    Args:
        ba1: A bytearray containing data that we want to bitwise XOR.
        ba2: A bytearray containing data that we want to bitwise XOR.
    Returns:
        xored_bytearray: A bytearray containing the results of the bitwise XOR.
    """
    xored_bytearray = bytearray()
    if len(ba1) < len(ba2):
        ba1 = ba1.zfill(len(ba2))
    elif len(ba2) < len(ba1):
        ba2 = ba2.zfill(len(ba1))
    for index, byte in enumerate(ba1):
        xored_bytearray.append(byte ^ ba2[index])

    return xored_bytearray
