# uplight-interview
## Evan Willford's Flask REST API HMAC Generator for the Uplight Interview

This project contains a basic Flask API with one interesting endpoint - a POST /generate-token endpoint that, given a 
dictionary with a key/value pair, generates an HMAC signature and returns it along with the initial input.

The Flask API factory and conftest were shamelessly stolen from the Flask documentation, although any glaring errors
are likely mine.

The hash_generator module contains the logic for actually generating the token.  I decided against implementing a
class for the sake of simplicity, although I am happy to discuss the ways in which we could generalize the approach
and the advantages a class-based approach would have over the simple function-based approach that I chose to implement
for this particular exercise.  I decided to make use of the SHA3-256 hash function as implemented by the hashlib library
as it seems to be one of the latest & greatest hashing algorithms.  I attempted to make it easy to add or change 
hashing algorithms, although there are certainly ways in which my approach could be improved.

# Installation & Setup
1. Ensure that you have [Python 3.10](https://www.python.org/downloads/release/python-3100/) and pip installed on your system.
2. Clone down this repository
   ```git clone https://github.com/EvanWillford123/uplight-interview.git```
3. CD into the uplight-interview directory
4. Create a virtual environment, e.g. (on Mac/Linux)

    ```python3 -m venv venv```
5. Activate the virtual environment

   ```. venv/bin/activate```
6. Install the requirements
   
    ```pip install -r requirements.txt```
7. Set the FLASK_APP environment variable so that Flask knows what application it needs to run.

   ```export FLASK_APP=server```
8. Run the server by running ```flask run```.

   NOTE: By default, this will start the server on localhost:5000. To use a port other than port 5000, you may provide the optional --port argument along with the port that you would prefer to use. 

9. Send a POST request with the appropriate headers and data to http://localhost:5000/generate-token

    NOTE: attempting to send a curl call using Windows command prompt will result in an error, as you must specify utf-8
    in the headers. I decided against implementing additional header-parsing logic for this particular case in the hopes
    that you lovely people are *nix users.

       e.g. curl command:
       ```curl http://localhost:5000/generate-token --request POST --header 'Content-Type: application/json' --data '{"id": "MDAwMDAwMDAtMDAwMC0wMDBiLTAxMmMtMDllZGU5NDE2MDAz"}```

# Testing
This repository contains unit tests for both the flask application and the hash generation logic.

In order to run the unit tests, follow steps 1-5 above.  Once you have set up the respository, your virtual environment, and the dependencies,
it is simple to run the unit tests.  Simply run ```pytest``` from the root of the project in order to run all unit tests.

If you wish to run the unit tests and see test coverage, run ```coverage run -m pytest```

# Resources Used
This list encompasses the primary resources that I utilized.  Of course, the Almighty Google provided aid along the way,
but I tried to primarily restrict myself to official documentation and (in the case of Flask) official tutorials.

* HMAC Wikipedia page: https://en.wikipedia.org/wiki/HMAC
* Hashlib documentation: https://docs.python.org/3/library/hashlib.html
* Flask v2.1 documentation (specifically including Quickstart and Tutorial): https://flask.palletsprojects.com/en/2.1.x/
* Pytest v6.2 documentation: https://docs.pytest.org/en/6.2.x/index.html
* Code Beautify's HMAC Generator (to create test data): https://codebeautify.org/hmac-generator
* JSON documentation: https://docs.python.org/3/library/json.html
* Python3 builtin docs: https://docs.python.org/3/library/functions.html
* NumPy docs: https://numpy.org/doc/stable/reference/generated/numpy.bitwise_xor.html
* Online HMAC generator (with SHA3-256 option, for test data): https://www.liavaag.org/English/SHA-Generator/HMAC/
* Unittest.mock (because I always have to reference this): https://docs.python.org/3/library/unittest.mock.html