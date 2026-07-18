from app.core.logging import configure_logging
from app.receivers.udp_syslog import UDPSyslogReceiver


def main() -> None:
    configure_logging()

    receiver = UDPSyslogReceiver(
        host="0.0.0.0",
        port=5514,
    )

    receiver.start()


if __name__ == "__main__":
    main()
