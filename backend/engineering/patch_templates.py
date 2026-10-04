VALIDATION_PATCHES = {

    "passenger_validation":

'''
if data["passengers"] <= 0:

    return {

        "message":
        "Passenger count must be greater than 0"
    }
'''
,

    "room_validation":

'''
if data["rooms_booked"] <= 0:

    return {

        "message":
        "Rooms booked must be greater than 0"
    }
'''
}