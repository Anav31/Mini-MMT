# Business validation rules

MODULE_RULES = {

    "flight": [

        "Passenger count must be greater than 0",

        "Passenger count cannot exceed available seats",

        "Journey date cannot be in the past"

    ],

    "hotel": [

        "Rooms booked must be greater than 0",

        "Rooms booked cannot exceed available rooms",

        "Stay date cannot be in the past"

    ],

    "bus": [

        "Passenger count must be greater than 0",

        "Seats cannot be overbooked"

    ],

    "train": [

        "Passenger count must be greater than 0",

        "Seats cannot be overbooked"

    ]
}


# Inspector Agent knowledge base

SCENARIO_RULES = {

    "negative_passengers": {

        "severity": "HIGH",

        "root_cause":
        "Validation Failure",

        "recommendation":
        "Reject passenger counts <= 0"
    },

    "negative_bus_passengers": {

        "severity": "HIGH",

        "root_cause":
        "Validation Failure",

        "recommendation":
        "Reject passenger counts <= 0"
    },

    "negative_train_passengers": {

        "severity": "HIGH",

        "root_cause":
        "Validation Failure",

        "recommendation":
        "Reject passenger counts <= 0"
    },

    "negative_rooms": {

        "severity": "MEDIUM",

        "root_cause":
        "Validation Failure",

        "recommendation":
        "Reject room counts <= 0"
    }
}