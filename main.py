
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DestinationRequest(BaseModel):
    destination: str

@app.post("/plan")
async def generate_plan(req: DestinationRequest):
    destination = req.destination
    return {"plan": f"Here is your travel plan for {destination}: Stay 3 days, visit landmarks, enjoy local food."}
