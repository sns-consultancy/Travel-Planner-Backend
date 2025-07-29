import os


class Settings:
    """Application settings loaded from environment variables."""

    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS", "")
    STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "")
    FLIGHT_API_KEY = os.getenv("FLIGHT_API_KEY", "")
    HOTEL_API_KEY = os.getenv("HOTEL_API_KEY", "")
    CAR_API_KEY = os.getenv("CAR_API_KEY", "")
    RESTAURANT_API_KEY = os.getenv("RESTAURANT_API_KEY", "")
    RIDE_API_KEY = os.getenv("RIDE_API_KEY", "")


settings = Settings()
