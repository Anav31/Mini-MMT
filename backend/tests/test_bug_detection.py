import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


# ==========================================
# NEGATIVE PASSENGER TEST
# ==========================================

def test_negative_flight_passengers():

    booking_data = {

        "user_id": 1,

        "user_name": "Bug Tester",

        "flight_id": 1,

        "airline": "IndiGo",

        "source": "Delhi",

        "destination": "Mumbai",

        "departure": "08:00",

        "arrival": "10:00",

        "duration": "2h",

        "passengers": -5,

        "journey_date": "2026-06-01",

        "price": 5000
    }

    response = client.post(
        "/book",
        json=booking_data
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        ==
        "Passenger count must be greater than 0"
    )


# ==========================================
# NEGATIVE BUS PASSENGERS
# ==========================================

def test_negative_bus_passengers():

    booking_data = {

        "user_id": 1,

        "user_name": "Bug Tester",

        "bus_id": 1,

        "operator": "RedBus Express",

        "source": "Delhi",

        "destination": "Manali",

        "departure": "08:00 PM",

        "arrival": "06:00 AM",

        "duration": "10h",

        "passengers": -2,

        "journey_date": "2026-06-01",

        "price": 1200
    }

    response = client.post(
        "/book-bus",
        json=booking_data
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        ==
        "Passenger count must be greater than 0"
    )


# ==========================================
# NEGATIVE TRAIN PASSENGERS
# ==========================================

def test_negative_train_passengers():

    booking_data = {

        "user_id": 1,

        "user_name": "Bug Tester",

        "train_id": 1,

        "train_name": "Rajdhani Express",

        "train_number": "12951",

        "source": "Delhi",

        "destination": "Mumbai",

        "departure": "04:00 PM",

        "arrival": "08:00 AM",

        "duration": "16h",

        "passengers": -10,

        "journey_date": "2026-06-01",

        "price": 2200
    }

    response = client.post(
        "/book-train",
        json=booking_data
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        ==
        "Passenger count must be greater than 0"
    )


# ==========================================
# NEGATIVE HOTEL ROOMS
# ==========================================

def test_negative_rooms_booking():

    booking_data = {

        "user_id": 1,

        "user_name": "Bug Tester",

        "hotel_id": 1,

        "hotel_name": "Taj Palace",

        "city": "Delhi",

        "room_type": "Deluxe",

        "rating": 4.8,

        "rooms_booked": -1,

        "stay_date": "2026-06-01",

        "price": 8500
    }

    response = client.post(
        "/book-hotel",
        json=booking_data
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        ==
        "Rooms booked must be greater than 0"
    )