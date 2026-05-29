from fastapi import FastAPI
from routes.hotels import router as hotels_router

from fastapi.middleware.cors import CORSMiddleware

from routes.flights import router as flights_router
from routes.trains import router as trains_router
from routes.bookings import router as bookings_router
from routes.buses import router as buses_router

app = FastAPI()

# CORS
app.add_middleware(CORSMiddleware,allow_origins=["*"], allow_credentials=True,allow_methods=["*"],
                   allow_headers=["*"],)

# ROUTES

app.include_router(flights_router)

app.include_router(bookings_router)

app.include_router(hotels_router)

app.include_router(buses_router)

app.include_router(trains_router)

@app.get("/")

def home():

    return {"message":"Mini MMT Backend Running"}