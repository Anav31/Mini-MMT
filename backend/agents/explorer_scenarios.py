FLIGHT_FUZZ_CASES = [

    {
        "name":
        "negative_passengers",

        "payload": {

            "user_id": 1,
            "user_name": "Explorer",

            "flight_id": 1,

            "airline": "IndiGo",

            "source": "Delhi",

            "destination": "Mumbai",

            "departure": "08:00",

            "arrival": "10:00",

            "duration": "2h",

            "passengers": -5,

            "journey_date":
            "2026-06-01",

            "price": 5000
        }
    },

    {
        "name":
        "zero_passengers",

        "payload": {

            "user_id": 1,
            "user_name": "Explorer",

            "flight_id": 1,

            "airline": "IndiGo",

            "source": "Delhi",

            "destination": "Mumbai",

            "departure": "08:00",

            "arrival": "10:00",

            "duration": "2h",

            "passengers": 0,

            "journey_date":
            "2026-06-01",

            "price": 5000
        }
    },

    {
        "name":
        "invalid_flight",

        "payload": {

            "user_id": 1,
            "user_name": "Explorer",

            "flight_id": 99999,

            "airline": "IndiGo",

            "source": "Delhi",

            "destination": "Mumbai",

            "departure": "08:00",

            "arrival": "10:00",

            "duration": "2h",

            "passengers": 1,

            "journey_date":
            "2026-06-01",

            "price": 5000
        }
    }
]