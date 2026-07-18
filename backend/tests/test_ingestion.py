import pytest

pytestmark = pytest.mark.asyncio


async def test_ingest_ssh_log(client):
    raw_log = (
        "Jul 19 02:15:43 server01 sshd[1842]: "
        "Failed password for admin from 192.168.1.25 port 54321 ssh2"
    )

    response = await client.post(
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


async def test_ingested_log_appears_in_events(client):
    raw_log = (
        "Jul 19 02:15:43 server01 sshd[1842]: "
        "Failed password for admin from 10.0.0.50 port 54321 ssh2"
    )

    create_response = await client.post(
        "/api/v1/ingestion/log",
        json={"raw_log": raw_log},
    )

    assert create_response.status_code == 201

    response = await client.get("/api/v1/events")

    assert response.status_code == 200

    events = response.json()

    assert len(events) == 1
    assert events[0]["source_ip"] == "10.0.0.50"


async def test_ingest_unknown_log_returns_422(client):
    response = await client.post(
        "/api/v1/ingestion/log",
        json={"raw_log": "Unknown application message"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == (
        "No suitable parser found for the provided log"
    )


async def test_ingest_log_file(client):
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

    response = await client.post(
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


async def test_file_ingestion_stores_events(client):
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

    upload_response = await client.post(
        "/api/v1/ingestion/file",
        files=files,
    )

    assert upload_response.status_code == 201

    response = await client.get("/api/v1/events")

    assert response.status_code == 200

    events = response.json()

    assert len(events) == 2

    sources = {event["source"] for event in events}

    assert "ssh" in sources
    assert "firewall" in sources


async def test_ingest_non_utf8_file_returns_400(client):
    files = {
        "file": (
            "invalid.log",
            b"\xff\xfe\xfa\xfb",
            "application/octet-stream",
        )
    }

    response = await client.post(
        "/api/v1/ingestion/file",
        files=files,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "File must be UTF-8 encoded"
