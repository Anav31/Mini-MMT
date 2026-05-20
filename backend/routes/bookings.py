from fastapi import APIRouter

from database import conn, cursor

import random

router = APIRouter()

def generate_pnr():

    return "MMT" + str(
        random.randint(10000, 99999)
    )

def generate_booking_id():

    return "BK" + str(
        random.randint(1000, 9999)
    )

@router.post("/book")

def book_flight(data: dict):

    cursor.execute("""

    SELECT * FROM flights
    WHERE id = ?

    """, (data["flight_id"],))

    flight = cursor.fetchone()

    if not flight:

        return {
            "message": "Flight Not Found"
        }

    if flight["seats"] < data["passengers"]:

        return {
            "message":
            "Not Enough Seats Available"
        }

    new_seats = (
        flight["seats"]
        - data["passengers"]
    )

    cursor.execute("""

    UPDATE flights
    SET seats = ?
    WHERE id = ?

    """, (
        new_seats,
        data["flight_id"]
    ))

    pnr = generate_pnr()

    booking_id = generate_booking_id()

    cursor.execute("""

    INSERT INTO bookings (

        user_id,
        user_name,
        flight_id,
        airline,
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

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        data["user_id"],
        data["user_name"],
        data["flight_id"],
        data["airline"],
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
        "Flight Booked Successfully"
    }

@router.get("/bookings")

def get_bookings():

    cursor.execute("SELECT * FROM bookings")

    bookings = cursor.fetchall()

    return [dict(b) for b in bookings]

@router.delete("/cancel/{booking_id}")

def cancel_booking(booking_id: str):

    cursor.execute("""

    SELECT * FROM bookings
    WHERE booking_id = ?

    """, (booking_id,))

    booking = cursor.fetchone()

    if not booking:

        return {
            "message": "Booking Not Found"
        }

    cursor.execute("""

    SELECT * FROM flights
    WHERE id = ?

    """, (booking["flight_id"],))

    flight = cursor.fetchone()

    updated_seats = (
        flight["seats"]
        + booking["passengers"]
    )

    cursor.execute("""

    UPDATE flights
    SET seats = ?
    WHERE id = ?

    """, (
        updated_seats,
        booking["flight_id"]
    ))

    cursor.execute("""

    DELETE FROM bookings
    WHERE booking_id = ?

    """, (booking_id,))

    conn.commit()

    return {
        "message":
        "Booking Cancelled Successfully"
    }