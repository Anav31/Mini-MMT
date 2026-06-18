SCENARIOS = [

    # =====================================
    # FLIGHT SCENARIOS
    # =====================================

    {
        "module": "flight",

        "name": "negative_passengers",

        "expected":
        "Passenger count must be greater than 0",

        "endpoint": "/book",

        "payload": {

            "user_id": 1,

            "user_name": "Agent User",

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
    },

    {
        "module": "flight",

        "name": "valid_booking",

        "expected":
        "Flight Booked Successfully",

        "endpoint": "/book",

        "payload": {

            "user_id": 1,

            "user_name": "Agent User",

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
    },

    # =====================================
    # HOTEL SCENARIOS
    # =====================================

    {
        "module": "hotel",

        "name": "negative_rooms",

        "expected":
        "Rooms booked must be greater than 0",

        "endpoint": "/book-hotel",

        "payload": {

            "user_id": 1,

            "user_name": "Agent User",

            "hotel_id": 1,

            "hotel_name": "Taj Palace",

            "city": "Delhi",

            "room_type": "Deluxe",

            "rating": 4.8,

            "rooms_booked": -2,

            "stay_date": "2026-06-01",

            "price": 8500
        }
    },

    # =====================================
    # BUS SCENARIOS
    # =====================================

    {
        "module": "bus",

        "name": "negative_bus_passengers",

        "expected":
        "Passenger count must be greater than 0",

        "endpoint": "/book-bus",

        "payload": {

            "user_id": 1,

            "user_name": "Agent User",

            "bus_id": 1,

            "operator": "RedBus Express",

            "source": "Delhi",

            "destination": "Manali",

            "departure": "08:00 PM",

            "arrival": "06:00 AM",

            "duration": "10h",

            "passengers": -3,

            "journey_date": "2026-06-01",

            "price": 1200
        }
    },

    # =====================================
    # TRAIN SCENARIOS
    # =====================================

    {
        "module": "train",

        "name": "negative_train_passengers",

        "expected":
        "Passenger count must be greater than 0",

        "endpoint": "/book-train",

        "payload": {

            "user_id": 1,

            "user_name": "Agent User",

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
    }
]