from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_flights():

    response = client.get("/flights")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )