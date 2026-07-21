import pytest

pytestmark = pytest.mark.asyncio


async def test_ingest_ssh_log(authenticated_client):
    raw_log = (
        "Jul 19 02:15:43 server01 sshd[1842]: "
        "Failed password for admin from 192.168.1.25 port 54321 ssh2"
    )

    response = await authenticated_client.post(
        "/api/v1/ingestion/log",
        json={"raw_log": raw_log},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["source"] == "ssh"
    assert data["event_type"] == "failed_login"
    assert data["severity"] == "high"
    assert data["source_ip"] == "192.168.1.25"
    assert data["raw_log"] == raw_log
    assert data["id"] is not None


async def test_ingested_log_appears_in_events(authenticated_client):
    raw_log = (
        "Jul 19 02:15:43 server01 sshd[1842]: "
        "Failed password for admin from 10.0.0.50 port 54321 ssh2"
    )

    create_response = await authenticated_client.post(
        "/api/v1/ingestion/log",
        json={"raw_log": raw_log},
    )

    assert create_response.status_code == 201

    response = await authenticated_client.get("/api/v1/events")

    assert response.status_code == 200

    events = response.json()

    assert len(events) == 1
    assert events[0]["source_ip"] == "10.0.0.50"


async def test_ingest_unknown_log_returns_422(authenticated_client):
    response = await authenticated_client.post(
        "/api/v1/ingestion/log",
        json={"raw_log": "Unknown application message"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == (
        "No suitable parser found for the provided log"
    )


async def test_ingest_log_file(authenticated_client):
    file_content = (
        "Jul 19 02:15:43 server01 sshd[1842]: "
        "Failed password for admin from 192.168.1.25 port 54321 ssh2\n"
        "Jul 19 03:20:15 firewall01 kernel: "
        "FIREWALL BLOCK SRC=203.0.113.50 DST=192.168.1.10 "
        "PROTO=TCP SPT=45678 DPT=22\n"
        "Unknown application message\n"
    )

    files = {
        "file": (
            "test_security.log",
            file_content,
            "text/plain",
        )
    }

    response = await authenticated_client.post(
        "/api/v1/ingestion/file",
        files=files,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["filename"] == "test_security.log"
    assert data["processed"] == 3
    assert data["ingested"] == 2
    assert data["failed"] == 1
    assert data["failed_logs"] == ["Unknown application message"]


async def test_file_ingestion_stores_events(authenticated_client):
    file_content = (
        "Jul 19 02:15:43 server01 sshd[1842]: "
        "Failed password for admin from 192.168.1.25 port 54321 ssh2\n"
        "Jul 19 03:20:15 firewall01 kernel: "
        "FIREWALL BLOCK SRC=203.0.113.50 DST=192.168.1.10 "
        "PROTO=TCP SPT=45678 DPT=22\n"
    )

    files = {
        "file": (
            "test_security.log",
            file_content,
            "text/plain",
        )
    }

    upload_response = await authenticated_client.post(
        "/api/v1/ingestion/file",
        files=files,
    )

    assert upload_response.status_code == 201

    response = await authenticated_client.get("/api/v1/events")

    assert response.status_code == 200

    events = response.json()

    assert len(events) == 2

    sources = {event["source"] for event in events}

    assert "ssh" in sources
    assert "firewall" in sources


async def test_ingest_non_utf8_file_returns_400(authenticated_client):
    files = {
        "file": (
            "invalid.log",
            b"\xff\xfe\xfa\xfb",
            "application/octet-stream",
        )
    }

    response = await authenticated_client.post(
        "/api/v1/ingestion/file",
        files=files,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "File must be UTF-8 encoded"


async def test_critical_ids_ingestion_creates_detection(
    authenticated_client,
    db_session,
):
    raw_log = (
        "IDS ALERT SRC=203.0.113.100 DST=192.168.1.10 "
        "SIGNATURE=SQL_INJECTION SEVERITY=critical"
    )

    response = await authenticated_client.post(
        "/api/v1/ingestion/log",
        json={"raw_log": raw_log},
    )

    assert response.status_code == 201

    from app.models.detection import Detection

    detection = db_session.query(Detection).first()

    assert detection is not None
    assert detection.rule_name == "critical_ids_alert"
    assert detection.severity == "critical"
    assert detection.event_id == response.json()["id"]


async def test_port_scan_ingestion_creates_detection(
    authenticated_client,
    db_session,
):
    raw_log = (
        "IDS ALERT SRC=10.0.0.50 DST=192.168.1.20 "
        "SIGNATURE=PORT_SCAN SEVERITY=high"
    )

    response = await authenticated_client.post(
        "/api/v1/ingestion/log",
        json={"raw_log": raw_log},
    )

    assert response.status_code == 201

    from app.models.detection import Detection

    detection = (
        db_session.query(Detection)
        .filter(Detection.rule_name == "port_scan_detected")
        .first()
    )

    assert detection is not None
    assert detection.rule_name == "port_scan_detected"
    assert detection.severity == "high"
    assert detection.event_id == response.json()["id"]


async def test_repeated_firewall_blocks_create_detection(
    authenticated_client,
    db_session,
):
    source_ip = "203.0.113.200"

    for source_port in range(50001, 50006):
        raw_log = (
            "Jul 19 08:00:00 firewall01 kernel: "
            f"FIREWALL BLOCK SRC={source_ip} DST=192.168.1.10 "
            f"PROTO=TCP SPT={source_port} DPT=22"
        )

        response = await authenticated_client.post(
            "/api/v1/ingestion/log",
            json={"raw_log": raw_log},
        )

        assert response.status_code == 201

    from app.models.detection import Detection

    detection = (
        db_session.query(Detection)
        .filter(
            Detection.rule_name == "suspicious_firewall_activity"
        )
        .first()
    )

    assert detection is not None
    assert detection.rule_name == "suspicious_firewall_activity"
    assert detection.severity == "high"


async def test_critical_ids_ingestion_creates_alert(
    authenticated_client,
    db_session,
):
    raw_log = (
        "IDS ALERT SRC=203.0.113.150 DST=192.168.1.10 "
        "SIGNATURE=SQL_INJECTION SEVERITY=critical"
    )

    response = await authenticated_client.post(
        "/api/v1/ingestion/log",
        json={"raw_log": raw_log},
    )

    assert response.status_code == 201

    from app.models.alert import Alert
    from app.models.detection import Detection

    detection = (
        db_session.query(Detection)
        .filter(Detection.rule_name == "critical_ids_alert")
        .first()
    )

    assert detection is not None

    alert = (
        db_session.query(Alert)
        .filter(Alert.detection_id == detection.id)
        .first()
    )

    assert alert is not None
    assert alert.title == "Critical IDS alert detected"
    assert alert.severity == "critical"
    assert alert.status == "open"
    assert alert.detection_id == detection.id


async def test_duplicate_detections_create_single_active_alert(
    authenticated_client,
    db_session,
):
    from app.models.alert import Alert
    from app.models.detection import Detection

    raw_logs = [
        (
            "IDS ALERT SRC=203.0.113.201 DST=192.168.1.10 "
            "SIGNATURE=SQL_INJECTION SEVERITY=critical"
        ),
        (
            "IDS ALERT SRC=203.0.113.201 DST=192.168.1.10 "
            "SIGNATURE=SQL_INJECTION SEVERITY=critical"
        ),
    ]

    for raw_log in raw_logs:
        response = await authenticated_client.post(
            "/api/v1/ingestion/log",
            json={"raw_log": raw_log},
        )

        assert response.status_code == 201

    detections = (
        db_session.query(Detection)
        .filter(Detection.rule_name == "critical_ids_alert")
        .all()
    )

    alerts = db_session.query(Alert).all()

    assert len(detections) == 2
    assert len(alerts) == 1
    assert alerts[0].status == "open"


async def test_same_rule_different_sources_create_separate_alerts(
    authenticated_client,
    db_session,
):
    from app.models.alert import Alert

    raw_logs = [
        (
            "IDS ALERT SRC=203.0.113.201 DST=192.168.1.10 "
            "SIGNATURE=SQL_INJECTION SEVERITY=critical"
        ),
        (
            "IDS ALERT SRC=203.0.113.202 DST=192.168.1.10 "
            "SIGNATURE=SQL_INJECTION SEVERITY=critical"
        ),
    ]

    for raw_log in raw_logs:
        response = await authenticated_client.post(
            "/api/v1/ingestion/log",
            json={"raw_log": raw_log},
        )

        assert response.status_code == 201

    alerts = db_session.query(Alert).all()

    assert len(alerts) == 2