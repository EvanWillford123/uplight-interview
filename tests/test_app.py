import json

# Would ideally move these to constants or use enums or library
SUCCESS_CODE = 200
INVALID_REQUEST_CODE = 400


def assert_and_log(expected_value, actual_value):
    assert expected_value == actual_value, f"Expected {expected_value} but got {actual_value}"


def test_homepage(client):
    """Dumb check to make sure everything is hooked up properly"""
    assert client.get("/").status_code == 200


def test_post_generate_token_data_input_returns_200(client, app):
    """Verify that sending valid inputs and headers to the app returns a 200 and expected output"""
    test_dict = json.dumps({"id": "test"})
    expected_result = {"id": "test", "signature": "6948b9f4f47eb0dd294356a6c1e12024f2a940eb93dd16a4b557f002abe5788b"}
    response = client.post("/generate-token", headers={"Content-Type": "application/json"}, data=test_dict)

    assert_and_log(expected_value=SUCCESS_CODE, actual_value=response.status_code)
    assert_and_log(expected_value=expected_result, actual_value=response.json)


def test_post_generate_token_no_headers_returns_400(client, app):
    """Verify that sending a request without the proper headers returns a 400"""
    test_dict = json.dumps({"id": "test"})
    response = client.post("/generate-token", data=test_dict)

    assert_and_log(expected_value=INVALID_REQUEST_CODE, actual_value=response.status_code)


def test_post_generate_token_invalid_headers_returns_400(client, app):
    """Verify that sending a request without the Content-Type in the headers returns a 400"""
    test_dict = json.dumps({"id": "test"})
    response = client.post("/generate-token", headers={"doubleHeader": "lol baseball"}, data=test_dict)

    assert_and_log(expected_value=INVALID_REQUEST_CODE, actual_value=response.status_code)


def test_post_generate_token_thats_not_json_returns_400(client, app):
    """Verify that sending a request with non-JSON content-type returns a 400"""
    test_dict = json.dumps({"id": "test"})
    response = client.post("/generate-token", headers={"Content-Type": "multipart/form-data"}, data=test_dict)

    assert_and_log(expected_value=INVALID_REQUEST_CODE, actual_value=response.status_code)


def test_post_generate_token_too_many_keys_returns_400(client, app):
    """Verify that sending a request with too many keys returns a 400"""
    test_dict = json.dumps({"id": "test", "oh no!": "a second key!"})
    response = client.post("/generate-token", headers={"Content-Type": "application/json"}, data=test_dict)

    assert_and_log(expected_value=INVALID_REQUEST_CODE, actual_value=response.status_code)


def test_post_generate_token_no_keys_returns_400(client, app):
    test_dict = json.dumps({})
    response = client.post("/generate-token", headers={"Content-Type": "application/json"}, data=test_dict)

    assert_and_log(expected_value=INVALID_REQUEST_CODE, actual_value=response.status_code)
