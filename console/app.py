import json
import os
import getpass
from datetime import datetime
import hashlib  # For password hashing

#  FILE OPERATIONS

def read_users_file():
    try:
        if not os.path.exists('users.json'):
            create_default_admin()
            return [get_default_admin()]
        with open('users.json', 'r') as file:
            users = json.load(file)
            return users
    except Exception as e:
        print(f"Error reading users file: {e}")
        return []

def write_users_file(users):
    try:
        with open('users.json', 'w') as file:
            json.dump(users, file, indent=4)
        return True
    except Exception as e:
        print(f"Error writing users file: {e}")
        return False

def read_events_file():
    try:
        if not os.path.exists('events.json'):
            # Create sample data if file doesn't exist
            sample_events = [
                {
                    "id": 1,
                    "name": "Tech Workshop",
                    "society": "Computer Society",
                    "date": "2024-12-15",
                    "time": "10:00 AM",
                    "location": "Room 101",
                    "description": "Learn programming basics",
                    "capacity": 50
                },
                {
                    "id": 2,
                    "name": "Music Concert",
                    "society": "Music Club",
                    "date": "2024-11-20",
                    "time": "6:00 PM",
                    "location": "Auditorium",
                    "description": "Annual music festival",
                    "capacity": 200
                }
            ]
            write_events_file(sample_events)
            return sample_events
        
        with open('events.json', 'r') as file:
            events = json.load(file)
            return events
    except Exception as e:
        print(f"Error reading events file: {e}")
        return []

def write_events_file(events):
    try:
        with open('events.json', 'w') as file:
            json.dump(events, file, indent=4)
        return True
    except Exception as e:
        print(f"Error writing events file: {e}")
        return False

def read_registrations_file():
    try:
        if not os.path.exists('registrations.json'):
            with open('registrations.json', 'w') as file:
                json.dump([], file)
            return []
        
        with open('registrations.json', 'r') as file:
            registrations = json.load(file)
            return registrations
    except Exception as e:
        print(f"Error reading registrations file: {e}")
        return []

def write_registrations_file(registrations):
    try:
        with open('registrations.json', 'w') as file:
            json.dump(registrations, file, indent=4)
        return True
    except Exception as e:
        print(f"Error writing registrations file: {e}")
        return False

def log_action(action, username="System"):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {username}: {action}\n"
        
        with open('system_log.txt', 'a') as log_file:
            log_file.write(log_entry)
    except Exception as e:
        print(f"Logging error: {e}")

# USER AUTHENTICATION

def hash_password(password):
    #This line turns the simple password into hashed_password using SHA-256 Algorithm
    return hashlib.sha256(password.encode()).hexdigest()

def get_default_admin():
    return {
        "id": 1,
        "username": "admin",
        "password_hash": hash_password("admin123"),
        "full_name": "System Administrator",
        "email": "admin@university.edu",
        "role": "admin",
        "created_at": "2024-01-01",
        "is_active": True
    }

def create_default_admin():
    admin_user = get_default_admin()
    write_users_file([admin_user])
    return admin_user

def find_user_by_username(username):
    users = read_users_file()
    for user in users:
        if user.get('username') == username and user.get('is_active', True):
            return user
    return None

def user_login():
    print("\n" + "="*50)
    print("USER LOGIN")
    print("="*50)
    
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        print(f"\nAttempt {attempts + 1} of {max_attempts}")
        username = input("Username: ").strip()
        
        if not username:
            print("Username cannot be empty!")
            continue
        
        # We use getpass to hide input Password
        try:
            password = getpass.getpass("Password: ")
        except Exception:
            password = input("Password: ").strip()
        
        user = find_user_by_username(username)
        
        if user:
            if user['password_hash'] == hash_password(password):
                print(f"\n✓ Login successful!")
                print(f"Welcome, {user['full_name']}!")
                log_action(f"User logged in: {username}", username)
                return user
            else:
                print("\n✗ Incorrect password!")
        else:
            print("\n✗ User not found!")
        
        attempts += 1
    
    print(f"\n✗ Maximum login attempts reached. Please try again later.")
    return None

def user_registration():
    """Register a new user"""
    print("\n" + "="*50)
    print("USER REGISTRATION")
    print("="*50)
    
    users = read_users_file()
    
    while True:
        username = input("\nChoose a username: ").strip()
        
        if not username:
            print("Username cannot be empty!")
            continue
        
        if find_user_by_username(username):
            print(f"✗ Username '{username}' already exists. Please choose another.")
            continue
        
        if len(username) < 3:
            print("Username must be at least 3 characters long.")
            continue
        
        break
    
    while True:
        try:
            password = getpass.getpass("Choose a password: ")
        except Exception:
            password = input("Choose a password: ").strip()
        
        if len(password) < 6:
            print("Password must be at least 6 characters long.")
            continue
        
        try:
            confirm_password = getpass.getpass("Confirm password: ")
        except Exception:
            confirm_password = input("Confirm password: ").strip()
        
        if password != confirm_password:
            print("Passwords do not match!")
            continue
        
        break
    
    full_name = input("Full Name: ").strip()
    
    while True:
        email = input("Email: ").strip()
        if '@' in email and '.' in email:
            break
        else:
            print("Please enter a valid email address.")
    
    print("\nSelect role:")
    print("1. Student (Default)")
    print("2. Faculty")
    
    role_choice = input("Enter choice (1-2): ").strip()
    role = "student" 
    
    if role_choice == '2':
        role = "faculty"
    
    if users:
        new_id = max([user.get('id', 0) for user in users]) + 1
    else:
        new_id = 1
    
    new_user = {
        "id": new_id,
        "username": username,
        "password_hash": hash_password(password),
        "full_name": full_name,
        "email": email,
        "role": role,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "is_active": True
    }
    
    users.append(new_user)
    
    if write_users_file(users):
        print(f"\n✓ Registration successful!")
        print(f"Welcome, {full_name}! You can now login with your credentials.")
        log_action(f"New user registered: {username}", "System")
        return new_user
    else:
        print("\n✗ Error during registration. Please try again.")
        return None

def admin_create_user(current_admin):
    """Admin function to create new users"""
    if current_admin.get('role') != 'admin':
        print("\n✗ Only administrators can create users!")
        return None
    
    print("\n" + "="*50)
    print("CREATE NEW USER (Admin)")
    print("="*50)
    
    users = read_users_file()
    
    while True:
        username = input("\nUsername: ").strip()
        
        if not username:
            print("Username cannot be empty!")
            continue
        
        if find_user_by_username(username):
            print(f"✗ Username '{username}' already exists.")
            continue
        
        if len(username) < 3:
            print("Username must be at least 3 characters long.")
            continue
        
        break
    
    while True:
        try:
            password = getpass.getpass("Password: ")
        except Exception:
            password = input("Password: ").strip()
        
        if len(password) < 6:
            print("Password must be at least 6 characters long.")
            continue
        break
    
    full_name = input("Full Name: ").strip()
    
    while True:
        email = input("Email: ").strip()
        if '@' in email and '.' in email:
            break
        else:
            print("Please enter a valid email address.")
    
    print("\nSelect role:")
    print("1. Student")
    print("2. Faculty")
    print("3. Administrator")
    
    role_choice = input("Enter choice (1-3): ").strip()
    
    if role_choice == '1':
        role = "student"
    elif role_choice == '2':
        role = "faculty"
    elif role_choice == '3':
        role = "admin"
    else:
        print("Invalid choice. Defaulting to Student.")
        role = "student"
    
    new_id = max([user.get('id', 0) for user in users]) + 1
    
    new_user = {
        "id": new_id,
        "username": username,
        "password_hash": hash_password(password),
        "full_name": full_name,
        "email": email,
        "role": role,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "is_active": True
    }
    
    users.append(new_user)
    
    if write_users_file(users):
        print(f"\n✓ User '{username}' created successfully!")
        print(f"Role: {role}")
        log_action(f"Created new user: {username} (Role: {role})", current_admin['username'])
        return new_user
    else:
        print("\n✗ Error creating user.")
        return None

def view_all_users(current_user):
    """View all users (Admin only)"""
    if current_user.get('role') != 'admin':
        print("\n✗ Only administrators can view all users!")
        return
    
    users = read_users_file()
    
    if not users:
        print("\nNo users found!")
        return
    
    print("\n" + "="*70)
    print("ALL SYSTEM USERS")
    print("="*70)
    print(f"{'ID':<5} {'Username':<15} {'Full Name':<20} {'Role':<10} {'Status':<8} {'Created':<12}")
    print("-" * 70)
    
    for user in users:
        user_id = user.get('id', 'N/A')
        username = user.get('username', 'N/A')[:15]
        full_name = user.get('full_name', 'N/A')[:20]
        role = user.get('role', 'N/A')
        status = "Active" if user.get('is_active', False) else "Inactive"
        created = user.get('created_at', 'N/A')
        
        print(f"{user_id:<5} {username:<15} {full_name:<20} {role:<10} {status:<8} {created:<12}")
    
    print("-" * 70)
    print(f"Total Users: {len(users)}")

def change_password(current_user):
    print("\n" + "="*50)
    print("CHANGE PASSWORD")
    print("="*50)
    
    users = read_users_file()
    
    user_index = -1
    for i, user in enumerate(users):
        if user.get('username') == current_user.get('username'):
            user_index = i
            break
    
    if user_index == -1:
        print("\n✗ User not found!")
        return

    try:
        current_password = getpass.getpass("Current Password: ")
    except Exception:
        current_password = input("Current Password: ").strip()
    
    if users[user_index]['password_hash'] != hash_password(current_password):
        print("\n✗ Current password is incorrect!")
        return
    
    while True:
        try:
            new_password = getpass.getpass("New Password: ")
        except Exception:
            new_password = input("New Password: ").strip()
        
        if len(new_password) < 6:
            print("Password must be at least 6 characters long.")
            continue
        
        try:
            confirm_password = getpass.getpass("Confirm New Password: ")
        except Exception:
            confirm_password = input("Confirm New Password: ").strip()
        
        if new_password != confirm_password:
            print("Passwords do not match!")
            continue
        
        break
    
    users[user_index]['password_hash'] = hash_password(new_password)
    
    if write_users_file(users):
        print("\n✓ Password changed successfully!")
        log_action("Changed password", current_user['username'])
    else:
        print("\n✗ Error changing password.")

def admin_manage_users(current_admin):
    """Admin user management"""
    if current_admin.get('role') != 'admin':
        print("\n✗ Access denied! Admin privileges required.")
        return
    
    while True:
        print("\n" + "="*50)
        print("USER MANAGEMENT (Admin)")
        print("="*50)
        print("1. View All Users")
        print("2. Create New User")
        print("3. Deactivate User")
        print("4. Reactivate User")
        print("5. Back to Admin Menu")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            view_all_users(current_admin)
        
        elif choice == '2':
            admin_create_user(current_admin)
        
        elif choice == '3':
            deactivate_user(current_admin)
        
        elif choice == '4':
            reactivate_user(current_admin)
        
        elif choice == '5':
            break
        
        else:
            print("Invalid choice! Please enter 1-5")

def deactivate_user(current_admin):
    if current_admin.get('role') != 'admin':
        print("\n✗ Access denied! Admin privileges required.")
        return
    
    username = input("\nEnter username to deactivate: ").strip()
    
    if username == current_admin['username']:
        print("\n✗ You cannot deactivate your own account!")
        return
    
    users = read_users_file()
    user_found = False
    
    for i, user in enumerate(users):
        if user.get('username') == username:
            if not user.get('is_active', True):
                print(f"\nUser '{username}' is already deactivated.")
                return
            
            confirm = input(f"Are you sure you want to deactivate user '{username}'? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                users[i]['is_active'] = False
                if write_users_file(users):
                    print(f"\n✓ User '{username}' deactivated successfully!")
                    log_action(f"Deactivated user: {username}", current_admin['username'])
                else:
                    print("\n✗ Error deactivating user.")
            else:
                print("Deactivation cancelled.")
            
            user_found = True
            break
    
    if not user_found:
        print(f"\n✗ User '{username}' not found!")

def reactivate_user(current_admin):
    if current_admin.get('role') != 'admin':
        print("\n✗ Access denied! Admin privileges required.")
        return
    
    username = input("\nEnter username to reactivate: ").strip()
    
    users = read_users_file()
    user_found = False
    
    for i, user in enumerate(users):
        if user.get('username') == username:
            if user.get('is_active', True):
                print(f"\nUser '{username}' is already active.")
                return

            confirm = input(f"Are you sure you want to reactivate user '{username}'? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                users[i]['is_active'] = True
                if write_users_file(users):
                    print(f"\n✓ User '{username}' reactivated successfully!")
                    log_action(f"Reactivated user: {username}", current_admin['username'])
                else:
                    print("\n✗ Error reactivating user.")
            else:
                print("Reactivation cancelled.")
            
            user_found = True
            break
    
    if not user_found:
        print(f"\n✗ User '{username}' not found!")

# CRUD OPERATIONS

def add_event(current_user):
    print("\n" + "="*50)
    print("ADD NEW EVENT")
    print("="*50)
    
    events = read_events_file()
    
    if events:
        new_id = max([event.get('id', 0) for event in events]) + 1
    else:
        new_id = 1
    
    print("Enter event details:")
    name = input("Event Name: ").strip()
    society = input("Society/Club: ").strip()
    date = input("Date (YYYY-MM-DD): ").strip()
    time = input("Time (e.g., 10:00 AM): ").strip()
    location = input("Location: ").strip()
    description = input("Description: ").strip()
    
    while True:
        try:
            capacity = int(input("Capacity: ").strip())
            if capacity > 0:
                break
            else:
                print("Capacity must be greater than 0")
        except ValueError:
            print("Please enter a valid number")
    
    new_event = {
        "id": new_id,
        "name": name,
        "society": society,
        "date": date,
        "time": time,
        "location": location,
        "description": description,
        "capacity": capacity,
        "created_by": current_user['username'],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    events.append(new_event)
    
    if write_events_file(events):
        print(f"\n✓ Event '{name}' added successfully!")
        log_action(f"Added event: {name}", current_user['username'])
    else:
        print("\n✗ Error adding event")

def view_all_events():
    """View all events"""
    print("\n" + "="*50)
    print("ALL EVENTS")
    print("="*50)
    
    events = read_events_file()
    
    if not events:
        print("No events found!")
        return
    
    registrations = read_registrations_file()
    
    print(f"\nTotal Events: {len(events)}")
    print("-" * 60)
    
    for event in events:
        reg_count = 0
        for reg in registrations:
            if reg.get('event_id') == event['id']:
                reg_count += 1
        
        status = get_event_status(event['date'])
        status_symbol = "🟢" if status == "upcoming" else "🟡" if status == "ongoing" else "🔴"
        
        print(f"\nID: {event['id']}")
        print(f"Name: {event['name']} {status_symbol}")
        print(f"Society: {event['society']}")
        print(f"Date: {event['date']} | Time: {event['time']}")
        print(f"Location: {event['location']}")
        print(f"Capacity: {reg_count}/{event['capacity']}")
        print(f"Created by: {event.get('created_by', 'System')}")
        print(f"Description: {event['description'][:100]}...")
        print("-" * 40)

def update_event(current_user):
    """Update an existing event"""
    print("\n" + "="*50)
    print("UPDATE EVENT")
    print("="*50)
    
    events = read_events_file()
    
    if not events:
        print("No events to update!")
        return
    
    view_all_events()
    
    try:
        event_id = int(input("\nEnter Event ID to update: ").strip())
    except ValueError:
        print("Invalid ID!")
        return
    
# Find event
    event_found = None
    for event in events:
        if event['id'] == event_id:
            event_found = event
            break
    
    if not event_found:
        print(f"Event with ID {event_id} not found!")
        return
    
    if current_user['role'] != 'admin' and event_found.get('created_by') != current_user['username']:
        print(f"\n✗ You don't have permission to edit this event!")
        print(f"  Event created by: {event_found.get('created_by', 'System')}")
        return
    
    print(f"\nUpdating Event: {event_found['name']}")
    print("Leave blank to keep current value")
    
    name = input(f"New Name [{event_found['name']}]: ").strip()
    society = input(f"New Society [{event_found['society']}]: ").strip()
    date = input(f"New Date [{event_found['date']}]: ").strip()
    time = input(f"New Time [{event_found['time']}]: ").strip()
    location = input(f"New Location [{event_found['location']}]: ").strip()
    description = input(f"New Description [{event_found['description'][:50]}...]: ").strip()
    
    if name:
        event_found['name'] = name
    if society:
        event_found['society'] = society
    if date:
        event_found['date'] = date
    if time:
        event_found['time'] = time
    if location:
        event_found['location'] = location
    if description:
        event_found['description'] = description
    
    # Update timestamp
    event_found['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event_found['updated_by'] = current_user['username']
    
    if write_events_file(events):
        print(f"\n✓ Event updated successfully!")
        log_action(f"Updated event ID: {event_id}", current_user['username'])
    else:
        print("\n✗ Error updating event")

def delete_event(current_user):
    print("\n" + "="*50)
    print("DELETE EVENT")
    print("="*50)
    
    events = read_events_file()
    
    if not events:
        print("No events to delete!")
        return
    
    view_all_events()
    
    try:
        event_id = int(input("\nEnter Event ID to delete: ").strip())
    except ValueError:
        print("Invalid ID!")
        return

    # Find event
    event_found = None
    for event in events:
        if event['id'] == event_id:
            event_found = event
            break
    
    if not event_found:
        print(f"Event with ID {event_id} not found!")
        return
    
    if current_user['role'] != 'admin':
        print(f"\n✗ Only administrators can delete events!")
        return
    confirm = input(f"Are you sure you want to delete event '{event_found['name']}'? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("Deletion cancelled")
        return
    
    original_count = len(events)
    events = [event for event in events if event['id'] != event_id]
    
    if len(events) < original_count:
        registrations = read_registrations_file()
        registrations = [reg for reg in registrations if reg.get('event_id') != event_id]
        write_registrations_file(registrations)
        
        if write_events_file(events):
            print(f"\n✓ Event deleted successfully!")
            log_action(f"Deleted event ID: {event_id}", current_user['username'])
        else:
            print("\n✗ Error deleting event")
    else:
        print(f"\nEvent with ID {event_id} not found!")

# SEARCH & FILTER

def search_by_name():
    print("\n" + "="*50)
    print("SEARCH EVENTS BY NAME")
    print("="*50)
    
    search_term = input("Enter event name to search: ").strip().lower()
    
    if not search_term:
        print("Please enter a search term")
        return
    
    events = read_events_file()
    
    if not events:
        print("No events found!")
        return
    
    found_events = []
    
    for event in events:
        if search_term in event['name'].lower():
            found_events.append(event)
    
    if found_events:
        print(f"\nFound {len(found_events)} event(s):")
        print("-" * 50)
        
        for event in found_events:
            print(f"ID: {event['id']} | Name: {event['name']}")
            print(f"Date: {event['date']} | Society: {event['society']}")
            print(f"Location: {event['location']}")
            print("-" * 30)
    else:
        print(f"\nNo events found with name containing '{search_term}'")

def search_by_date():
    print("\n" + "="*50)
    print("SEARCH EVENTS BY DATE")
    print("="*50)
    
    date_input = input("Enter date to search (YYYY-MM-DD): ").strip()
    
    if not date_input:
        print("Please enter a date")
        return
    
    events = read_events_file()
    if not events:
        print("No events found!")
        return
    
    found_events = []
    for event in events:
        if event['date'] == date_input:
            found_events.append(event)
    
    if found_events:
        print(f"\nFound {len(found_events)} event(s) on {date_input}:")
        print("-" * 50)
        
        for event in found_events:
            print(f"ID: {event['id']} | Name: {event['name']}")
            print(f"Time: {event['time']} | Society: {event['society']}")
            print(f"Location: {event['location']}")
            print("-" * 30)
    else:
        print(f"\nNo events found on {date_input}")

def filter_upcoming_events():
    """Filter upcoming events"""
    print("\n" + "="*50)
    print("UPCOMING EVENTS")
    print("="*50)
    
    events = read_events_file()
    
    if not events:
        print("No events found!")
        return
    
    today = datetime.now().date()
    upcoming_events = []
    for event in events:
        try:
            event_date = datetime.strptime(event['date'], "%Y-%m-%d").date()
            if event_date > today:
                upcoming_events.append(event)
        except:
            continue
    
    if upcoming_events:
        print(f"\nFound {len(upcoming_events)} upcoming event(s):")
        print("-" * 50)
        
        for event in upcoming_events:
            days_until = (datetime.strptime(event['date'], "%Y-%m-%d").date() - today).days
            print(f"ID: {event['id']} | Name: {event['name']}")
            print(f"Date: {event['date']} (in {days_until} days)")
            print(f"Time: {event['time']} | Location: {event['location']}")
            print("-" * 30)
    else:
        print("\nNo upcoming events found!")

def filter_by_location():
    """Filter events by location"""
    print("\n" + "="*50)
    print("FILTER EVENTS BY LOCATION")
    print("="*50)
    
    events = read_events_file()
    
    if not events:
        print("No events found!")
        return
    
    locations = []
    for event in events:
        if event['location'] not in locations:
            locations.append(event['location'])
    
    if not locations:
        print("No locations found!")
        return
    
    print("\nAvailable Locations:")
    for i, location in enumerate(locations, 1):
        print(f"{i}. {location}")
    
    try:
        choice = int(input("\nSelect location number: ").strip())
        if 1 <= choice <= len(locations):
            selected_location = locations[choice - 1]
        else:
            print("Invalid choice!")
            return
    except ValueError:
        print("Invalid input!")
        return
    
    filtered_events = []
    for event in events:
        if event['location'] == selected_location:
            filtered_events.append(event)
    
    if filtered_events:
        print(f"\nFound {len(filtered_events)} event(s) at {selected_location}:")
        print("-" * 50)
        
        for event in filtered_events:
            print(f"ID: {event['id']} | Name: {event['name']}")
            print(f"Date: {event['date']} | Time: {event['time']}")
            print(f"Society: {event['society']}")
            print("-" * 30)
    else:
        print(f"\nNo events found at {selected_location}")

def sort_by_date():
    """Sort events by date"""
    print("\n" + "="*50)
    print("EVENTS SORTED BY DATE")
    print("="*50)
    
    events = read_events_file()
    
    if not events:
        print("No events found!")
        return
    try:
        sorted_events = sorted(events, key=lambda x: x['date'])
    except:
        print("Error sorting events")
        return
    
    print(f"\nTotal Events: {len(sorted_events)}")
    print("-" * 50)
    
    for event in sorted_events:
        status = get_event_status(event['date'])
        status_text = "Upcoming" if status == "upcoming" else "Ongoing" if status == "ongoing" else "Past"
        
        print(f"\nID: {event['id']} | {status_text}")
        print(f"Name: {event['name']}")
        print(f"Date: {event['date']} | Time: {event['time']}")
        print(f"Location: {event['location']} | Society: {event['society']}")
        print("-" * 30)

# REGISTRATION SYSTEM

def register_for_event(current_user):
    """Register for an event"""
    print("\n" + "="*50)
    print("REGISTER FOR EVENT")
    print("="*50)
    
    events = read_events_file() 
    if not events:
        print("No events available!")
        return
    
    view_all_events()
    try:
        event_id = int(input("\nEnter Event ID to register: ").strip())
    except ValueError:
        print("Invalid ID!")
        return
    
    # Find event
    event_found = None
    for event in events:
        if event['id'] == event_id:
            event_found = event
            break
    
    if not event_found:
        print(f"Event with ID {event_id} not found!")
        return
    
    # Check capacity
    registrations = read_registrations_file()
    event_reg_count = 0
    for reg in registrations:
        if reg.get('event_id') == event_id:
            event_reg_count += 1
    
    if event_reg_count >= event_found['capacity']:
        print(f"\n✗ Event '{event_found['name']}' is full!")
        return
    
    print(f"\nRegistering for: {event_found['name']}")
    print(f"Available spots: {event_found['capacity'] - event_reg_count}")
    
    # Check for duplicate registration
    for reg in registrations:
        if reg.get('event_id') == event_id and reg.get('user_email') == current_user['email']:
            print(f"\n✗ You are already registered for this event!")
            return
    
    # Generate registration ID
    if registrations:
        new_reg_id = max([reg.get('id', 0) for reg in registrations]) + 1
    else:
        new_reg_id = 1
    
    new_registration = {
        "id": new_reg_id,
        "event_id": event_id,
        "user_id": current_user['id'],
        "user_name": current_user['full_name'],
        "user_email": current_user['email'],
        "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    registrations.append(new_registration)
    
    if write_registrations_file(registrations):
        print(f"\n✓ Successfully registered for '{event_found['name']}'!")
        log_action(f"Registered for event ID: {event_id}", current_user['username'])
    else:
        print("\n✗ Error registering")

def cancel_registration(current_user):
    print("\n" + "="*50)
    print("CANCEL REGISTRATION")
    print("="*50)
    
    registrations = read_registrations_file()
    
    if not registrations:
        print("No registrations found!")
        return
    
    # Find user's registrations
    user_registrations = []
    for reg in registrations:
        if reg.get('user_id') == current_user['id']:
            user_registrations.append(reg)
    
    if not user_registrations:
        print(f"\nYou have no registrations!")
        return
    
    print(f"\nYour Registrations:")
    print("-" * 60)
    
    events = read_events_file()
    event_dict = {event['id']: event for event in events}
    
    for reg in user_registrations:
        event = event_dict.get(reg['event_id'], {})
        print(f"Registration ID: {reg['id']}")
        print(f"Event: {event.get('name', 'Unknown')}")
        print(f"Date: {event.get('date', 'Unknown')}")
        print(f"Registered on: {reg.get('registration_date', 'Unknown')}")
        print("-" * 40)
    
    try:
        reg_id = int(input("\nEnter Registration ID to cancel: ").strip())
    except ValueError:
        print("Invalid ID!")
        return

    reg_found = None
    for reg in registrations:
        if reg['id'] == reg_id and reg['user_id'] == current_user['id']:
            reg_found = reg
            break
    
    if not reg_found:
        print(f"\n✗ Registration with ID {reg_id} not found or you don't own it!")
        return
    
    event_name = event_dict.get(reg_found['event_id'], {}).get('name', 'Unknown Event')
    confirm = input(f"Are you sure you want to cancel registration for '{event_name}'? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("Cancellation cancelled")
        return
    
    original_count = len(registrations)
    registrations = [reg for reg in registrations if reg['id'] != reg_id]
    
    if len(registrations) < original_count:
        if write_registrations_file(registrations):
            print("\n✓ Registration cancelled successfully!")
            log_action(f"Cancelled registration ID: {reg_id}", current_user['username'])
        else:
            print("\n✗ Error cancelling registration")
    else:
        print(f"\nRegistration with ID {reg_id} not found!")

def view_event_registrations(current_user):
    """View registrations for a specific event"""
    print("\n" + "="*50)
    print("VIEW EVENT REGISTRATIONS")
    print("="*50)
    
    events = read_events_file()
    
    if not events:
        print("No events found!")
        return
    
    view_all_events()
    
    try:
        event_id = int(input("\nEnter Event ID to view registrations: ").strip())
    except ValueError:
        print("Invalid ID!")
        return
    
    # Find event
    event_found = None
    for event in events:
        if event['id'] == event_id:
            event_found = event
            break
    
    if not event_found:
        print(f"Event with ID {event_id} not found!")
        return
    
    if current_user['role'] != 'admin' and event_found.get('created_by') != current_user['username']:
        print(f"\n✗ You don't have permission to view registrations for this event!")
        return
    
    registrations = read_registrations_file()
    event_registrations = []
    for reg in registrations:
        if reg.get('event_id') == event_id:
            event_registrations.append(reg)
    
    print(f"\nRegistrations for: {event_found['name']}")
    print(f"Total Registrations: {len(event_registrations)}/{event_found['capacity']}")
    print("-" * 60)
    
    if event_registrations:
        for i, reg in enumerate(event_registrations, 1):
            print(f"{i}. {reg['user_name']}")
            print(f"   Email: {reg['user_email']}")
            print(f"   Registered: {reg['registration_date']}")
            print("-" * 40)
    else:
        print("No registrations yet!")

def count_registrations_per_event():
    """Count registrations per event"""
    print("\n" + "="*50)
    print("REGISTRATION COUNTS PER EVENT")
    print("="*50)
    
    events = read_events_file()
    registrations = read_registrations_file()
    if not events:
        print("No events found!")
        return
    
    print("\nEvent Registration Summary:")
    print("-" * 70)
    print(f"{'Event Name':<25} {'Society':<15} {'Registrations':<15} {'Capacity':<10} {'Status':<10}")
    print("-" * 70)
    
    for event in events:
        reg_count = 0
        for reg in registrations:
            if reg.get('event_id') == event['id']:
                reg_count += 1
        
        # Calculate percentage
        if event['capacity'] > 0:
            percentage = (reg_count / event['capacity']) * 100
        else:
            percentage = 0
        
        status = "Full" if reg_count >= event['capacity'] else f"{percentage:.1f}%"
        
        print(f"{event['name'][:25]:<25} {event['society'][:15]:<15} {reg_count:<15} {event['capacity']:<10} {status:<10}")
    
    total_events = len(events)
    total_registrations = len(registrations)
    total_capacity = sum([event['capacity'] for event in events])
    
    print("-" * 70)
    print(f"Total Events: {total_events}")
    print(f"Total Registrations: {total_registrations}")
    print(f"Total Capacity: {total_capacity}")

# ==================== DASHBOARD & SYSTEM

def get_event_status(event_date):
    try:
        current_date = datetime.now().date()
        event_date_obj = datetime.strptime(event_date, "%Y-%m-%d").date()
        
        if event_date_obj < current_date:
            return "past"
        elif event_date_obj == current_date:
            return "ongoing"
        else:
            return "upcoming"
    except:
        return "unknown"

def show_event_status():
    print("\n" + "="*50)
    print("EVENT STATUS SUMMARY")
    print("="*50)
    
    events = read_events_file()
    
    if not events:
        print("No events found!")
        return
    
    upcoming_count = 0
    ongoing_count = 0
    past_count = 0
    
    for event in events:
        status = get_event_status(event['date'])
        if status == "upcoming":
            upcoming_count += 1
        elif status == "ongoing":
            ongoing_count += 1
        elif status == "past":
            past_count += 1
    
    print(f"\nEvent Status Summary:")
    print("-" * 40)
    print(f" Upcoming Events: {upcoming_count}")
    print(f" Ongoing Events: {ongoing_count}")
    print(f" Past Events: {past_count}")
    print(f" Total Events: {len(events)}")
    print("-" * 40)
    
    # Show upcoming events
    if upcoming_count > 0:
        print("\n Upcoming Events:")
        for event in events:
            if get_event_status(event['date']) == "upcoming":
                days_until = (datetime.strptime(event['date'], "%Y-%m-%d").date() - datetime.now().date()).days
                print(f"  • {event['name']} - {event['date']} (in {days_until} days)")

def show_total_events_counter():
    """Show total events counter"""
    events = read_events_file()
    print(f"\nTotal Events in System: {len(events)}")

def show_system_logs(current_user):
    """Show system logs"""
    if current_user['role'] != 'admin':
        print("\n✗ Only administrators can view system logs!")
        return
    
    print("\n" + "="*50)
    print("SYSTEM LOGS")
    print("="*50)
    try:
        if not os.path.exists('system_log.txt'):
            print("No logs found!")
            return
        
        with open('system_log.txt', 'r') as log_file:
            logs = log_file.readlines()
        
        if not logs:
            print("No logs found!")
            return
        
        print(f"Total Log Entries: {len(logs)}")
        print("-" * 60)
        
        for log in logs[-20:]:
            print(log.strip())
    except Exception as e:
        print(f"Error reading logs: {e}")

def show_user_profile(current_user):
    print("\n" + "="*50)
    print("YOUR PROFILE")
    print("="*50)
    
    print(f"Username: {current_user['username']}")
    print(f"Full Name: {current_user['full_name']}")
    print(f"Email: {current_user['email']}")
    print(f"Role: {current_user['role'].title()}")
    print(f"Account Created: {current_user['created_at']}")
    print(f"Status: {'Active' if current_user.get('is_active', True) else 'Inactive'}")

    registrations = read_registrations_file()
    user_reg_count = 0
    for reg in registrations:
        if reg.get('user_id') == current_user['id']:
            user_reg_count += 1
    
    print(f"Event Registrations: {user_reg_count}")
    
    if current_user['role'] in ['admin', 'faculty']:
        events = read_events_file()
        user_events = [e for e in events if e.get('created_by') == current_user['username']]
        print(f"Events Created: {len(user_events)}")

# MENUS

def admin_menu(current_user):
    """Admin menu"""
    while True:
        print("\n" + "="*50)
        print(f"ADMIN DASHBOARD - Welcome, {current_user['full_name']}!")
        print("="*50)
        print("1. Add Event")
        print("2. Update Event")
        print("3. Delete Event")
        print("4. View All Events")
        print("5. Search & Filter Events")
        print("6. Manage Users")
        print("7. View Event Registrations")
        print("8. View System Logs")
        print("9. System Statistics")
        print("10. My Profile")
        print("11. Change Password")
        print("12. Logout")
        
        choice = input("\nEnter your choice (1-12): ").strip()
        
        if choice == '1':
            add_event(current_user)
        elif choice == '2':
            update_event(current_user)
        elif choice == '3':
            delete_event(current_user)
        elif choice == '4':
            view_all_events()
        elif choice == '5':
            search_filter_menu(current_user)
        elif choice == '6':
            admin_manage_users(current_user)
        elif choice == '7':
            view_event_registrations(current_user)
        elif choice == '8':
            show_system_logs(current_user)
        elif choice == '9':
            print("\nSystem Statistics:")
            show_total_events_counter()
            show_event_status()
            count_registrations_per_event()
        elif choice == '10':
            show_user_profile(current_user)
        elif choice == '11':
            change_password(current_user)
        elif choice == '12':
            print(f"\n✓ Logging out {current_user['username']}...")
            log_action("User logged out", current_user['username'])
            break
        else:
            print("Invalid choice! Please enter 1-12")

#Student menu
def student_menu(current_user):
    while True:
        print("\n" + "="*50)
        print(f"STUDENT DASHBOARD - Welcome, {current_user['full_name']}!")
        print("="*50)
        print("1. View All Events")
        print("2. Register for Event")
        print("3. Cancel Registration")
        print("4. Search & Filter Events")
        print("5. My Registrations")
        print("6. My Profile")
        print("7. Change Password")
        print("8. Logout")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        if choice == '1':
            view_all_events()
        elif choice == '2':
            register_for_event(current_user)
        elif choice == '3':
            cancel_registration(current_user)
        elif choice == '4':
            search_filter_menu(current_user)
        elif choice == '5':
            registrations = read_registrations_file()
            user_regs = [r for r in registrations if r.get('user_id') == current_user['id']]
            
            if user_regs:
                print(f"\nYour Registrations ({len(user_regs)}):")
                print("-" * 50)
                
                events = read_events_file()
                event_dict = {event['id']: event for event in events}
                
                for i, reg in enumerate(user_regs, 1):
                    event = event_dict.get(reg['event_id'], {})
                    print(f"{i}. {event.get('name', 'Unknown Event')}")
                    print(f"   Date: {event.get('date', 'Unknown')}")
                    print(f"   Registered: {reg.get('registration_date', 'Unknown')}")
                    print("-" * 30)
            else:
                print("\nYou have no registrations.")
        elif choice == '6':
            show_user_profile(current_user)
        elif choice == '7':
            change_password(current_user)
        elif choice == '8':
            print(f"\n✓ Logging out {current_user['username']}...")
            log_action("User logged out", current_user['username'])
            break
        else:
            print("Invalid choice! Please enter 1-8")

def faculty_menu(current_user):
    """Faculty menu"""
    while True:
        print("\n" + "="*50)
        print(f"FACULTY DASHBOARD - Welcome, {current_user['full_name']}!")
        print("="*50)
        print("1. Add Event")
        print("2. Update My Events")
        print("3. View All Events")
        print("4. Register for Event")
        print("5. Cancel Registration")
        print("6. Search & Filter Events")
        print("7. View My Event Registrations")
        print("8. My Profile")
        print("9. Change Password")
        print("10. Logout")
        
        choice = input("\nEnter your choice (1-10): ").strip()
        
        if choice == '1':
            add_event(current_user)
        elif choice == '2':
            update_event(current_user)
        elif choice == '3':
            view_all_events()
        elif choice == '4':
            register_for_event(current_user)
        elif choice == '5':
            cancel_registration(current_user)
        elif choice == '6':
            search_filter_menu(current_user)
        elif choice == '7':
            events = read_events_file()
            faculty_events = [e for e in events if e.get('created_by') == current_user['username']]
            
            if faculty_events:
                print(f"\nEvents Created by You:")
                for event in faculty_events:
                    print(f"ID: {event['id']} - {event['name']}")
                
                try:
                    event_id = int(input("\nEnter Event ID to view registrations: ").strip())
                    # Verify ownership
                    event_found = None
                    for event in faculty_events:
                        if event['id'] == event_id:
                            event_found = event
                            break
                    
                    if event_found:
                        # Call view registrations with permission check bypass
                        temp_user = current_user.copy()
                        view_event_registrations(temp_user)
                    else:
                        print(f"\n✗ You don't own event with ID {event_id}")
                except ValueError:
                    print("Invalid ID!")
            else:
                print("\nYou haven't created any events yet.")
        elif choice == '8':
            show_user_profile(current_user)
        elif choice == '9':
            change_password(current_user)
        elif choice == '10':
            print(f"\n✓ Logging out {current_user['username']}...")
            log_action("User logged out", current_user['username'])
            break
        else:
            print("Invalid choice! Please enter 1-10")

def search_filter_menu(current_user):
    while True:
        print("\n" + "="*50)
        print("SEARCH & FILTER EVENTS")
        print("="*50)
        print("1. Search by Name")
        print("2. Search by Date")
        print("3. Filter Upcoming Events")
        print("4. Filter by Location")
        print("5. Sort by Date")
        print("6. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            search_by_name()
        elif choice == '2':
            search_by_date()
        elif choice == '3':
            filter_upcoming_events()
        elif choice == '4':
            filter_by_location()
        elif choice == '5':
            sort_by_date()
        elif choice == '6':
            break
        else:
            print("Invalid choice! Please enter 1-6")

# MAIN PROGRAM

def main():

    print("="*60)
    print("EVENT MANAGEMENT SYSTEM WITH USER AUTHENTICATION")
    print("File-Based CRUD Application")
    print("="*60)
    
    # Initialize files
    read_users_file()  # Creates default admin if admin doesn't exist
    read_events_file()  # Create pre loaded events
    read_registrations_file()  # Creates Registrations file
    
    print("\n✓ System initialized successfully!")
    
    while True:
        print("\n" + "="*50)
        print("MAIN MENU")
        print("="*50)
        print("1. Login")
        print("2. Register as New User")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            current_user = user_login()
            
            if current_user:
                #Menu Based on Role
                if current_user['role'] == 'admin':
                    admin_menu(current_user)
                elif current_user['role'] == 'faculty':
                    faculty_menu(current_user)
                else:  #Student Menu
                    student_menu(current_user)
        
        elif choice == '2':
            new_user = user_registration()
            if new_user:
                print("\nPlease login with your new credentials.")
        
        elif choice == '3':
            print("\nThank you for using Event Management System!")
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Please enter 1-3")

# RUN PROGRAM
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()