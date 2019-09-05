from flaskr import create_app


def test_config():
    """Test 'create app' w/o passing test config."""
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, sir!'