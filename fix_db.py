import sqlite3
import os

db_path = os.path.join('instance', 'shrikrishna_real_estate.db')

if not os.path.exists(db_path):
    # Try root if not in instance
    db_path = 'shrikrishna_real_estate.db'

print(f"Connecting to database at: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Add user_id column to properties table
    try:
        cursor.execute("ALTER TABLE properties ADD COLUMN user_id INTEGER REFERENCES users(id)")
        print("Added 'user_id' column to 'properties' table.")
    except sqlite3.OperationalError as e:
        print(f"Skipping 'user_id': {e}")

    # 2. Add is_public column to properties table
    try:
        cursor.execute("ALTER TABLE properties ADD COLUMN is_public BOOLEAN DEFAULT 1")
        print("Added 'is_public' column to 'properties' table.")
    except sqlite3.OperationalError as e:
        print(f"Skipping 'is_public': {e}")

    # 3. Add role column to users table
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'Buyer'")
        print("Added 'role' column to 'users' table.")
    except sqlite3.OperationalError as e:
        print(f"Skipping 'role': {e}")

    conn.commit()
    conn.close()
    print("Database schema updated successfully!")

except Exception as e:
    print(f"Error updating database: {e}")
