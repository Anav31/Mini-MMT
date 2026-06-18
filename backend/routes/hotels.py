from fastapi import APIRouter

from database import conn, cursor

from logger import logger
from config.bug_config import BUG_CONFIG
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
    logger.info(
        f"Hotels fetched | count={len(hotels)}"
    )

    return [
        dict(hotel)
        for hotel in hotels
    ]

# BOOK HOTEL

@router.post("/book-hotel")

def book_hotel(data: dict):

    logger.info(
        f"Hotel booking request received | "
        f"user={data.get('user_name')} | "
        f"hotel_id={data.get('hotel_id')} | "
        f"rooms_requested={data.get('rooms_booked')}"
    )

    if (
        not BUG_CONFIG["allow_negative_rooms"]
        and data["rooms_booked"] <= 0
    ):

        logger.warning(
            f"Hotel booking failed | "
            f"reason=Invalid Room Count | "
            f"requested={data['rooms_booked']}"
        )

        return {
            "message":
            "Rooms booked must be greater than 0"
        }

    cursor.execute("""

    SELECT * FROM hotels
    WHERE id = ?

    """, (data["hotel_id"],))

    hotel = cursor.fetchone()

    if not hotel:

        logger.warning(
            f"Hotel booking failed | "
            f"reason=Hotel Not Found | "
            f"hotel_id={data.get('hotel_id')}"
        )

        return {
            "message":
            "Hotel Not Found"
        }

    if hotel["rooms"] < data["rooms_booked"]:

        logger.warning(
            f"Hotel booking failed | "
            f"reason=Not Enough Rooms | "
            f"available={hotel['rooms']} | "
            f"requested={data['rooms_booked']}"
        )

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
    logger.info(
        f"Hotel booked successfully | "
        f"booking_id={booking_id} | "
        f"pnr={pnr} | "
        f"user={data['user_name']} | "
        f"remaining_rooms={updated_rooms}"
    )

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
    logger.info(
        f"Hotel bookings fetched | "
        f"count={len(bookings)}"
    )

    return [
        dict(b)
        for b in bookings
    ]

# CANCEL HOTEL BOOKING

@router.delete(
    "/cancel-hotel/{booking_id}"
)

def cancel_hotel_booking(booking_id: str):
    logger.info(
        f"Hotel cancellation request received | "
        f"booking_id={booking_id}"
    )

    cursor.execute("""

    SELECT * FROM hotel_bookings
    WHERE booking_id = ?

    """, (booking_id,))

    booking = cursor.fetchone()

    if not booking:

        logger.warning(
            f"Hotel cancellation failed | "
            f"reason=Booking Not Found | "
            f"booking_id={booking_id}"
        )

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

    logger.info(
        f"Hotel booking cancelled | "
        f"booking_id={booking_id} | "
        f"restored_rooms={booking['rooms_booked']}"
    )

    return {
        "message":
        "Hotel Booking Cancelled"
    }