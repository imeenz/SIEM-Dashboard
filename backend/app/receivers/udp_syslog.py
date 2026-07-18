import logging
import socket

from app.core.database import SessionLocal
from app.services.ingestion import IngestionService

logger = logging.getLogger(__name__)


class UDPSyslogReceiver:
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
                "Ingested UDP event %s from %s",
                event.id,
                address,
            )

        except ValueError:
            logger.warning(
                "Unsupported UDP log from %s: %s",
                address,
                raw_log,
            )

        except Exception:
            logger.exception(
                "Failed to ingest UDP log from %s",
                address,
            )

        finally:
            db.close()

    def start(self) -> None:
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
        )

        sock.bind((self.host, self.port))

        logger.info(
            "UDP Syslog receiver listening on %s:%s",
            self.host,
            self.port,
        )

        try:
            while True:
                data, address = sock.recvfrom(65535)

                self.process_message(
                    data=data,
                    address=address,
                )

        finally:
            sock.close()
