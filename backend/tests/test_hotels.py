from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_hotels():

    response = client.get("/hotels")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )