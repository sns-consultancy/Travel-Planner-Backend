from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Destination(BaseModel):
    destination: str

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
    consentPhone: Optional[bool] = Form(False)
):
    return {"message": f"User {fullName} registered successfully."}

@app.post("/login")
async def login_user(username: str = Form(...), password: str = Form(...)):
    return {"user": {"id": "user123", "firstName": username, "email": f"{username}@example.com"}}
