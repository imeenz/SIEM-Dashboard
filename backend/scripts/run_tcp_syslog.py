from app.core.logging import configure_logging
from app.receivers.tcp_syslog import TCPSyslogReceiver


def main() -> None:
    configure_logging()

    receiver = TCPSyslogReceiver(
        host="0.0.0.0",
        port=5514,
    )

    receiver.start()


if __name__ == "__main__":
    main()
