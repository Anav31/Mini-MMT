from fastapi import APIRouter

from database import conn, cursor
from logger import logger

router = APIRouter()

# INSERT DEFAULT FLIGHTS ONLY ONCE

cursor.execute("SELECT COUNT(*) FROM flights")

count = cursor.fetchone()[0]

if count == 0:

    flights = [

        ("IndiGo", "Delhi", "Mumbai", "08:00", "10:00", "2h", 40, 5000),

        ("Air India", "Delhi", "Mumbai", "12:00", "14:00", "2h", 35, 6200),

        ("SpiceJet", "Delhi", "Mumbai", "18:00", "20:15", "2h 15m", 20, 4800),

        ("Vistara", "Delhi", "Goa", "09:00", "11:30", "2h 30m", 25, 7200),

        ("Akasa Air", "Mumbai", "Bangalore", "07:00", "09:00", "2h", 30, 5400),

        ("AirAsia", "Bangalore", "Goa", "13:00", "14:30", "1h 30m", 28, 4500)

    ]

    cursor.executemany("""

    INSERT INTO flights (
        airline,
        source,
        destination,
        departure,
        arrival,
        duration,
        seats,
        price
    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, flights)

    conn.commit()

@router.get("/flights")

def get_flights():

    logger.info("Flights fetched")

    cursor.execute("SELECT * FROM flights")

    flights = cursor.fetchall()

    return [dict(flight) for flight in flights]