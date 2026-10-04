# Venue360

Venue360 is an academic team project for discovering university events and accessing student and administrator workspaces. It was developed for Programming Fundamentals and AICT coursework at UET Lahore, Main Campus.

## My contribution

**Muhammad Amir:** frontend design, planning the features to be available, and defining the website's user flow. The overall application was a team project; the backend is not presented as my sole contribution.

## Features implemented in the backend

- Public landing page with events and an About page with societies derived from event data.
- Student registration, login, logout and profile updates.
- Student event registration and cancellation.
- Optional redirects to an event's Google Form.
- Administrator login and an event-management workspace.
- Event creation, editing and deletion.
- Administrator registration lists with event filtering and text search.
- JSON-file persistence and password hashing through Werkzeug.

Event fee and price fields store information; the application does not contain a payment-processing flow.

## Technology

Python, Flask, Werkzeug, HTML, CSS, JavaScript and JSON files.

## Project files

| Path | Purpose |
| --- | --- |
| `app.py` | Flask application, routes and JSON persistence |
| `templates/` | HTML templates rendered by the application |
| `static/` | Frontend assets |
| `files/` | Additional HTML files retained with the project |
| `scratch/test_flask_app.py` | Existing manual smoke-test script |
| `setup_demo.py` | Creates fictional account data for a fresh checkout |
| `requirements.txt` | Direct Python dependencies |
| `data/` | Local runtime data, excluded from version control |

The application renders these files from **templates/**:

- `index.html`
- `about_us.html`
- `student_portal.html`
- `admin_portal.html`
- `404.html`
- `500.html`

## Run locally on Windows / PowerShell

Use Python 3.9 or newer. Run these commands from the project root.

### 1. Create an isolated environment and install dependencies

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Initialize fictional demo data

```powershell
.\.venv\Scripts\python.exe setup_demo.py
```

This creates the four runtime JSON files only when none of them already exists. If any runtime file exists, setup skips all writes and preserves the existing files.

| Role | Demo username/email | Demo password |
| --- | --- | --- |
| Student | student@uet.com | student123 |
| Administrator | admin@uet.com | admin123 |

These accounts are fictional public fixtures for local demonstrations and match the identities in the existing smoke-test script. An existing local dataset may have different accounts.

### 3. Set a session secret and start the application

```powershell
$env:SECRET_KEY = & .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
.\.venv\Scripts\python.exe app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

Set the environment variable again when opening a new terminal. Keep the same value while using the same local server session.

## Runtime data

Real account and registration files are excluded from Git. The application can create missing JSON files as empty lists. A fresh administrator account is supplied by `setup_demo.py`, because the application has no administrator-registration route.

Events start empty. Sign in as the demo administrator to create an event, then use the demo student account to register for it.

## Existing smoke check

After fresh demo setup, from the project root:

```powershell
$env:SECRET_KEY = & .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
.\.venv\Scripts\python.exe scratch\test_flask_app.py
```

The script exercises the landing page, student login, logout and administrator login. It depends on templates and seeded accounts, and its page-text assertions are only a basic smoke check.

## Project status

This is an academic prototype intended for local demonstration. It uses JSON-file storage and the Flask development server. The repository is a source-code showcase; a live deployment is optional.

## References

- [Flask installation and dependencies](https://flask.palletsprojects.com/en/stable/installation/)
- [Flask configuration and session secrets](https://flask.palletsprojects.com/en/stable/config/)

