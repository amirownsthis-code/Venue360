import os
import json
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

STUDENTS_FILE = os.path.join("data", "students.json")
ADMINS_FILE = os.path.join("data", "admins.json")
EVENTS_FILE = os.path.join("data", "events.json")
REGISTRATIONS_FILE = os.path.join("data", "registrations.json")

# ------------------ Utility Functions ------------------

def load_json(file_path):
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_json(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_next_id(data):
    return max([item.get("id", 0) for item in data], default=0) + 1

# ------------------ Decorators ------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "student_id" not in session:
            flash("Please sign in to access your portal.", "warning")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_id" not in session:
            flash("Admin access required.", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

# ------------------ Context Processor ------------------

@app.context_processor
def inject_globals():
    return {
        "current_year": datetime.now().year
    }

# ------------------ Public Pages ------------------

@app.route("/")
def index():
    events = load_json(EVENTS_FILE)
    featured_events = sorted(events, key=lambda x: x.get("date", ""), reverse=True)

    return render_template(
        "index.html",
        featured_events=featured_events
    )

@app.route("/about")
def about_us():
    events = load_json(EVENTS_FILE)
    societies = sorted(list(set(e.get("society", "").strip() for e in events if e.get("society"))))
    return render_template("about_us.html", societies=societies)

# ------------------ Unified Authentication Handlers ------------------

@app.route("/auth/login", methods=["POST"])
@app.route("/student/login", methods=["POST"])
@app.route("/admin/login", methods=["POST"])
def unified_login():
    identity = request.form.get("username", "").strip().lower()
    password = request.form.get("password", "")

    # 1. Check Admin credentials first
    admins = load_json(ADMINS_FILE)
    admin = next((a for a in admins if a.get("admin_id", "").lower() == identity), None)

    if admin and check_password_hash(admin.get("password", ""), password):
        session.clear()
        session["admin_id"] = admin["admin_id"]
        session["admin_name"] = admin.get("name", "Administrator")
        flash("Logged into Admin Workspace.", "success")
        return redirect(url_for("admin_portal"))

    # 2. Check Student credentials
    students = load_json(STUDENTS_FILE)
    student = next((s for s in students if s.get("username", "").lower() == identity or s.get("email", "").lower() == identity), None)

    if student and check_password_hash(student.get("password", ""), password):
        session.clear()
        session["student_id"] = student["id"]
        session["student_name"] = student["username"]
        session["student_email"] = student["email"]
        flash(f"Welcome back, {student['username']}!", "success")
        return redirect(url_for("student_portal"))

    flash("Invalid username/email or password.", "danger")
    return redirect(url_for("index"))

@app.route("/auth/student/register", methods=["POST"])
@app.route("/student/register", methods=["POST"])
def student_register():
    students = load_json(STUDENTS_FILE)
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not username or not email or not password:
        flash("All required fields must be filled out.", "danger")
        return redirect(url_for("index"))

    if password != confirm_password:
        flash("Passwords do not match!", "danger")
        return redirect(url_for("index"))

    if any(s.get("username", "").lower() == username.lower() or s.get("email", "").lower() == email for s in students):
        flash("Username or Email already registered. Please sign in.", "warning")
        return redirect(url_for("index"))

    new_student = {
        "id": get_next_id(students),
        "username": username,
        "email": email,
        "password": generate_password_hash(password),
        "phone": request.form.get("phone", "").strip(),
        "department": request.form.get("department", "").strip(),
        "year": request.form.get("year", "").strip(),
        "student_id": request.form.get("student_id", "").strip()
    }

    students.append(new_student)
    save_json(STUDENTS_FILE, students)
    
    session.clear()
    session["student_id"] = new_student["id"]
    session["student_name"] = new_student["username"]
    session["student_email"] = new_student["email"]
    flash("Account created! Welcome to Venue360.", "success")
    return redirect(url_for("student_portal"))

@app.route("/logout")
@app.route("/student/logout")
@app.route("/admin/logout")
@app.route("/auth/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("index"))

# ------------------ Student Workspace ------------------

@app.route("/student")
@app.route("/student/portal")
@login_required
def student_portal():
    students = load_json(STUDENTS_FILE)
    events = load_json(EVENTS_FILE)
    registrations = load_json(REGISTRATIONS_FILE)

    student_id = session["student_id"]
    student = next((s for s in students if s["id"] == student_id), {})

    my_regs = [r for r in registrations if r.get("student_id") == student_id]
    registered_event_ids = [r.get("event_id") for r in my_regs]
    my_events = [e for e in events if e.get("id") in registered_event_ids]

    return render_template(
        "student_portal.html",
        student=student,
        events=events,
        my_events=my_events,
        registered_event_ids=registered_event_ids
    )

@app.route("/student/profile/update", methods=["POST"])
@app.route("/student/profile", methods=["GET", "POST"])
@login_required
def student_profile():
    if request.method == "POST":
        students = load_json(STUDENTS_FILE)
        student_id = session["student_id"]
        student = next((s for s in students if s["id"] == student_id), None)

        if student:
            student["phone"] = request.form.get("phone", "").strip()
            student["department"] = request.form.get("department", "").strip()
            student["year"] = request.form.get("year", "").strip()
            student["student_id"] = request.form.get("student_id", "").strip()

            new_password = request.form.get("new_password", "").strip()
            if new_password:
                student["password"] = generate_password_hash(new_password)

            save_json(STUDENTS_FILE, students)
            flash("Profile details updated!", "success")

    return redirect(url_for("student_portal", tab="profile"))

@app.route("/student/event/register/<int:event_id>", methods=["POST"])
@app.route("/student/register-event/<int:event_id>", methods=["POST"])
@login_required
def register_event(event_id):
    registrations = load_json(REGISTRATIONS_FILE)
    events = load_json(EVENTS_FILE)
    student_id = session["student_id"]

    event = next((e for e in events if e.get("id") == event_id), None)
    if not event:
        flash("Event not found.", "danger")
        return redirect(url_for("student_portal", tab="events"))

    if not any(r.get("student_id") == student_id and r.get("event_id") == event_id for r in registrations):
        registrations.append({
            "student_id": student_id,
            "event_id": event_id,
            "created_at": datetime.now().strftime("%d %b %Y, %I:%M %p")
        })
        save_json(REGISTRATIONS_FILE, registrations)
        flash(f"Successfully registered for {event['title']}!", "success")

    form_link = event.get("google_form_link")
    if form_link and form_link.startswith("http"):
        return redirect(form_link)
    return redirect(url_for("student_portal", tab="registrations"))

@app.route("/student/event/unregister/<int:event_id>", methods=["POST"])
@login_required
def unregister_event(event_id):
    registrations = load_json(REGISTRATIONS_FILE)
    student_id = session["student_id"]

    new_regs = [r for r in registrations if not (r.get("student_id") == student_id and r.get("event_id") == event_id)]

    if len(new_regs) < len(registrations):
        save_json(REGISTRATIONS_FILE, new_regs)
        flash("Registration cancelled.", "info")

    return redirect(url_for("student_portal", tab="registrations"))

# ------------------ Admin Workspace ------------------

@app.route("/admin")
@app.route("/admin/portal")
@app.route("/admin/dashboard")
@admin_required
def admin_portal():
    events = load_json(EVENTS_FILE)
    registrations = load_json(REGISTRATIONS_FILE)
    students = load_json(STUDENTS_FILE)

    selected_event_str = request.args.get("event_id", "").strip()
    search_q = request.args.get("q", "").strip().lower()
    selected_event_id = int(selected_event_str) if selected_event_str.isdigit() else None

    for event in events:
        event["reg_count"] = sum(1 for r in registrations if r.get("event_id") == event.get("id"))

    display_regs = []
    for r in registrations:
        if selected_event_id and r.get("event_id") != selected_event_id:
            continue

        student = next((s for s in students if s.get("id") == r.get("student_id")), None)
        event = next((e for e in events if e.get("id") == r.get("event_id")), None)

        if student and event:
            reg_data = {
                "student_name": student.get("username", "Unknown"),
                "student_id": student.get("student_id", "N/A"),
                "department": student.get("department", "N/A"),
                "semester": student.get("year", "N/A"),
                "email": student.get("email", "N/A"),
                "phone": student.get("phone", "N/A"),
                "event_title": event.get("title", "Unknown"),
                "event_society": event.get("society", "N/A"),
                "created_at": r.get("created_at", "N/A")
            }

            if search_q:
                match = (
                    search_q in reg_data["student_name"].lower()
                    or search_q in reg_data["student_id"].lower()
                    or search_q in reg_data["email"].lower()
                    or search_q in reg_data["event_title"].lower()
                    or search_q in reg_data["department"].lower()
                )
                if not match:
                    continue

            display_regs.append(reg_data)

    return render_template(
        "admin_portal.html",
        events=events,
        registrations=display_regs,
        selected_event=selected_event_id,
        search_q=search_q
    )

@app.route("/admin/event/add", methods=["POST"])
@app.route("/admin/add-event", methods=["GET", "POST"])
@admin_required
def add_event():
    if request.method == "POST":
        events = load_json(EVENTS_FILE)

        title = request.form.get("title", "").strip()
        society = request.form.get("society", "").strip()
        date = request.form.get("date", "").strip()
        time = request.form.get("time", "").strip()
        venue = request.form.get("venue", "").strip()
        type_str = request.form.get("type", "").strip()
        fee_type = request.form.get("fee_type", "Free").strip()
        price = request.form.get("price", "Free").strip()
        image = request.form.get("image", "club.jpeg").strip()
        description = request.form.get("description", "").strip()
        google_form_link = request.form.get("google_form_link", "").strip()

        if not title or not society or not date:
            flash("Event title, society, and date are required.", "danger")
            return redirect(url_for("admin_portal", tab="manage"))

        new_event = {
            "id": get_next_id(events),
            "title": title,
            "society": society,
            "type": type_str,
            "date": date,
            "time": time,
            "venue": venue,
            "fee_type": fee_type,
            "price": price if fee_type == "Paid" else "Free",
            "image": image or "club.jpeg",
            "description": description,
            "google_form_link": google_form_link
        }

        events.append(new_event)
        save_json(EVENTS_FILE, events)
        flash(f"Event '{title}' created successfully!", "success")

    return redirect(url_for("admin_portal", tab="manage"))

@app.route("/admin/event/edit/<int:event_id>", methods=["POST"])
@app.route("/admin/edit-event/<int:event_id>", methods=["GET", "POST"])
@admin_required
def edit_event(event_id):
    events = load_json(EVENTS_FILE)
    event = next((e for e in events if e.get("id") == event_id), None)

    if not event:
        flash("Event not found.", "danger")
        return redirect(url_for("admin_portal", tab="manage"))

    if request.method == "POST":
        fee_type = request.form.get("fee_type", "Free").strip()
        event["title"] = request.form.get("title", "").strip()
        event["society"] = request.form.get("society", "").strip()
        event["type"] = request.form.get("type", "").strip()
        event["date"] = request.form.get("date", "").strip()
        event["time"] = request.form.get("time", "").strip()
        event["venue"] = request.form.get("venue", "").strip()
        event["fee_type"] = fee_type
        event["price"] = request.form.get("price", "Free").strip() if fee_type == "Paid" else "Free"
        event["image"] = request.form.get("image", "club.jpeg").strip()
        event["description"] = request.form.get("description", "").strip()
        event["google_form_link"] = request.form.get("google_form_link", "").strip()

        save_json(EVENTS_FILE, events)
        flash(f"Event '{event['title']}' updated successfully!", "success")

    return redirect(url_for("admin_portal", tab="manage"))

@app.route("/admin/event/delete/<int:event_id>", methods=["POST", "GET"])
@app.route("/admin/delete-event/<int:event_id>", methods=["POST", "GET"])
@admin_required
def delete_event(event_id):
    events = load_json(EVENTS_FILE)
    registrations = load_json(REGISTRATIONS_FILE)

    event = next((e for e in events if e.get("id") == event_id), None)
    if not event:
        flash("Event not found.", "danger")
        return redirect(url_for("admin_portal", tab="manage"))

    new_events = [e for e in events if e.get("id") != event_id]
    save_json(EVENTS_FILE, new_events)

    new_registrations = [r for r in registrations if r.get("event_id") != event_id]
    save_json(REGISTRATIONS_FILE, new_registrations)

    flash(f"Event '{event['title']}' deleted.", "info")
    return redirect(url_for("admin_portal", tab="manage"))

# ------------------ Error Handlers ------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)