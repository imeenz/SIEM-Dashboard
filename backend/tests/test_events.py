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


def test_create_event(client):
    response = client.post("/api/v1/events", json=sample_event())

    assert response.status_code == 201

    data = response.json()

    assert data["source"] == "Windows Server"
    assert data["severity"] == "high"
    assert data["id"] is not None


def test_get_events(client):
    client.post("/api/v1/events", json=sample_event())

    response = client.get("/api/v1/events")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_event_by_id(client):
    create_response = client.post(
        "/api/v1/events",
        json=sample_event(),
    )

    event_id = create_response.json()["id"]

    response = client.get(f"/api/v1/events/{event_id}")

    assert response.status_code == 200
    assert response.json()["id"] == event_id


def test_event_not_found(client):
    response = client.get("/api/v1/events/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


def test_invalid_severity(client):
    event = sample_event()
    event["severity"] = "banana"

    response = client.post("/api/v1/events", json=event)

    assert response.status_code == 422


def test_invalid_ip(client):
    event = sample_event()
    event["source_ip"] = "999.999.999.999"

    response = client.post("/api/v1/events", json=event)

    assert response.status_code == 422


def test_event_pagination(client):
    client.post("/api/v1/events", json=sample_event())
    client.post("/api/v1/events", json=sample_event())

    response = client.get("/api/v1/events?skip=0&limit=1")

    assert response.status_code == 200
    assert len(response.json()) == 1
