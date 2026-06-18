from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_invalid_flight():

    payload = {

        "user_id":1,
        "user_name":"Test",

        "flight_id":9999,

        "airline":"Test",

        "source":"Delhi",

        "destination":"Mumbai",

        "departure":"10",

        "arrival":"12",

        "duration":"2h",

        "passengers":1,

        "journey_date":"2026-07-01",

        "price":5000

    }

    response = client.post(
        "/book",
        json=payload
    )

    assert response.status_code == 200

    assert response.json()["message"] == "Flight Not Found"