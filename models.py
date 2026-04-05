"""
models.py  —  Database connection + all query helpers.
"""

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


def get_conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database="ticket_system"
    )


# ── user ─────────────────────────────────────────────────────────────────────

def get_user_by_email(email):
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM user WHERE email = %s", (email,))
    row = cur.fetchone(); cur.close(); conn.close()
    return row

def create_user(name, email, phone):
    conn = get_conn(); cur = conn.cursor()
    cur.execute(
        "INSERT INTO user (name, email, phone) VALUES (%s, %s, %s)",
        (name, email, phone),
    )
    uid = cur.lastrowid; conn.commit(); cur.close(); conn.close()
    return uid

def get_user(user_id):
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
    row = cur.fetchone(); cur.close(); conn.close()
    return row


# ── event ────────────────────────────────────────────────────────────────────

def get_all_events():
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM event ORDER BY date ASC")
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def get_event(event_id):
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM event WHERE event_id = %s", (event_id,))
    row = cur.fetchone(); cur.close(); conn.close()
    return row


# ── booking ──────────────────────────────────────────────────────────────────

def create_booking(user_id, event_id, number_of_tickets):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO booking (user_id, event_id, number_of_tickets) VALUES (%s, %s, %s)",
        (user_id, event_id, number_of_tickets)
    )

    bid = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()

    return bid

def get_booking(booking_id):
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT b.*, e.name AS event_name, e.location, e.date AS event_date,
               e.price, u.name AS user_name, u.email
        FROM   booking b
        JOIN   event   e ON e.event_id  = b.event_id
        JOIN   user    u ON u.user_id   = b.user_id
        WHERE  b.booking_id = %s
    """, (booking_id,))
    row = cur.fetchone(); cur.close(); conn.close()
    return row

def get_booking_by_user(user_id):
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT b.*, e.name AS event_name, e.location, e.date AS event_date,
               e.price, p.status AS pay_status, p.method AS pay_method
        FROM   booking b
        JOIN   event   e ON e.event_id  = b.event_id
        LEFT JOIN payment p ON p.booking_id = b.booking_id
        WHERE  b.user_id = %s
        ORDER  BY b.date DESC
    """, (user_id,))
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows


# ── payment ──────────────────────────────────────────────────────────────────

def create_payment(booking_id, method):
    conn = get_conn(); cur = conn.cursor()
    cur.execute(
        "INSERT INTO payment (booking_id, method, status) VALUES (%s, %s, 'pending')",
        (booking_id, method),
    )
    pid = cur.lastrowid; conn.commit(); cur.close(); conn.close()
    return pid

def complete_payment(booking_id):
    conn = get_conn(); cur = conn.cursor()
    cur.execute(
        "UPDATE payment SET status = 'completed' WHERE booking_id = %s",
        (booking_id,),
    )
    conn.commit(); cur.close(); conn.close()

def get_payment(booking_id):
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM payment WHERE booking_id = %s", (booking_id,))
    row = cur.fetchone(); cur.close(); conn.close()
    return row
