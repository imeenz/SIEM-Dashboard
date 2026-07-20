from app.demo.log_generator import DEMO_LOGS, generate_log


def test_generate_log_returns_string():
    log = generate_log()

    assert isinstance(log, str)
    assert len(log) > 0


def test_generate_log_returns_known_demo_log():
    log = generate_log()

    assert log in DEMO_LOGS
