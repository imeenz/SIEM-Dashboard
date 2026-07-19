import pytest

pytestmark = pytest.mark.asyncio


async def create_alert_via_ingestion(client):
    response = await client.post(
        "/api/v1/ingestion/log",
        json={
            "raw_log": (
                "IDS ALERT SRC=203.0.113.150 DST=192.168.1.10 "
                "SIGNATURE=SQL_INJECTION SEVERITY=critical"
            )
        },
    )

    assert response.status_code == 201


async def test_get_alerts(client):
    await create_alert_via_ingestion(client)

    response = await client.get("/api/v1/alerts")

    assert response.status_code == 200

    alerts = response.json()

    assert len(alerts) == 1
    assert alerts[0]["status"] == "open"
    assert alerts[0]["severity"] == "critical"


async def test_get_alert_by_id(client):
    await create_alert_via_ingestion(client)

    alerts_response = await client.get("/api/v1/alerts")
    alert_id = alerts_response.json()[0]["id"]

    response = await client.get(f"/api/v1/alerts/{alert_id}")

    assert response.status_code == 200
    assert response.json()["id"] == alert_id


async def test_alert_not_found(client):
    response = await client.get("/api/v1/alerts/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Alert not found"


async def test_update_alert_status(client):
    await create_alert_via_ingestion(client)

    alerts_response = await client.get("/api/v1/alerts")
    alert_id = alerts_response.json()[0]["id"]

    response = await client.patch(
        f"/api/v1/alerts/{alert_id}/status",
        json={"status": "investigating"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "investigating"


async def test_resolve_alert(client):
    await create_alert_via_ingestion(client)

    alerts_response = await client.get("/api/v1/alerts")
    alert_id = alerts_response.json()[0]["id"]

    response = await client.patch(
        f"/api/v1/alerts/{alert_id}/status",
        json={"status": "resolved"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "resolved"


async def test_invalid_alert_status(client):
    await create_alert_via_ingestion(client)

    alerts_response = await client.get("/api/v1/alerts")
    alert_id = alerts_response.json()[0]["id"]

    response = await client.patch(
        f"/api/v1/alerts/{alert_id}/status",
        json={"status": "invalid"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid alert status"


async def test_new_alert_created_after_previous_alert_resolved(
    client,
):
    raw_log = (
        "IDS ALERT SRC=203.0.113.210 DST=192.168.1.10 "
        "SIGNATURE=SQL_INJECTION SEVERITY=critical"
    )

    first_response = await client.post(
        "/api/v1/ingestion/log",
        json={"raw_log": raw_log},
    )

    assert first_response.status_code == 201

    alerts_response = await client.get("/api/v1/alerts")
    alerts = alerts_response.json()

    assert len(alerts) == 1

    first_alert_id = alerts[0]["id"]

    resolve_response = await client.patch(
        f"/api/v1/alerts/{first_alert_id}/status",
        json={"status": "resolved"},
    )

    assert resolve_response.status_code == 200
    assert resolve_response.json()["status"] == "resolved"

    second_response = await client.post(
        "/api/v1/ingestion/log",
        json={"raw_log": raw_log},
    )

    assert second_response.status_code == 201

    alerts_response = await client.get("/api/v1/alerts")
    alerts = alerts_response.json()

    assert len(alerts) == 2

    statuses = [alert["status"] for alert in alerts]

    assert "resolved" in statuses
    assert "open" in statuses


async def test_filter_alerts_by_status(client):
    await create_alert_via_ingestion(client)

    response = await client.get("/api/v1/alerts?status=open")

    assert response.status_code == 200

    alerts = response.json()

    assert len(alerts) == 1
    assert alerts[0]["status"] == "open"


async def test_filter_alerts_by_severity(client):
    await create_alert_via_ingestion(client)

    response = await client.get("/api/v1/alerts?severity=critical")

    assert response.status_code == 200

    alerts = response.json()

    assert len(alerts) == 1
    assert alerts[0]["severity"] == "critical"


async def test_filter_alerts_by_status_and_severity(client):
    await create_alert_via_ingestion(client)

    response = await client.get("/api/v1/alerts?status=open&severity=critical")

    assert response.status_code == 200

    alerts = response.json()

    assert len(alerts) == 1
    assert alerts[0]["status"] == "open"
    assert alerts[0]["severity"] == "critical"
