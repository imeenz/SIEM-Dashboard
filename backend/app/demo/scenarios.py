SCENARIOS = {
    "sql_injection": [
        (
            "IDS ALERT SRC=203.0.113.201 DST=192.168.1.10 "
            "SIGNATURE=SQL_INJECTION SEVERITY=critical"
        ),
    ],
    "brute_force": [
        "Failed password for admin from 198.51.100.25",
        "Failed password for invalid user root from 198.51.100.25",
        (
            "IDS ALERT SRC=198.51.100.25 DST=192.168.1.15 "
            "SIGNATURE=BRUTE_FORCE SEVERITY=high"
        ),
    ],
    "suspicious_firewall": [
        (
            "FIREWALL BLOCK SRC=203.0.113.50 DST=192.168.1.20 "
            "PROTO=TCP SPT=45123 DPT=22"
        ),
        (
            "FIREWALL BLOCK SRC=203.0.113.50 DST=192.168.1.20 "
            "PROTO=TCP SPT=45124 DPT=443"
        ),
    ],
}


def get_scenario(name: str) -> list[str]:
    """Return the logs belonging to a named demo scenario."""
    if name not in SCENARIOS:
        raise ValueError(f"Unknown demo scenario: {name}")

    return SCENARIOS[name]
