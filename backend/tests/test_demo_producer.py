from app.demo.producer import DemoLogProducer


def test_produce_once_sends_generated_log_to_handler():
    received_logs = []

    def handler(log: str) -> None:
        received_logs.append(log)

    producer = DemoLogProducer(
        handler=handler,
        interval_seconds=0,
    )

    produced_log = producer.produce_once()

    assert len(received_logs) == 1
    assert received_logs[0] == produced_log
