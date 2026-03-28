import sqlite3

# ─────────────────────────────────────────────
# REGULO SYSTEMS — seed_db.py
# Run once to populate zoning.db with test data
# Usage: python seed_db.py
# ─────────────────────────────────────────────

DB_NAME = "zoning.db"

def seed_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        id                        INTEGER PRIMARY KEY AUTOINCREMENT,
        erf_number                TEXT,
        suburb                    TEXT,
        city                      TEXT,
        zone                      TEXT,
        land_use                  TEXT,
        coverage                  TEXT,
        floor_area_ratio          REAL,
        height                    TEXT,
        setbacks                  TEXT,
        erf_size                  INTEGER,
        coverage_numeric          REAL,
        height_numeric            REAL,
        heritage_overlay          INTEGER DEFAULT 0,
        environmental_restriction INTEGER DEFAULT 0,
        notes                     TEXT
    )
    """)

    cursor.execute("DELETE FROM properties")

    properties = [
        (
            "3864",
            "Central",
            "Gqeberha",
            "Business 1",
            "Commercial / Mixed Use",
            "100%",
            3.0,
            "20m",
            "Street: 0m | Side: 2m | Rear: 3m",
            1200,
            100.0,
            20,
            0, 0,
            "Prime commercial zoning suitable for retail, office, or mixed-use development."
        ),
        (
            "1021",
            "Summerstrand",
            "Gqeberha",
            "Residential 3",
            "Medium Density Residential",
            "60%",
            1.2,
            "10m",
            "Street: 3m | Side: 2m | Rear: 3m",
            900,
            60.0,
            10,
            0, 0,
            "Suitable for townhouse or sectional title development."
        ),
        (
            "447",
            "Walmer",
            "Gqeberha",
            "Residential 1",
            "Single Residential",
            "50%",
            0.8,
            "8m",
            "Street: 4.5m | Side: 1.5m | Rear: 3m",
            750,
            50.0,
            8,
            1, 0,
            "Property falls within a heritage protection overlay. Additional approvals may be required."
        ),
        (
            "2230",
            "Newton Park",
            "Gqeberha",
            "Business 2",
            "Commercial / Retail",
            "75%",
            2.5,
            "15m",
            "Street: 0m | Side: 2m | Rear: 3m",
            1500,
            75.0,
            15,
            0, 0,
            "High-visibility commercial node suitable for retail or office park development."
        ),
        (
            "781",
            "Humewood",
            "Gqeberha",
            "Residential 2",
            "Low to Medium Density Residential",
            "60%",
            1.0,
            "10m",
            "Street: 4m | Side: 1.5m | Rear: 3m",
            680,
            60.0,
            10,
            0, 1,
            "Environmental sensitivity zone — proximity to coastal dune system. EIA may be required."
        ),
        (
            "912",
            "Richmond Hill",
            "Gqeberha",
            "Mixed Use",
            "Mixed Use — Residential / Commercial",
            "70%",
            2.0,
            "14m",
            "Street: 2m | Side: 2m | Rear: 3m",
            1100,
            70.0,
            14,
            1, 0,
            "Heritage overlay applies. Mixed-use development potential subject to heritage authority approval."
        ),
    ]

    cursor.executemany("""
    INSERT INTO properties (
        erf_number, suburb, city, zone, land_use, coverage,
        floor_area_ratio, height, setbacks, erf_size,
        coverage_numeric, height_numeric,
        heritage_overlay, environmental_restriction, notes
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, properties)

    conn.commit()
    count = cursor.execute("SELECT COUNT(*) FROM properties").fetchone()[0]
    conn.close()

    print(f"✅ Database seeded — {count} properties inserted into {DB_NAME}")
    print()
    for p in properties:
        erf, suburb, erf_size, far = p[0], p[1], p[9], p[6]
        buildable = erf_size * far
        heritage = "⚠ Heritage" if p[12] else ""
        enviro   = "⚠ Environmental" if p[13] else ""
        flags    = " ".join(filter(None, [heritage, enviro])) or "✓ No overlays"
        print(f"   ERF {erf:<6} | {suburb:<15} | {buildable:>7,.0f} m² buildable | {flags}")

if __name__ == "__main__":
    seed_database()