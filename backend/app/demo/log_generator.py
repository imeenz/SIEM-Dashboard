import random

NORMAL_LOGS = [
    ("FIREWALL ALLOW SRC=192.168.1.25 DST=192.168.1.10 " "PROTO=TCP SPT=52341 DPT=443"),
    ("FIREWALL ALLOW SRC=192.168.1.30 DST=192.168.1.15 " "PROTO=TCP SPT=49152 DPT=80"),
    "Jul 21 09:15:32 webserver nginx[1234]: Connection established",
    "Jul 21 09:16:45 database postgres[2456]: Database service started",
    "Jul 21 09:17:20 server01 cron[987]: Scheduled task completed",
]

SUSPICIOUS_LOGS = [
    ("FIREWALL BLOCK SRC=203.0.113.50 DST=192.168.1.20 " "PROTO=TCP SPT=45123 DPT=22"),
    "Failed password for admin from 198.51.100.25",
    "Failed password for invalid user root from 203.0.113.75",
]

ATTACK_LOGS = [
    (
        "IDS ALERT SRC=203.0.113.201 DST=192.168.1.10 "
        "SIGNATURE=SQL_INJECTION SEVERITY=critical"
    ),
    (
        "IDS ALERT SRC=198.51.100.42 DST=192.168.1.15 "
        "SIGNATURE=BRUTE_FORCE SEVERITY=high"
    ),
]

DEMO_LOGS = NORMAL_LOGS + SUSPICIOUS_LOGS + ATTACK_LOGS


def generate_log() -> str:
    """Generate realistic weighted SIEM demo traffic."""
    category = random.choices(
        population=[
            NORMAL_LOGS,
            SUSPICIOUS_LOGS,
            ATTACK_LOGS,
        ],
        weights=[
            60,
            25,
            15,
        ],
        k=1,
    )[0]

    return random.choice(category)
