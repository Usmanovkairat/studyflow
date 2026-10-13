import pytest
from studyflow import create_app

@pytest.fixture
def app(tmp_path):
    return create_app({'TESTING': True, 'DATABASE': str(tmp_path / 'test.sqlite'), 'SECRET_KEY': 'test-secret'})

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def token(client):
    client.get('/')
    with client.session_transaction() as session:
        session['csrf_token'] = 'test-token'
    return 'test-token'
