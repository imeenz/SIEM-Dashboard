import pytest

pytestmark = pytest.mark.asyncio


def sample_event():
    return {
        "source": "Windows Server",
        "event_type": "Failed Login",
        "severity": "high",
        "source_ip": "192.168.1.25",
        "destination_ip": "192.168.1.10",
        "message": "Multiple failed login attempts detected",
        "raw_log": "Failed password for admin from 192.168.1.25",
    }


async def test_create_event(client):
    response = await client.post("/api/v1/events", json=sample_event())

    assert response.status_code == 201

    data = response.json()

    assert data["source"] == "Windows Server"
    assert data["severity"] == "high"
    assert data["id"] is not None


async def test_get_events(client):
    await client.post("/api/v1/events", json=sample_event())

    response = await client.get("/api/v1/events")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_event_by_id(client):
    create_response = await client.post(
        "/api/v1/events",
        json=sample_event(),
    )

    event_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/events/{event_id}")

    assert response.status_code == 200
    assert response.json()["id"] == event_id


async def test_event_not_found(client):
    response = await client.get("/api/v1/events/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


async def test_invalid_severity(client):
    event = sample_event()
    event["severity"] = "banana"

    response = await client.post("/api/v1/events", json=event)

    assert response.status_code == 422


async def test_invalid_ip(client):
    event = sample_event()
    event["source_ip"] = "999.999.999.999"

    response = await client.post("/api/v1/events", json=event)

    assert response.status_code == 422


async def test_event_pagination(client):
    await client.post("/api/v1/events", json=sample_event())
    await client.post("/api/v1/events", json=sample_event())

    response = await client.get("/api/v1/events?skip=0&limit=1")

    assert response.status_code == 200
    assert len(response.json()) == 1
