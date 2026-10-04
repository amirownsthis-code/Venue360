import sys
sys.path.insert(0, '.')
import app

client = app.app.test_client()

print("--- Testing Public Landing Page ---")
res = client.get("/")
assert res.status_code == 200
print("GET / -> 200 OK")

print("\n--- Testing Unified Login (as Student) ---")
res = client.post("/auth/login", data={"username": "student@uet.com", "password": "student123"}, follow_redirects=True)
assert res.status_code == 200
assert b"My Events" in res.data or b"Welcome" in res.data
print("POST /auth/login (Student) -> Logged in to Student Portal!")

res = client.get("/logout", follow_redirects=True)
assert res.status_code == 200
print("GET /logout -> Logged out")

print("\n--- Testing Unified Login (as Admin) ---")
res = client.post("/auth/login", data={"username": "admin@uet.com", "password": "admin123"}, follow_redirects=True)
assert res.status_code == 200
assert b"Admin Workspace" in res.data
print("POST /auth/login (Admin) -> Logged in to Admin Workspace!")

print("\n--- ALL TESTS PASSED WITH 100% SUCCESS! ---")
