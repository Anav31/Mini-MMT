from fastapi import APIRouter

from database import conn, cursor

import random

router = APIRouter()

# INSERT DEFAULT HOTELS

cursor.execute(
    "SELECT COUNT(*) FROM hotels"
)

count = cursor.fetchone()[0]

if count == 0:

    hotels = [

        (
            "Taj Palace",
            "Delhi",
            "Deluxe",
            4.8,
            20,
            8500
        ),

        (
            "Oberoi Grand",
            "Mumbai",
            "Suite",
            4.7,
            15,
            12000
        ),

        (
            "ITC Royal",
            "Bangalore",
            "Standard",
            4.5,
            25,
            6000
        ),

        (
            "Leela Palace",
            "Chennai",
            "Deluxe",
            4.6,
            18,
            7500
        ),

        (
            "Radisson Blu",
            "Hyderabad",
            "Suite",
            4.4,
            12,
            9500
        ),

        (
            "Holiday Inn",
            "Goa",
            "Standard",
            4.3,
            30,
            5500
        ),

        (
            "Marriott",
            "Pune",
            "Deluxe",
            4.7,
            22,
            8200
        ),

        (
            "Vivanta",
            "Jaipur",
            "Suite",
            4.5,
            14,
            9800
        )

    ]

    cursor.executemany("""

    INSERT INTO hotels (

        hotel_name,
        city,
        room_type,
        rating,
        rooms,
        price

    )

    VALUES (?, ?, ?, ?, ?, ?)

    """, hotels)

    conn.commit()

# GENERATE PNR

def generate_pnr():

    return "HTL" + str(
        random.randint(10000, 99999)
    )

# GENERATE BOOKING ID

def generate_booking_id():

    return "HTBK" + str(
        random.randint(1000, 9999)
    )

# GET HOTELS

@router.get("/hotels")

def get_hotels():

    cursor.execute(
        "SELECT * FROM hotels"
    )

    hotels = cursor.fetchall()

    return [
        dict(hotel)
        for hotel in hotels
    ]

# BOOK HOTEL

@router.post("/book-hotel")

def book_hotel(data: dict):

    cursor.execute("""

    SELECT * FROM hotels
    WHERE id = ?

    """, (data["hotel_id"],))

    hotel = cursor.fetchone()

    if not hotel:

        return {
            "message":
            "Hotel Not Found"
        }

    if hotel["rooms"] < data["rooms_booked"]:

        return {
            "message":
            "Not Enough Rooms Available"
        }

    updated_rooms = (

        hotel["rooms"]

        - data["rooms_booked"]

    )

    cursor.execute("""

    UPDATE hotels
    SET rooms = ?
    WHERE id = ?

    """, (

        updated_rooms,

        data["hotel_id"]

    ))

    pnr = generate_pnr()

    booking_id = generate_booking_id()

    cursor.execute("""

    INSERT INTO hotel_bookings (

        user_id,
        user_name,
        hotel_id,
        hotel_name,
        city,
        room_type,
        rating,
        rooms_booked,
        stay_date,
        price,
        pnr,
        booking_id

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        data["user_id"],
        data["user_name"],
        data["hotel_id"],
        data["hotel_name"],
        data["city"],
        data["room_type"],
        data["rating"],
        data["rooms_booked"],
        data["stay_date"],
        data["price"],
        pnr,
        booking_id

    ))

    conn.commit()

    return {
        "message":
        "Hotel Booked Successfully"
    }

# GET HOTEL BOOKINGS

@router.get("/hotel-bookings")

def get_hotel_bookings():

    cursor.execute(
        "SELECT * FROM hotel_bookings"
    )

    bookings = cursor.fetchall()

    return [
        dict(b)
        for b in bookings
    ]

# CANCEL HOTEL BOOKING

@router.delete(
    "/cancel-hotel/{booking_id}"
)

def cancel_hotel_booking(
    booking_id: str
):

    cursor.execute("""

    SELECT * FROM hotel_bookings
    WHERE booking_id = ?

    """, (booking_id,))

    booking = cursor.fetchone()

    if not booking:

        return {
            "message":
            "Booking Not Found"
        }

    cursor.execute("""

    SELECT * FROM hotels
    WHERE id = ?

    """, (booking["hotel_id"],))

    hotel = cursor.fetchone()

    updated_rooms = (

        hotel["rooms"]

        + booking["rooms_booked"]

    )

    cursor.execute("""

    UPDATE hotels
    SET rooms = ?
    WHERE id = ?

    """, (

        updated_rooms,

        booking["hotel_id"]

    ))

    cursor.execute("""

    DELETE FROM hotel_bookings
    WHERE booking_id = ?

    """, (booking_id,))

    conn.commit()

    return {
        "message":
        "Hotel Booking Cancelled"
    }