"""
setup_db.py  —  Run this once to create the database and all tables.
Usage:  python setup_db.py
"""

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# ── Connect without selecting a DB first ──────────────────────────────────────
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
)
cur = conn.cursor()

DB = os.getenv("DB_NAME", "ticket_booking")

# ── Create database ───────────────────────────────────────────────────────────
cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB}")
cur.execute(f"USE {DB}")

# ── Tables ────────────────────────────────────────────────────────────────────
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id   INT          AUTO_INCREMENT PRIMARY KEY,
    name      VARCHAR(100) NOT NULL,
    email     VARCHAR(100) NOT NULL UNIQUE,
    phone     VARCHAR(15)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS events (
    event_id  INT          AUTO_INCREMENT PRIMARY KEY,
    name      VARCHAR(150) NOT NULL,
    location  VARCHAR(200) NOT NULL,
    date      DATETIME     NOT NULL,
    price     DECIMAL(8,2) NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT      AUTO_INCREMENT PRIMARY KEY,
    user_id    INT      NOT NULL,
    event_id   INT      NOT NULL,
    tickets    INT      NOT NULL DEFAULT 1,
    date       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)  REFERENCES users(user_id)  ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS payments (
    payment_id INT         AUTO_INCREMENT PRIMARY KEY,
    booking_id INT         NOT NULL UNIQUE,
    method     VARCHAR(50) NOT NULL,
    status     ENUM('pending','completed','failed') NOT NULL DEFAULT 'pending',
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
)
""")

# ── Seed a few sample events ──────────────────────────────────────────────────
cur.execute("SELECT COUNT(*) FROM events")
if cur.fetchone()[0] == 0:
    sample_events = [
        ("Tech Fest 2025",       "IIT Delhi Auditorium",   "2025-08-15 10:00:00", 499.00),
        ("Cultural Night",       "City Open Amphitheatre", "2025-09-05 18:00:00", 299.00),
        ("Startup Summit",       "Convention Centre, MG Rd","2025-10-12 09:00:00", 799.00),
        ("Annual Sports Meet",   "University Ground",       "2025-11-01 08:00:00",  99.00),
        ("Music Carnival 2025",  "Jaipur Heritage Ground",  "2025-12-20 17:00:00", 599.00),
    ]
    cur.executemany(
        "INSERT INTO events (name, location, date, price) VALUES (%s, %s, %s, %s)",
        sample_events,
    )
    print(f"  Inserted {len(sample_events)} sample events.")

conn.commit()
cur.close()
conn.close()

print("✅  Database and tables created successfully.")
print(f"    Database : {DB}")
print("    Tables   : users, events, bookings, payments")
