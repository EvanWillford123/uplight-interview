import os
import json

from flask import Flask, abort, request

import hash_generator.hash_generator


# Startup stuff copied from Flask tutorial
def create_app(test_config=None):
    # create and configure the app
    # TODO: Make a class that inherits from Flask?
    # TODO: HTTPS? Don't want to reveal our secret message.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'  # TODO: Make this a random string?
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.get("/")
    def homepage():
        """Return a homepage for sanity-checking and helping to build out tests"""
        return "<p>Hello, world!</p>"

    @app.post("/generate-token")
    def generate_token():
        # If user did not provide appropriate headers or data, return a 400 error
        # NOTE: If 'Content-Type' key is not present in headers, it will also throw a 400
        if not request.headers.get("Content-Type")\
                or request.headers["Content-Type"] != "application/json"\
                or not request.data:
            abort(400)  # TODO Return 400 (invalid request) - should add messaging for usability

        request_json = json.loads(request.data)

        # Make sure that we have a valid input for the actual hash function
        # (i.e. one k/v pair, message of appropriate length??)
        if not len(request_json.keys()) == 1:
            abort(400)  # TODO Add messaging for usability
        # TODO: Enforce particular string encoding? For now, assume UTF-8
        # TODO: Sanitize input

        try:
            signature = hash_generator.hash_generator.generate_hash(input_data=request_json)
            request_json["signature"] = signature
            return request_json
        except ValueError:
            abort(400)  # We received an invalid value and need to quit
        # Other exceptions will be raised
        # Enhancements: define custom exceptions with clear messaging & tie them to response codes

    return app
