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

# ------------------------
# FLIGHT TESTS
# ------------------------

def test_get_flights():

    response = client.get("/flights")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

# ------------------------
# BUS TESTS
# ------------------------

def test_get_buses():

    response = client.get("/buses")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

# ------------------------
# TRAIN TESTS
# ------------------------

def test_get_trains():

    response = client.get("/trains")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

# ------------------------
# HOTEL TESTS
# ------------------------

def test_get_hotels():

    response = client.get("/hotels")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

# ------------------------
# FLIGHT BOOKING TEST
# ------------------------

def test_flight_booking():

    booking_data = {

        "user_id": 1,

        "user_name": "Test User",

        "flight_id": 1,

        "airline": "IndiGo",

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
        "Flight Booked Successfully"
    )

# ------------------------
# BUS BOOKING TEST
# ------------------------

def test_bus_booking():

    booking_data = {

        "user_id": 1,

        "user_name": "Test User",

        "bus_id": 1,

        "operator": "RedBus Express",

        "source": "Delhi",

        "destination": "Manali",

        "departure": "08:00 PM",

        "arrival": "06:00 AM",

        "duration": "10h",

        "passengers": 1,

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
        "Bus Booked Successfully"
    )

# ------------------------
# TRAIN BOOKING TEST
# ------------------------

def test_train_booking():

    booking_data = {

        "user_id": 1,

        "user_name": "Test User",

        "train_id": 1,

        "train_name":
        "Rajdhani Express",

        "train_number": "12951",

        "source": "Delhi",

        "destination": "Mumbai",

        "departure": "04:00 PM",

        "arrival": "08:00 AM",

        "duration": "16h",

        "passengers": 1,

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
        "Train Booked Successfully"
    )

# ------------------------
# HOTEL BOOKING TEST
# ------------------------

def test_hotel_booking():

    booking_data = {

        "user_id": 1,

        "user_name": "Test User",

        "hotel_id": 1,

        "hotel_name":
        "Taj Palace",

        "city": "Delhi",

        "room_type": "Deluxe",

        "rating": 4.8,

        "rooms_booked": 1,

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
        "Hotel Booked Successfully"
    )