from app.core.database import SessionLocal
from app.demo.runner import create_demo_producer


def main() -> None:
    db = SessionLocal()

    try:
        producer = create_demo_producer(
            db=db,
            interval_seconds=5.0,
        )

        print("SIEM demo generator started.")
        print("Generating a security log every 5 seconds.")
        print("Press Ctrl+C to stop.")

        producer.run()

    except KeyboardInterrupt:
        print("\nSIEM demo generator stopped.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
