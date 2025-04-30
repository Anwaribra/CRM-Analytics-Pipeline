import json
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
conn = psycopg2.connect(
    host=os.getenv("PG_HOST", "localhost"),
    dbname=os.getenv("PG_DB", "crm_db"),
    user=os.getenv("PG_USER", "postgres"),
    password=os.getenv("PG_PASSWORD", "postgres"),
    port=os.getenv("PG_PORT", "5432")
)
cursor = conn.cursor()

RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
latest_file = sorted(RAW_DATA_DIR.glob("mock_contacts_*.json"))[-1]

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id UUID PRIMARY KEY,
    createdate TIMESTAMP,
    email TEXT,
    firstname TEXT,
    lastname TEXT,
    hs_object_id UUID,
    lastmodifieddate TIMESTAMP,
    archived BOOLEAN
);
""")

with open(latest_file, "r") as f:
    data = json.load(f)["results"]

for contact in data:
    p = contact["properties"]
    cursor.execute("""
        INSERT INTO contacts (id, createdate, email, firstname, lastname, hs_object_id, lastmodifieddate, archived)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """, (
        contact["id"],
        p.get("createdate"),
        p.get("email"),
        p.get("firstname"),
        p.get("lastname"),
        p.get("hs_object_id"),
        p.get("lastmodifieddate"),
        contact["archived"]
    ))

conn.commit()
cursor.close()
conn.close()
print(f"Loaded {len(data)} contacts into PostgreSQL!")
