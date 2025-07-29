from typing import List
from pydantic import BaseModel

class Restaurant(BaseModel):
    name: str
    address: str
    cuisine: str
    rating: float


def search_restaurants(location: str) -> List[Restaurant]:
    """Placeholder restaurant search returning static data."""
    return [
        Restaurant(name="The Fancy Fork", address="789 Cuisine Rd", cuisine="French", rating=4.7),
        Restaurant(name="Pizza Planet", address="1010 Space St", cuisine="Italian", rating=4.2),
    ]
