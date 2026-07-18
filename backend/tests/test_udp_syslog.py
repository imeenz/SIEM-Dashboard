from unittest.mock import MagicMock

from app.receivers.udp_syslog import UDPSyslogReceiver


def test_process_valid_udp_message():
    receiver = UDPSyslogReceiver()

    receiver.ingestion_service = MagicMock()

    mock_event = MagicMock()
    mock_event.id = 1

    receiver.ingestion_service.ingest_log.return_value = mock_event

    raw_log = "Jul 19 06:30:15 server03 nginx: " "Suspicious request detected"

    receiver.process_message(
        data=raw_log.encode("utf-8"),
        address=("127.0.0.1", 50000),
    )

    receiver.ingestion_service.ingest_log.assert_called_once()

    call_args = receiver.ingestion_service.ingest_log.call_args

    assert call_args.kwargs["raw_log"] == raw_log


def test_process_unsupported_udp_message():
    receiver = UDPSyslogReceiver()

    receiver.ingestion_service = MagicMock()
    receiver.ingestion_service.ingest_log.side_effect = ValueError(
        "No suitable parser found"
    )

    receiver.process_message(
        data=b"Unsupported random message",
        address=("127.0.0.1", 50000),
    )

    receiver.ingestion_service.ingest_log.assert_called_once()


def test_process_invalid_utf8_udp_message():
    receiver = UDPSyslogReceiver()

    receiver.ingestion_service = MagicMock()

    receiver.process_message(
        data=b"\xff\xfe\xfa\xfb",
        address=("127.0.0.1", 50000),
    )

    receiver.ingestion_service.ingest_log.assert_not_called()


def test_process_empty_udp_message():
    receiver = UDPSyslogReceiver()

    receiver.ingestion_service = MagicMock()

    receiver.process_message(
        data=b"   ",
        address=("127.0.0.1", 50000),
    )

    receiver.ingestion_service.ingest_log.assert_not_called()
