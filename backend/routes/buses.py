from fastapi import APIRouter

from database import conn, cursor

import random

router = APIRouter()

# INSERT DEFAULT BUSES

cursor.execute("SELECT COUNT(*) FROM buses")

count = cursor.fetchone()[0]

if count == 0:

    buses = [

        (
            "RedBus Express",
            "Delhi",
            "Manali",
            "08:00 PM",
            "06:00 AM",
            "10h",
            18,
            1200
        ),

        (
            "Volvo Travels",
            "Delhi",
            "Jaipur",
            "07:00 AM",
            "01:00 PM",
            "6h",
            22,
            850
        ),

        (
            "Orange Tours",
            "Mumbai",
            "Pune",
            "09:00 AM",
            "01:00 PM",
            "4h",
            15,
            700
        ),
        (
            "MiniBus Express",
            "Delhi",
            "Mumbai",
            "08:00 PM",
            "10:00 AM",
            "14h",
            18,
            2500
        ),

        (
            "Lak Travels",
            "Delhi",
            "Lucknow",
            "07:00 AM",
            "07:00 PM",
            "12h",
            22,
            1250
        ),
        (
            "Orange Tours",
            "Mumbai",
            "Delhi",
            "09:00 AM",
            "12:00 Noon",
            "14h",
            15,
            3000
        )
    ]

    cursor.executemany("""

    INSERT INTO buses (

        operator,
        source,
        destination,
        departure,
        arrival,
        duration,
        seats,
        price

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, buses)

    conn.commit()

def generate_pnr():

    return "BUS" + str(
        random.randint(10000, 99999)
    )

def generate_booking_id():

    return "BUSBK" + str(
        random.randint(1000, 9999)
    )

@router.get("/buses")

def get_buses():

    cursor.execute(
        "SELECT * FROM buses"
    )

    buses = cursor.fetchall()

    return [dict(bus) for bus in buses]

@router.post("/book-bus")

def book_bus(data: dict):

    cursor.execute("""

    SELECT * FROM buses
    WHERE id = ?

    """, (data["bus_id"],))

    bus = cursor.fetchone()

    if not bus:

        return {
            "message":
            "Bus Not Found"
        }

    if bus["seats"] < data["passengers"]:

        return {
            "message":
            "Not Enough Seats Available"
        }

    updated_seats = (
        bus["seats"]
        - data["passengers"]
    )

    cursor.execute("""

    UPDATE buses
    SET seats = ?
    WHERE id = ?

    """, (
        updated_seats,
        data["bus_id"]
    ))

    pnr = generate_pnr()

    booking_id = generate_booking_id()

    cursor.execute("""

    INSERT INTO bus_bookings (

        user_id,
        user_name,
        bus_id,
        operator,
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
        data["bus_id"],
        data["operator"],
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
        "Bus Booked Successfully"
    }

@router.get("/bus-bookings")

def get_bus_bookings():

    cursor.execute(
        "SELECT * FROM bus_bookings"
    )

    bookings = cursor.fetchall()

    return [dict(b) for b in bookings]

@router.delete(
    "/cancel-bus/{booking_id}"
)

def cancel_bus_booking(
    booking_id: str
):

    cursor.execute("""

    SELECT * FROM bus_bookings
    WHERE booking_id = ?

    """, (booking_id,))

    booking = cursor.fetchone()

    if not booking:

        return {
            "message":
            "Booking Not Found"
        }

    cursor.execute("""

    SELECT * FROM buses
    WHERE id = ?

    """, (booking["bus_id"],))

    bus = cursor.fetchone()

    updated_seats = (
        bus["seats"]
        + booking["passengers"]
    )

    cursor.execute("""

    UPDATE buses
    SET seats = ?
    WHERE id = ?

    """, (
        updated_seats,
        booking["bus_id"]
    ))

    cursor.execute("""

    DELETE FROM bus_bookings
    WHERE booking_id = ?

    """, (booking_id,))

    conn.commit()

    return {
        "message":
        "Bus Booking Cancelled"
    }