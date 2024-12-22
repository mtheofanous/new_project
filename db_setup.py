import sqlite3

DATABASE_PATH = "database.db"

def get_db_connection():
    """Create and return a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable accessing columns by name
    return conn

def create_tables():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # Renter Profiles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS renter_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_pic BLOB,
        email TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        name TEXT,
        tagline TEXT,
        age INTEGER CHECK (age >= 18),
        phone TEXT,
        nationality TEXT,
        occupation TEXT,
        contract_type TEXT,
        income REAL,
        work_mode TEXT,
        bio TEXT,
        hobbies TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # Rental Preferences Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rental_preferences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_id INTEGER NOT NULL,
        preferred_city TEXT,
        preferred_area TEXT,
        budget_min REAL,
        budget_max REAL,
        property_type TEXT,
        rooms_needed INTEGER,
        number_of_people INTEGER,
        move_in_date DATE,
        lease_duration TEXT,
        pets BOOLEAN,
        pet_type TEXT,
        FOREIGN KEY (profile_id) REFERENCES renter_profiles(id) ON DELETE CASCADE
    )
    """)

    # Credit Scores Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credit_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_id INTEGER NOT NULL,
        credit_score_verified BOOLEAN DEFAULT FALSE,
        uploaded_document BLOB,
        FOREIGN KEY (profile_id) REFERENCES renter_profiles(id) ON DELETE CASCADE
    )
    """)

    # Landlord Recommendations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS landlord_recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        renter_id INTEGER NOT NULL,
        landlord_name TEXT,
        landlord_email TEXT,
        landlord_phone TEXT,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY (renter_id) REFERENCES renter_profiles(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
