from app import app as flask_app
import pytest


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    # initialize_app(app)
    # app.config['TESTING'] = True
    return app.test_client()
