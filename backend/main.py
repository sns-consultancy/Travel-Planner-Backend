from datetime import datetime, timedelta
from typing import Dict, Optional, List

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Destination(BaseModel):
    destination: str

class User(BaseModel):
    fullName: str
    dob: str
    email: Optional[str]
    mobile: Optional[str]
    country: str
    hashed_password: str

class UserOut(BaseModel):
    fullName: str
    dob: str
    email: Optional[str]
    mobile: Optional[str]
    country: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TripCreate(BaseModel):
    destination: str
    start_date: str
    days: int


class Trip(BaseModel):
    id: str
    destination: str
    start_date: str
    days: int
    plan: str
    owner: str

users_db: Dict[str, User] = {}
trips_db: Dict[str, Trip] = {}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> Optional[User]:
    user = users_db.get(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = users_db.get(username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/plan")
async def generate_plan(data: Destination):
    return {"plan": f"Here is your custom travel itinerary for {data.destination}."}


@app.post("/register")
async def register_user(
    fullName: str = Form(...),
    dob: str = Form(...),
    email: str = Form(None),
    mobile: str = Form(None),
    country: str = Form(...),
    password: str = Form(...),
    confirmPassword: str = Form(...),
    profilePhoto: Optional[UploadFile] = File(None),
    consentGmail: Optional[bool] = Form(False),
    consentPhone: Optional[bool] = Form(False),
):
    if password != confirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if fullName in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = get_password_hash(password)
    users_db[fullName] = User(
        fullName=fullName,
        dob=dob,
        email=email,
        mobile=mobile,
        country=country,
        hashed_password=hashed_password,
    )
    return {"message": f"User {fullName} registered successfully."}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.fullName})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return UserOut(
        fullName=current_user.fullName,
        dob=current_user.dob,
        email=current_user.email,
        mobile=current_user.mobile,
        country=current_user.country,
    )


def generate_trip_plan(destination: str, start_date: str, days: int) -> str:
    return (
        f"Trip to {destination} starting {start_date} for {days} days."
        f" Enjoy sightseeing and local cuisine!"
    )


@app.post("/trip", response_model=Trip)
async def create_trip(
    trip: TripCreate, current_user: User = Depends(get_current_user)
):
    trip_id = str(uuid4())
    plan = generate_trip_plan(trip.destination, trip.start_date, trip.days)
    new_trip = Trip(
        id=trip_id,
        destination=trip.destination,
        start_date=trip.start_date,
        days=trip.days,
        plan=plan,
        owner=current_user.fullName,
    )
    trips_db[trip_id] = new_trip
    return new_trip


@app.get("/trips", response_model=List[Trip])
async def list_trips(current_user: User = Depends(get_current_user)):
    return [t for t in trips_db.values() if t.owner == current_user.fullName]


@app.get("/trip/{trip_id}", response_model=Trip)
async def get_trip(trip_id: str, current_user: User = Depends(get_current_user)):
    trip = trips_db.get(trip_id)
    if not trip or trip.owner != current_user.fullName:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip
