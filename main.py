# ------------------------------------------------------------
# Appointment Booking and Reminder System
# Name    : Pritam Hira
# Roll No : 25/SCA/BCOA/057
# Course  : BCA - Python Mini Project
# ------------------------------------------------------------
# This program lets a user:
#   1. Book an appointment
#   2. View all appointments
#   3. Cancel an appointment
#   4. See reminders (today and tomorrow)
#   5. Search appointments by name
#   6. Exit
# All appointments are saved in a file called appointments.json
# so the data is not lost when the program is closed.
# ------------------------------------------------------------

import json                                  # to save and load data
import os                                    # to check if file exists
from datetime import datetime, date, timedelta   # to work with dates

FILE_NAME = "appointments.json"


# ---------- File handling ----------

def load_appointments():
    """Read all appointments from the file. If file is missing, return empty list."""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []


def save_appointments(appointments):
    """Write all appointments into the file."""
    with open(FILE_NAME, "w") as file:
        json.dump(appointments, file, indent=4)


# ---------- Helper functions ----------

def is_valid_date(text):
    """Check that date is in DD-MM-YYYY format."""
    try:
        datetime.strptime(text, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def is_valid_time(text):
    """Check that time is in HH:MM (24 hour) format."""
    try:
        datetime.strptime(text, "%H:%M")
        return True
    except ValueError:
        return False


def get_next_id(appointments):
    """Give every appointment a new unique number."""
    if len(appointments) == 0:
        return 1
    return appointments[-1]["id"] + 1


def print_appointment(a):
    """Print one appointment in a neat line."""
    print(f"ID: {a['id']} | {a['name']} | Phone: {a['phone']} | "
          f"Purpose: {a['purpose']} | Date: {a['date']} | Time: {a['time']}")


# ---------- Main features ----------

def book_appointment(appointments):
    print("\n--- Book New Appointment ---")
    name = input("Enter your name: ").strip()
    phone = input("Enter phone number: ").strip()
    purpose = input("Enter purpose (e.g. Doctor, Salon, Meeting): ").strip()
    appt_date = input("Enter date (DD-MM-YYYY): ").strip()
    appt_time = input("Enter time (HH:MM, 24 hour): ").strip()

    # Check that nothing is empty
    if name == "" or phone == "" or purpose == "":
        print("Error: Name, phone and purpose cannot be empty.")
        return

    # Check phone number
    if not (phone.isdigit() and len(phone) == 10):
        print("Error: Phone number must be exactly 10 digits.")
        return

    # Check date and time format
    if not is_valid_date(appt_date):
        print("Error: Invalid date. Use DD-MM-YYYY format.")
        return
    if not is_valid_time(appt_time):
        print("Error: Invalid time. Use HH:MM format.")
        return

    # Do not allow booking in the past
    chosen = datetime.strptime(appt_date, "%d-%m-%Y").date()
    if chosen < date.today():
        print("Error: You cannot book an appointment in the past.")
        return

    # Do not allow two appointments at the same date and time
    for a in appointments:
        if a["date"] == appt_date and a["time"] == appt_time:
            print("Error: This time slot is already booked. Please choose another.")
            return

    # Everything is fine, so save the appointment
    new_appointment = {
        "id": get_next_id(appointments),
        "name": name,
        "phone": phone,
        "purpose": purpose,
        "date": appt_date,
        "time": appt_time
    }
    appointments.append(new_appointment)
    save_appointments(appointments)
    print(f"Appointment booked successfully! Your appointment ID is {new_appointment['id']}.")


def view_appointments(appointments):
    print("\n--- All Appointments ---")
    if len(appointments) == 0:
        print("No appointments found.")
        return
    for a in appointments:
        print_appointment(a)


def cancel_appointment(appointments):
    print("\n--- Cancel Appointment ---")
    if len(appointments) == 0:
        print("No appointments to cancel.")
        return

    try:
        appt_id = int(input("Enter the appointment ID to cancel: "))
    except ValueError:
        print("Error: ID must be a number.")
        return

    for a in appointments:
        if a["id"] == appt_id:
            appointments.remove(a)
            save_appointments(appointments)
            print("Appointment cancelled successfully.")
            return
    print("Error: No appointment found with that ID.")


def show_reminders(appointments):
    print("\n--- Reminders ---")
    today = date.today().strftime("%d-%m-%Y")
    tomorrow = (date.today() + timedelta(days=1)).strftime("%d-%m-%Y")

    found = False
    for a in appointments:
        if a["date"] == today:
            print(f"REMINDER (TODAY): {a['name']} has {a['purpose']} at {a['time']}")
            found = True
        elif a["date"] == tomorrow:
            print(f"REMINDER (TOMORROW): {a['name']} has {a['purpose']} at {a['time']}")
            found = True

    if not found:
        print("No appointments today or tomorrow.")


def search_appointment(appointments):
    print("\n--- Search Appointment ---")
    keyword = input("Enter name to search: ").strip().lower()

    found = False
    for a in appointments:
        if keyword in a["name"].lower():
            print_appointment(a)
            found = True

    if not found:
        print("No appointment found for that name.")


# ---------- Main program ----------

def main():
    appointments = load_appointments()

    # Show reminders automatically when the program starts
    print("=" * 50)
    print("   APPOINTMENT BOOKING AND REMINDER SYSTEM")
    print("=" * 50)
    show_reminders(appointments)

    while True:
        print("\n========== MENU ==========")
        print("1. Book Appointment")
        print("2. View All Appointments")
        print("3. Cancel Appointment")
        print("4. Show Reminders")
        print("5. Search by Name")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            book_appointment(appointments)
        elif choice == "2":
            view_appointments(appointments)
        elif choice == "3":
            cancel_appointment(appointments)
        elif choice == "4":
            show_reminders(appointments)
        elif choice == "5":
            search_appointment(appointments)
        elif choice == "6":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


main()
