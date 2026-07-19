import pytest

pytestmark = pytest.mark.asyncio


async def test_get_detections(client):
    response = await client.get("/api/v1/detections")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_detection_by_id(client):
    ingest_response = await client.post(
        "/api/v1/ingestion/log",
        json={
            "raw_log": (
                "IDS ALERT SRC=203.0.113.100 DST=192.168.1.10 "
                "SIGNATURE=SQL_INJECTION SEVERITY=critical"
            )
        },
    )

    assert ingest_response.status_code == 201

    detections_response = await client.get("/api/v1/detections")

    assert detections_response.status_code == 200

    detections = detections_response.json()

    assert len(detections) >= 1

    detection_id = detections[0]["id"]

    response = await client.get(f"/api/v1/detections/{detection_id}")

    assert response.status_code == 200

    detection = response.json()

    assert detection["id"] == detection_id
    assert detection["rule_name"] == "critical_ids_alert"
    assert detection["severity"] == "critical"


async def test_detection_not_found(client):
    response = await client.get("/api/v1/detections/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Detection not found"


async def test_detection_pagination(client):
    response = await client.get("/api/v1/detections?skip=0&limit=10")

    assert response.status_code == 200
    assert len(response.json()) <= 10
