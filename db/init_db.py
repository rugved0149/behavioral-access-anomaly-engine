from pathlib import Path
from database import get_connection

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())

    # Ensure baseline row exists
    cursor.execute("SELECT COUNT(*) FROM baseline_profile")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO baseline_profile (
                id,
                mean_access_hour,
                std_access_hour,
                avg_events_per_hour,
                burst_threshold,
                known_countries,
                known_asns,
                known_clients,
                known_devices,
                identity_risk,
                last_updated
            ) VALUES (
                1,
                0.0,
                1.0,
                0.0,
                10.0,
                '[]',
                '[]',
                '[]',
                '[]',
                0.0,
                datetime('now')
            )
        """)
    conn.commit()
    conn.close()
    print("[+] Database initialized successfully")

if __name__ == "__main__":
    init_db()
