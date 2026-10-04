TEST_TEMPLATES = {

    "book_flight":

'''
def test_negative_passengers():

    booking_data = {

        "user_id": 1,
        "user_name": "Tester",
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

    assert (
        response.json()["message"]
        ==
        "Passenger count must be greater than 0"
    )
'''
,

    "book_bus":

'''
def test_negative_bus_passengers():

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
        "passengers": -5,
        "journey_date": "2026-06-01",
        "price": 1200
    }

    response = client.post(
        "/book-bus",
        json=booking_data
    )

    assert (
        response.json()["message"]
        ==
        "Passenger count must be greater than 0"
    )
'''
,

    "book_train":

'''
def test_negative_train_passengers():

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
        "passengers": -5,
        "journey_date": "2026-06-01",
        "price": 2200
    }

    response = client.post(
        "/book-train",
        json=booking_data
    )

    assert (
        response.json()["message"]
        ==
        "Passenger count must be greater than 0"
    )
'''
,

    "book_hotel":

'''
def test_negative_rooms():

    booking_data = {

        "user_id": 1,
        "user_name": "Tester",
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

    assert (
        response.json()["message"]
        ==
        "Rooms booked must be greater than 0"
    )
'''
}