import logging
import socket

from app.core.database import SessionLocal
from app.services.ingestion import IngestionService

logger = logging.getLogger(__name__)


class TCPSyslogReceiver:
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 5514,
    ) -> None:
        self.host = host
        self.port = port
        self.ingestion_service = IngestionService()

    def process_message(
        self,
        data: bytes,
        address: tuple[str, int],
    ) -> None:
        try:
            raw_log = data.decode("utf-8").strip()
        except UnicodeDecodeError:
            logger.warning(
                "Received invalid UTF-8 data from %s",
                address,
            )
            return

        if not raw_log:
            return

        db = SessionLocal()

        try:
            event = self.ingestion_service.ingest_log(
                db=db,
                raw_log=raw_log,
            )

            logger.info(
                "Ingested TCP event %s from %s",
                event.id,
                address,
            )

        except ValueError:
            logger.warning(
                "Unsupported TCP log from %s: %s",
                address,
                raw_log,
            )

        except Exception:
            logger.exception(
                "Failed to ingest TCP log from %s",
                address,
            )

        finally:
            db.close()

    def start(self) -> None:
        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

        server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )

        server_socket.bind((self.host, self.port))
        server_socket.listen()

        logger.info(
            "TCP Syslog receiver listening on %s:%s",
            self.host,
            self.port,
        )

        try:
            while True:
                connection, address = server_socket.accept()

                try:
                    data = connection.recv(65535)

                    if data:
                        self.process_message(
                            data=data,
                            address=address,
                        )

                finally:
                    connection.close()

        finally:
            server_socket.close()
