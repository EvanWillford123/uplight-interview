from unittest.mock import MagicMock, patch
from hash_generator import hash_generator


def test_generate_hash():
    """Verify that generate_hash returns the expected values"""
    input_data = {"message": "MDAwMDAwMDAtMDAwMC0wMDBiLTAxMmMtMDllZGU5NDE2MDAz"}
    output_value = hash_generator.generate_hash(input_data=input_data)
    print(f"{output_value}")
    assert len(output_value) == hash_generator.SHA3_256_OUTPUT_SIZE * 2  # hex digest is double


@patch("hash_generator.hash_generator.sha3_256")
@patch("hash_generator.hash_generator.bytearray_bitwise_xor")
@patch("hash_generator.hash_generator.compute_block_sized_key")
def test_compute_full_hmac(mock_compute_block_sized_key, mock_xor, mock_hash):
    """Verify that the compute_full_hmac function calls the expected functions"""
    mock_xor.return_value = bytearray(b"1"*hash_generator.SHA3_256_BLOCK_SIZE)

    hash_generator.compute_full_hmac(
        key=bytearray("test_key", encoding=hash_generator.STRING_ENCODING),
        message=bytearray("test_message", encoding=hash_generator.STRING_ENCODING)
    )

    mock_compute_block_sized_key.assert_called()
    mock_xor.assert_called()  # TODO: enhance with actual calls
    mock_hash.assert_called()


def test_compute_block_sized_key_greater_than_block_size():
    """Ensure that a byte array greater than the supported block size is hashed (and thus is as long
    as the hash output for our algorithm)"""
    dummy_str = "a" * (hash_generator.SHA3_256_BLOCK_SIZE + 1)
    dummy_key = bytearray(dummy_str, encoding="utf-8")
    assert len(dummy_key) > hash_generator.SHA3_256_BLOCK_SIZE
    hash_digest_value = hash_generator.compute_block_sized_key(key=dummy_key)
    assert len(hash_digest_value) == hash_generator.SHA3_256_OUTPUT_SIZE


def test_compute_block_sized_key_less_than_block_size():
    """Ensure that a smaller byte array is padded up to the maximum block size"""
    dummy_str = "a"
    dummy_key = bytearray(dummy_str, encoding="utf-8")
    assert len(dummy_key) < hash_generator.SHA3_256_BLOCK_SIZE
    hash_digest_value = hash_generator.compute_block_sized_key(key=dummy_key)
    assert len(hash_digest_value) == hash_generator.SHA3_256_BLOCK_SIZE


def test_compute_block_sized_key_equal_to_block_size():
    """Ensure that a bytearray the length of the maximum block size is returned unmodified"""
    dummy_str = "a" * hash_generator.SHA3_256_BLOCK_SIZE
    dummy_key = bytearray(dummy_str, encoding="utf-8")
    assert len(dummy_key) == hash_generator.SHA3_256_BLOCK_SIZE
    hash_digest_value = hash_generator.compute_block_sized_key(key=dummy_key)
    assert len(hash_digest_value) == hash_generator.SHA3_256_BLOCK_SIZE


def test_bytearray_bitwise_xor_equal_lengths():
    """Ensure that the bitwise xor function returns the expected value when the given bytearrays are the
    same size"""
    ba1 = bytearray("0101", encoding=hash_generator.STRING_ENCODING)
    ba2 = bytearray("1100", encoding=hash_generator.STRING_ENCODING)
    xored = hash_generator.bytearray_bitwise_xor(ba1, ba2)
    expected_value = "1001"
    converted_bytes = ""
    for byte in xored:
        converted_bytes += str(byte)

    assert converted_bytes == expected_value


def test_bytearray_bitwise_xor_b1_less_than_b2():
    """Ensure that the bitwise xor function returns the expected value when the first bytearray is
    shorter than the second (i.e. that padding works correctly in this case)"""
    ba1 = bytearray("0101", encoding=hash_generator.STRING_ENCODING)
    ba2 = bytearray("1100110", encoding=hash_generator.STRING_ENCODING)
    xored = hash_generator.bytearray_bitwise_xor(ba1, ba2)
    expected_value = "1100011"
    converted_bytes = ""
    for byte in xored:
        converted_bytes += str(byte)

    assert converted_bytes == expected_value


def test_bytearray_bitwise_xor_b1_greater_than_b2():
    """Ensure that the bitwise xor function returns the expected value when the first bytearray is
    longer than the second (i.e. that padding works correctly in this case)"""
    ba1 = bytearray("1100101", encoding=hash_generator.STRING_ENCODING)
    ba2 = bytearray("1101", encoding=hash_generator.STRING_ENCODING)
    xored = hash_generator.bytearray_bitwise_xor(ba1, ba2)
    expected_value = "1101000"
    converted_bytes = ""
    for byte in xored:
        converted_bytes += str(byte)

    assert converted_bytes == expected_value
