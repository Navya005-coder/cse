
import sqlite3
import getpass

# Database connection
conn = sqlite3.connect("railway.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT)''')
                
cursor.execute('''CREATE TABLE IF NOT EXISTS trains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                source TEXT,
                destination TEXT,
                seats INTEGER)''')
                
cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT,
                train_id INTEGER,
                seats_booked INTEGER,
                FOREIGN KEY(train_id) REFERENCES trains(id))''')
conn.commit()

# User Registration
def register():
    username = input("Enter a username: ")
    password = getpass.getpass("Enter a password: ")
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Registration Successful!")
    except sqlite3.IntegrityError:
        print("Username already exists!")

# User Login
def login():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    if user:
        print("Login Successful!")
        return username
    else:
        print("Invalid credentials!")
        return None

# View Available Trains
def view_trains():
    cursor.execute("SELECT * FROM trains")
    trains = cursor.fetchall()
    if not trains:
        print("No trains available!")
    else:
        print("Available Trains:")
        for train in trains:
            print(f"ID: {train[0]}, Name: {train[1]}, From: {train[2]}, To: {train[3]}, Seats: {train[4]}")

# Book Ticket
def book_ticket(username):
    view_trains()
    train_id = int(input("Enter Train ID: "))
    seats = int(input("Enter number of seats to book: "))
    cursor.execute("SELECT seats FROM trains WHERE id=?", (train_id,))
    train = cursor.fetchone()
    if train and train[0] >= seats:
        cursor.execute("UPDATE trains SET seats=seats-? WHERE id=?", (seats, train_id))
        cursor.execute("INSERT INTO bookings (user, train_id, seats_booked) VALUES (?, ?, ?)", (username, train_id, seats))
        conn.commit()
        print("Booking Successful!")
    else:
        print("Not enough seats available!")

# Cancel Ticket
def cancel_ticket(username):
    cursor.execute("SELECT * FROM bookings WHERE user=?", (username,))
    bookings = cursor.fetchall()
    if not bookings:
        print("No bookings found!")
        return
    for booking in bookings:
        print(f"Booking ID: {booking[0]}, Train ID: {booking[2]}, Seats: {booking[3]}")
    booking_id = int(input("Enter Booking ID to cancel: "))
    cursor.execute("SELECT train_id, seats_booked FROM bookings WHERE id=?", (booking_id,))
    booking = cursor.fetchone()
    if booking:
        cursor.execute("UPDATE trains SET seats=seats+? WHERE id=?", (booking[1], booking[0]))
        cursor.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
        conn.commit()
        print("Booking Cancelled!")
    else:
        print("Invalid Booking ID!")

# Admin - Add Train
def add_train():
    name = input("Enter train name: ")
    source = input("Enter source station: ")
    destination = input("Enter destination station: ")
    seats = int(input("Enter number of seats: "))
    cursor.execute("INSERT INTO trains (name, source, destination, seats) VALUES (?, ?, ?, ?)", (name, source, destination, seats))
    conn.commit()
    print("Train Added Successfully!")

# Main Menu
def main():
    while True:
        print("\n1. Register\n2. Login\n3. Admin - Add Train\n4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            register()
        elif choice == '2':
            user = login()
            if user:
                while True:
                    print("\n1. View Trains\n2. Book Ticket\n3. Cancel Ticket\n4. Logout")
                    user_choice = input("Enter choice: ")
                    if user_choice == '1':
                        view_trains()
                    elif user_choice == '2':
                        book_ticket(user)
                    elif user_choice == '3':
                        cancel_ticket(user)
                    elif user_choice == '4':
                        break
        elif choice == '3':
            add_train()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()

# Close connection
conn.close()
