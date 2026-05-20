from fastapi import APIRouter
from database import SessionLocal
from models import User

router = APIRouter()

@router.post("/register")
@router.post("/register")
def register(name: str, email: str, password: str):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:

        return {
            "message": "Email already registered"
        }

    user = User(
        name=name,
        email=email,
        password=password
    )

    db.add(user)
    db.commit()

    return {
        "message": "User Registered Successfully"
    }

@router.post("/login")
def login(email: str, password: str):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email,
        User.password == password
    ).first()

    if user:

        return {
            "message": "Login Successful",
            "user_id": user.id,
            "name": user.name
        }

    return {
        "message": "Invalid Email or Password"
    }