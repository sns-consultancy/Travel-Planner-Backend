from pydantic import BaseModel

class RideEstimate(BaseModel):
    service: str
    estimate_minutes: int
    estimate_cost: float


def get_ride_estimate(pickup: str, dropoff: str) -> RideEstimate:
    """Placeholder ride estimate returning static data."""
    return RideEstimate(service="RideShareX", estimate_minutes=15, estimate_cost=18.5)
