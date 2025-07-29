from typing import List
from pydantic import BaseModel

class CarRental(BaseModel):
    company: str
    model: str
    daily_rate: float


def search_car_rentals(location: str, start_date: str, days: int) -> List[CarRental]:
    """Placeholder car rental search returning static data."""
    return [
        CarRental(company="Acme Rentals", model="Economy", daily_rate=35.0),
        CarRental(company="City Cars", model="SUV", daily_rate=60.0),
    ]
