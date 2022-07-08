from hash_generator import hash_generator


def test_generate_hash():
    output_value = hash_generator.generate_hash(
        input_data={"message": "test_data"}
    )
    expected_value = "16d5578cb76c190f310bd502d3439fa975aef510772d60c6446613d6f600a955"
    assert output_value == expected_value, \
        f"expected {expected_value}, got {output_value}"


def test_compute_full_hmac():
    assert False is True


def test_compute_block_sized_key():
    assert False is True
