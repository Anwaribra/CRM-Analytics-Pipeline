from faker import Faker
import json
from pathlib import Path
from datetime import datetime
import uuid

RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

fake = Faker()
Faker.seed(42)

def generate_contact():
    created = fake.date_time_this_year()
    modified = fake.date_time_between_dates(datetime_start=created)
    return {
        "id": str(uuid.uuid4()),
        "properties": {
            "createdate": created.isoformat(),
            "email": fake.email(),
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
            "hs_object_id": str(uuid.uuid4()),
            "lastmodifieddate": modified.isoformat()
        },
        "archived": False
    }

def generate_contacts(num_contacts=100_000):
    print(f"Generating {num_contacts} contacts...")
    contacts = [generate_contact() for _ in range(num_contacts)]
    return {"results": contacts}

def save_to_file(data):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_path = RAW_DATA_DIR / f"mock_contacts_{timestamp}.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    fake_data = generate_contacts()
    save_to_file(fake_data)
