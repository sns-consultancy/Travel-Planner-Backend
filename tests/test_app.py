import pytest
from fastapi.testclient import TestClient

from backend.main import app, users_db, trips_db, leads_db


@pytest.fixture(autouse=True)
def clear_databases():
    users_db.clear()
    trips_db.clear()
    leads_db.clear()
    yield
    users_db.clear()
    trips_db.clear()
    leads_db.clear()


def register_user(client, username="alice", password="secret"):
    data = {
        "fullName": username,
        "dob": "1990-01-01",
        "country": "USA",
        "password": password,
        "confirmPassword": password,
    }
    response = client.post("/register", json=data)
    assert response.status_code == 200
    return username, password


def get_token(client, username, password):
    response = client.post(
        "/token",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_register_login_profile():
    client = TestClient(app)
    username, password = register_user(client)
    token = get_token(client, username, password)
    response = client.get("/profile", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert body["fullName"] == username


def test_trip_creation_and_listing():
    client = TestClient(app)
    username, password = register_user(client, username="bob")
    token = get_token(client, username, password)
    trip_data = {"destination": "Paris", "start_date": "2023-01-01", "days": 3}
    response = client.post(
        "/trip",
        json={"trip": trip_data},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    trip_id = response.json()["id"]

    response = client.get("/trips", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    trips = response.json()
    assert any(t["id"] == trip_id for t in trips)


def test_search_cars_with_current_location():
    client = TestClient(app)
    response = client.get(
        "/search/cars",
        params={
            "date": "2023-01-01",
            "use_current_location": True,
            "lat": 40.0,
            "lon": -74.0,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body[0]["location"] == "40.0,-74.0"
