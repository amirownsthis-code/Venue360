"""Create fictional local demo data for a fresh Venue360 checkout.

Existing runtime files are never overwritten. Run after installing requirements.
"""

import json
from pathlib import Path

from werkzeug.security import generate_password_hash


def main():
    data_dir = Path(__file__).resolve().parent / "data"
    filenames = (
        "admins.json",
        "students.json",
        "events.json",
        "registrations.json",
    )

    existing = [name for name in filenames if (data_dir / name).exists()]
    if existing:
        print("Demo setup skipped: runtime data already exists.")
        print("Existing files were preserved: " + ", ".join(existing))
        print("Use this script in a fresh checkout to create demo accounts.")
        return 0

    fixtures = {
        "admins.json": [
            {
                "admin_id": "admin@uet.com",
                "name": "Demo Administrator",
                "password": generate_password_hash("admin123"),
            }
        ],
        "students.json": [
            {
                "id": 1,
                "username": "Demo Student",
                "email": "student@uet.com",
                "password": generate_password_hash("student123"),
                "phone": "",
                "department": "Demo Department",
                "year": "Demo",
                "student_id": "DEMO-001",
            }
        ],
        "events.json": [],
        "registrations.json": [],
    }

    data_dir.mkdir(parents=True, exist_ok=True)
    for filename, records in fixtures.items():
        # Exclusive creation prevents replacing a file created after the check.
        with (data_dir / filename).open("x", encoding="utf-8") as handle:
            json.dump(records, handle, indent=4, ensure_ascii=False)

    print("Fictional demo data created. Events and registrations start empty.")
    print("Student login: student@uet.com / student123")
    print("Admin login: admin@uet.com / admin123")
    print("These public demo credentials are for local development only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

