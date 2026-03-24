import os
import urllib.parse
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fix_supabase_schema():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("Error: DATABASE_URL not found in .env")
        return

    # Handle password encoding (same logic as config.py)
    if db_url.startswith("postgresql://") and ":" in db_url and "@" in db_url:
        prefix, rest = db_url.split("://", 1)
        user_pass, host_db = rest.rsplit("@", 1)
        if ":" in user_pass:
            user, password = user_pass.split(":", 1)
            encoded_password = urllib.parse.quote_plus(password)
            db_url = f"{prefix}://{user}:{encoded_password}@{host_db}"

    print(f"Connecting to Supabase...")
    engine = create_engine(db_url)

    try:
        with engine.connect() as conn:
            print("Successfully connected. Applying fixes...")
            
            # 1. Force password_hash to TEXT
            print("Updating 'password_hash' column in 'users' table...")
            conn.execute(text("ALTER TABLE users ALTER COLUMN password_hash TYPE TEXT"))
            
            # 2. Update role to 50 chars just in case
            print("Updating 'role' column in 'users' table...")
            conn.execute(text("ALTER TABLE users ALTER COLUMN role TYPE VARCHAR(50)"))
            
            # 3. Add missing columns if they don't exist
            print("Checking for other missing columns...")
            try:
                conn.execute(text("ALTER TABLE properties ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id)"))
            except Exception: pass
            
            try:
                conn.execute(text("ALTER TABLE properties ADD COLUMN IF NOT EXISTS is_public BOOLEAN DEFAULT TRUE"))
            except Exception: pass

            conn.commit()
            print("\nSUCCESS: Supabase schema updated successfully!")
            print("You can now register users without any truncation errors.")

    except Exception as e:
        print(f"\nERROR: Failed to update Supabase: {e}")

if __name__ == '__main__':
    fix_supabase_schema()
