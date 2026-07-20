import pytest

from app.demo.scenarios import get_scenario


def test_get_sql_injection_scenario():
    logs = get_scenario("sql_injection")

    assert len(logs) > 0
    assert "SQL_INJECTION" in logs[0]


def test_get_brute_force_scenario():
    logs = get_scenario("brute_force")

    assert len(logs) > 0


def test_unknown_scenario_raises_error():
    with pytest.raises(ValueError):
        get_scenario("unknown")
