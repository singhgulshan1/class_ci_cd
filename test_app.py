import pytest
import io
from bg_remover_app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_no_image_uploaded(client):
    """Test API behavior when no image is sent in the request."""
    response = client.post('/remove-bg')
    assert response.status_code == 400
    assert b"No image uploaded" in response.data

def test_empty_image_selected(client):
    """Test API behavior when an empty file is sent."""
    data = {'image': (io.BytesIO(b""), '')}
    response = client.post('/remove-bg', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b"No image selected" in response.data