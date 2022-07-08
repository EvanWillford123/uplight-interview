import pytest
from server import create_app


"""
Very simple conftest for unit tests - borrowed & simplified from the Flask tutorial
"""


@pytest.fixture
def app():
    """Creates and returns our server application for use in unit testing"""
    app = create_app({
        'TESTING': True,
    })

    yield app


@pytest.fixture
def client(app):
    """Creates and returns a client which can make test calls to the given app object"""
    return app.test_client()
