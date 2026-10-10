# Venue360 — Console Version

A standalone Python event-management application developed for the
Programming Fundamentals component of our academic team project.

This version runs in the terminal and is independent of the Flask
web application in the repository root.

## Features

- Admin, student, and faculty menus
- User registration and login
- Event creation, viewing, updating, and deletion
- Event registration and cancellation
- Search, filtering, and sorting
- JSON file storage and activity logging

## Run

Python 3 is required. No third-party packages are needed.

From the repository root:

```powershell
Set-Location .\console
py -3 app.py
```

The application initializes missing data files in the current working
directory. Run it from the console folder to keep its data separate.

On a fresh setup, the demo administrator account is:
- Username: admin
- Password: admin123

## Notes

This is an academic demonstration, not a production authentication system.
The included sample events use historical dates.

Generated user records, events, registrations, and logs are excluded
from version control.