import sqlite3

DATABASE_NAME = "mini_mmt.db"

def get_connection():

    conn = sqlite3.connect(
        DATABASE_NAME,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn

conn = get_connection()

cursor = conn.cursor()

# USERS TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    email TEXT UNIQUE,

    password TEXT

)

""")

# FLIGHTS TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS flights (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    airline TEXT,

    source TEXT,

    destination TEXT,

    departure TEXT,

    arrival TEXT,

    duration TEXT,

    seats INTEGER,

    price INTEGER

)

""")

# BUSES TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS buses (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    operator TEXT,

    source TEXT,

    destination TEXT,

    departure TEXT,

    arrival TEXT,

    duration TEXT,

    seats INTEGER,

    price INTEGER

)

""")

# BOOKINGS TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS bookings (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    user_name TEXT,

    flight_id INTEGER,

    airline TEXT,

    source TEXT,

    destination TEXT,

    departure TEXT,

    arrival TEXT,

    duration TEXT,

    passengers INTEGER,

    journey_date TEXT,

    price INTEGER,

    pnr TEXT,

    booking_id TEXT

)

""")

# BUS BOOKINGS TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS bus_bookings (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    user_name TEXT,

    bus_id INTEGER,

    operator TEXT,

    source TEXT,

    destination TEXT,

    departure TEXT,

    arrival TEXT,

    duration TEXT,

    passengers INTEGER,

    journey_date TEXT,

    price INTEGER,

    pnr TEXT,

    booking_id TEXT

)

""")

# TRAINS TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS trains (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    train_name TEXT,

    train_number TEXT,

    source TEXT,

    destination TEXT,

    departure TEXT,

    arrival TEXT,

    duration TEXT,

    seats INTEGER,

    price INTEGER

)

""")

# TRAIN BOOKINGS TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS train_bookings (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    user_name TEXT,

    train_id INTEGER,

    train_name TEXT,

    train_number TEXT,

    source TEXT,

    destination TEXT,

    departure TEXT,

    arrival TEXT,

    duration TEXT,

    passengers INTEGER,

    journey_date TEXT,

    price INTEGER,

    pnr TEXT,

    booking_id TEXT

)

""")

# HOTELS TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS hotels (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    hotel_name TEXT,

    city TEXT,

    room_type TEXT,

    rating REAL,

    rooms INTEGER,

    price INTEGER

)

""")

# HOTEL BOOKINGS TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS hotel_bookings (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    user_name TEXT,

    hotel_id INTEGER,

    hotel_name TEXT,

    city TEXT,

    room_type TEXT,

    rating REAL,

    rooms_booked INTEGER,

    stay_date TEXT,

    price INTEGER,

    pnr TEXT,

    booking_id TEXT

)

""")

conn.commit()