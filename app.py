"""
app.py  —  Event Ticket Booking System (Flask entry point + all routes)
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
import models, os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "changeme")


# ── Helper ────────────────────────────────────────────────────────────────────

def logged_in():
    return "user_id" in session


# ── Auth ──────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET", "POST"])
def index():
    """Landing page with inline register / login."""
    if logged_in():
        return redirect(url_for("events"))

    if request.method == "POST":
        action = request.form.get("action")
        email  = request.form.get("email", "").strip()
        name   = request.form.get("name",  "").strip()
        phone  = request.form.get("phone", "").strip()

        if action == "register":
            if models.get_user_by_email(email):
                flash("Email already registered. Please login.", "error")
            else:
                uid = models.create_user(name, email, phone)
                session["user_id"]   = uid
                session["user_name"] = name
                flash("Account created! Welcome.", "success")
                return redirect(url_for("events"))

        elif action == "login":
            user = models.get_user_by_email(email)
            if not user:
                flash("No account found with that email.", "error")
            else:
                session["user_id"]   = user["user_id"]
                session["user_name"] = user["name"]
                return redirect(url_for("events"))

    return render_template("index.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ── Events ────────────────────────────────────────────────────────────────────

@app.route("/events")
def events():
    if not logged_in():
        return redirect(url_for("index"))
    all_events = models.get_all_events()
    return render_template("events.html", events=all_events)


# ── Booking ───────────────────────────────────────────────────────────────────

@app.route("/book/<int:event_id>", methods=["GET", "POST"])
def book(event_id):
    if not logged_in():
        return redirect(url_for("index"))

    event = models.get_event(event_id)
    if not event:
        flash("Event not found.", "error")
        return redirect(url_for("events"))

    if request.method == "POST":
        tickets = int(request.form.get("tickets", 1))

        if tickets < 1:
            flash("Select at least 1 ticket.", "error")
            return redirect(url_for("book", event_id=event_id))

        user_id = session.get("user_id")
        user = models.get_user(user_id)
        if not user:
            flash("User session invalid. Please login again.", "error")
            session.clear()
            return redirect(url_for("index"))

        booking_id = models.create_booking(user_id, event_id, tickets)

        return redirect(url_for("payment", booking_id=booking_id))

    return render_template("book.html", event=event)


# ── Payment ───────────────────────────────────────────────────────────────────

@app.route("/payment/<int:booking_id>", methods=["GET", "POST"])
def payment(booking_id):
    if not logged_in():
        return redirect(url_for("index"))

    user_id = session.get("user_id")
    user = models.get_user(user_id)
    if not user:
        flash("User session invalid. Please login again.", "error")
        session.clear()
        return redirect(url_for("index"))

    booking = models.get_booking(booking_id)
    if not booking or booking["user_id"] != user_id: 
        flash("Booking not found.", "error")
        return redirect(url_for("my_bookings"))

    existing = models.get_payment(booking_id)

    if request.method == "POST":
        method = request.form.get("method", "card")
        if not existing:
            models.create_payment(booking_id, method)
        models.complete_payment(booking_id)
        flash("Payment successful! Your tickets are confirmed.", "success")
        return redirect(url_for("my_bookings"))

    total = booking["price"] * booking["tickets"]
    return render_template("payment.html", booking=booking, total=total, existing=existing)


# ── My Bookings ───────────────────────────────────────────────────────────────

@app.route("/my-bookings")
def my_bookings():
    if not logged_in():
        return redirect(url_for("index"))
    
    user_id = session.get("user_id")
    user = models.get_user(user_id)
    if not user:
        flash("User session invalid. Please login again.", "error")
        session.clear()
        return redirect(url_for("index"))
    
    bookings = models.get_booking_by_user(user_id)
    return render_template("bookings.html", bookings=bookings)


# ── Run ───────────────────────────────────────────────────────────────────────



if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG", "True") == "True")