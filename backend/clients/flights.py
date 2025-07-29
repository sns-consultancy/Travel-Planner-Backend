from typing import List
from pydantic import BaseModel

class Flight(BaseModel):
    flight_number: str
    airline: str
    departure: str
    arrival: str
    price: float


def search_flights(origin: str, destination: str, date: str) -> List[Flight]:
    """Placeholder flight search returning static data."""
    return [
        Flight(
            flight_number="AB123",
            airline="Acme Air",
            departure=f"{date}T08:00",
            arrival=f"{date}T12:00",
            price=199.99,
        ),
        Flight(
            flight_number="CD456",
            airline="Example Airlines",
            departure=f"{date}T14:00",
            arrival=f"{date}T18:00",
            price=249.99,
        ),
    ]
