from typing import List
from pydantic import BaseModel

class Hotel(BaseModel):
    name: str
    address: str
    price_per_night: float
    rating: float


def search_hotels(destination: str, check_in: str, nights: int) -> List[Hotel]:
    """Placeholder hotel search returning static data."""
    return [
        Hotel(
            name="Grand Example Hotel",
            address="123 Example St",
            price_per_night=150.0,
            rating=4.5,
        ),
        Hotel(
            name="Budget Inn",
            address="456 Sample Ave",
            price_per_night=80.0,
            rating=3.8,
        ),
    ]
