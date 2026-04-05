# 🎟 Event Ticket Booking System

A minor project for online event ticket booking built with Python (Flask) and MySQL.

---

## 📋 Project Description

A web-based ticket booking system where users can register, browse upcoming events, book tickets, and make payments. The system manages users, events, bookings, and payments through a relational MySQL database.

**Key Features:**
- User registration and login (by email)
- Browse and view upcoming events
- Book multiple tickets per event
- Payment processing with multiple methods (UPI, Card, Net Banking, Wallet)
- View all personal bookings with payment status

---

## 🗂 File Structure

```
event-ticket-booking/
├── app.py          # Flask app — all routes
├── models.py       # DB connection + query helpers
├── setup_db.py     # Creates database and tables (run once)
├── requirements.txt
├── .env            # Environment variables
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── index.html      # Login / Register
    ├── events.html     # Event listing
    ├── book.html       # Booking form
    ├── payment.html    # Payment page
    └── bookings.html   # My Bookings
```

---

## 🛠 Tech Stack

| Layer    | Technology           |
|----------|----------------------|
| Backend  | Python 3, Flask      |
| Database | MySQL                |
| Frontend | HTML, CSS (minimal)  |
| Config   | python-dotenv (.env) |

---

## 🗄 Database Schema

```
users       (user_id PK, name, email, phone)
events      (event_id PK, name, location, date, price)
bookings    (booking_id PK, user_id FK, event_id FK, tickets, date)
payments    (payment_id PK, booking_id FK, method, status)
```

**Relationships:**
- `bookings.user_id` → `users.user_id`
- `bookings.event_id` → `events.event_id`
- `payments.booking_id` → `bookings.booking_id`

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.8+
- MySQL Server running locally

### 2. Clone / download the project
```bash
cd event-ticket-booking
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Edit the `.env` file with your MySQL credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=ticket_booking
SECRET_KEY=any-random-secret
DEBUG=True
```

### 5. Create the database and tables
```bash
python setup_db.py
```
This creates the `ticket_booking` database, all four tables, and seeds 5 sample events.

### 6. Run the application
```bash
python app.py
```
Open your browser at **http://127.0.0.1:5000**

---

## 🚀 Usage Flow

1. **Register** with your name, email, and phone — or **Login** with your email.
2. Browse **Upcoming Events** and click **Book Now**.
3. Select the number of tickets → **Proceed to Payment**.
4. Choose a payment method and confirm.
5. View all your bookings under **My Bookings**.

---

## 👩‍💻 Team / Author

Minor Project — B.Tech (Computer Science)  
Academic Year 2024–25
