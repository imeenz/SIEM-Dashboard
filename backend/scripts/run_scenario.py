import argparse

from app.core.database import SessionLocal
from app.demo.scenarios import SCENARIOS, get_scenario
from app.services.ingestion import IngestionService


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a SIEM demo attack scenario.")

    parser.add_argument(
        "scenario",
        choices=SCENARIOS.keys(),
        help="Demo scenario to execute.",
    )

    args = parser.parse_args()

    db = SessionLocal()
    ingestion_service = IngestionService()

    try:
        logs = get_scenario(args.scenario)

        print(f"Running demo scenario: {args.scenario}")

        for raw_log in logs:
            ingestion_service.ingest_log(
                db=db,
                raw_log=raw_log,
            )

            print(f"Ingested: {raw_log}")

        print("Scenario completed successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
