import time
from collections.abc import Callable

from app.demo.log_generator import generate_log


class DemoLogProducer:
    def __init__(
        self,
        handler: Callable[[str], None],
        interval_seconds: float = 5.0,
    ):
        self.handler = handler
        self.interval_seconds = interval_seconds

    def produce_once(self) -> str:
        log = generate_log()
        self.handler(log)

        return log

    def run(self) -> None:
        while True:
            self.produce_once()
            time.sleep(self.interval_seconds)
