from fastapi import APIRouter

from database import conn, cursor

import random

router = APIRouter()

# INSERT DEFAULT TRAINS

cursor.execute(
    "SELECT COUNT(*) FROM trains"
)

count = cursor.fetchone()[0]

if count == 0:

    trains = [

        (
            "Rajdhani Express",
            "12951",
            "Delhi",
            "Mumbai",
            "04:00 PM",
            "08:00 AM",
            "16h",
            120,
            2200
        ),

        (
            "Shatabdi Express",
            "12001",
            "Delhi",
            "Chandigarh",
            "06:00 AM",
            "09:30 AM",
            "3h 30m",
            80,
            950
        ),

        (
            "Duronto Express",
            "12213",
            "Mumbai",
            "Pune",
            "08:00 AM",
            "11:00 AM",
            "3h",
            90,
            750
        ),

        (
            "Garib Rath",
            "12909",
            "Delhi",
            "Jaipur",
            "10:00 PM",
            "04:00 AM",
            "6h",
            100,
            650
        ),

        (
            "Vande Bharat",
            "22436",
            "Delhi",
            "Varanasi",
            "06:00 AM",
            "02:00 PM",
            "8h",
            70,
            1800
        ),

        (
            "Tejas Express",
            "22119",
            "Mumbai",
            "Goa",
            "07:00 AM",
            "03:00 PM",
            "8h",
            60,
            1900
        ),

        (
            "Humsafar Express",
            "22913",
            "Ahmedabad",
            "Bangalore",
            "05:00 PM",
            "11:00 AM",
            "18h",
            110,
            2400
        ),

        (
            "Jan Shatabdi",
            "12075",
            "Chennai",
            "Bangalore",
            "07:00 AM",
            "01:00 PM",
            "6h",
            95,
            850
        ),

        (
            "Intercity Express",
            "12127",
            "Lucknow",
            "Kanpur",
            "09:00 AM",
            "11:30 AM",
            "2h 30m",
            85,
            400
        ),

        (
            "Superfast Express",
            "12627",
            "Hyderabad",
            "Chennai",
            "08:00 PM",
            "07:00 AM",
            "11h",
            130,
            1500
        )

    ]

    cursor.executemany("""

    INSERT INTO trains (

        train_name,
        train_number,
        source,
        destination,
        departure,
        arrival,
        duration,
        seats,
        price

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, trains)

    conn.commit()

def generate_pnr():

    return "TRN" + str(
        random.randint(10000, 99999)
    )

def generate_booking_id():

    return "TRBK" + str(
        random.randint(1000, 9999)
    )

@router.get("/trains")

def get_trains():

    cursor.execute(
        "SELECT * FROM trains"
    )

    trains = cursor.fetchall()

    return [dict(train)
            for train in trains]

@router.post("/book-train")

def book_train(data: dict):

    cursor.execute("""

    SELECT * FROM trains
    WHERE id = ?

    """, (data["train_id"],))

    train = cursor.fetchone()

    if not train:

        return {
            "message":
            "Train Not Found"
        }

    if train["seats"] < data["passengers"]:

        return {
            "message":
            "Not Enough Seats"
        }

    updated_seats = (

        train["seats"]

        - data["passengers"]

    )

    cursor.execute("""

    UPDATE trains
    SET seats = ?
    WHERE id = ?

    """, (

        updated_seats,

        data["train_id"]

    ))

    pnr = generate_pnr()

    booking_id = generate_booking_id()

    cursor.execute("""

    INSERT INTO train_bookings (

        user_id,
        user_name,
        train_id,
        train_name,
        train_number,
        source,
        destination,
        departure,
        arrival,
        duration,
        passengers,
        journey_date,
        price,
        pnr,
        booking_id

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        data["user_id"],
        data["user_name"],
        data["train_id"],
        data["train_name"],
        data["train_number"],
        data["source"],
        data["destination"],
        data["departure"],
        data["arrival"],
        data["duration"],
        data["passengers"],
        data["journey_date"],
        data["price"],
        pnr,
        booking_id

    ))

    conn.commit()

    return {
        "message":
        "Train Booked Successfully"
    }

@router.get("/train-bookings")

def get_train_bookings():

    cursor.execute(
        "SELECT * FROM train_bookings"
    )

    bookings = cursor.fetchall()

    return [dict(b)
            for b in bookings]

@router.delete(
    "/cancel-train/{booking_id}"
)

def cancel_train_booking(
    booking_id: str
):

    cursor.execute("""

    SELECT * FROM train_bookings
    WHERE booking_id = ?

    """, (booking_id,))

    booking = cursor.fetchone()

    if not booking:

        return {
            "message":
            "Booking Not Found"
        }

    cursor.execute("""

    SELECT * FROM trains
    WHERE id = ?

    """, (booking["train_id"],))

    train = cursor.fetchone()

    updated_seats = (

        train["seats"]

        + booking["passengers"]

    )

    cursor.execute("""

    UPDATE trains
    SET seats = ?
    WHERE id = ?

    """, (

        updated_seats,

        booking["train_id"]

    ))

    cursor.execute("""

    DELETE FROM train_bookings
    WHERE booking_id = ?

    """, (booking_id,))

    conn.commit()

    return {
        "message":
        "Train Booking Cancelled"
    }