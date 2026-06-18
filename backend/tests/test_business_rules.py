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
# FLIGHT BUSINESS RULE TESTS
# ==========================================

def test_invalid_flight_booking():

    booking_data = {

        "user_id": 1,
        "user_name": "Tester",

        "flight_id": 9999,

        "airline": "Fake Airline",

        "source": "Delhi",
        "destination": "Mumbai",

        "departure": "08:00",
        "arrival": "10:00",

        "duration": "2h",

        "passengers": 1,

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
        "Flight Not Found"
    )


# ==========================================
# HOTEL BUSINESS RULE TESTS
# ==========================================

def test_hotel_overbooking():

    booking_data = {

        "user_id": 1,

        "user_name": "Tester",

        "hotel_id": 1,

        "hotel_name": "Taj Palace",

        "city": "Delhi",

        "room_type": "Deluxe",

        "rating": 4.8,

        "rooms_booked": 1000,

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
        "Not Enough Rooms Available"
    )


# ==========================================
# BUS BUSINESS RULE TESTS
# ==========================================

def test_bus_overbooking():

    booking_data = {

        "user_id": 1,

        "user_name": "Tester",

        "bus_id": 1,

        "operator": "RedBus Express",

        "source": "Delhi",

        "destination": "Manali",

        "departure": "08:00 PM",

        "arrival": "06:00 AM",

        "duration": "10h",

        "passengers": 100,

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
        "Not Enough Seats Available"
    )


# ==========================================
# TRAIN BUSINESS RULE TESTS
# ==========================================

def test_train_overbooking():

    booking_data = {

        "user_id": 1,

        "user_name": "Tester",

        "train_id": 1,

        "train_name": "Rajdhani Express",

        "train_number": "12951",

        "source": "Delhi",

        "destination": "Mumbai",

        "departure": "04:00 PM",

        "arrival": "08:00 AM",

        "duration": "16h",

        "passengers": 1000,

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
        "Not Enough Seats"
    )