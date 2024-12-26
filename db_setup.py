import sqlite3

DATABASE_PATH = "database.db"  # Path to your SQLite database file

def get_db_connection():
    """Create and return a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable accessing columns by name
    return conn

def create_tables():
    """Create all necessary tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
   
    )
    """)
    # Roles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL
    )
    """)
    
    # User Roles Table (Junction Table)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_roles (
        user_id INTEGER NOT NULL,
        role_id INTEGER NOT NULL,
        PRIMARY KEY (user_id, role_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
    )
    """)
                

    # Renter Profiles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS renter_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        profile_pic BLOB DEFAULT NULL,
        name TEXT DEFAULT NULL,
        tagline TEXT DEFAULT NULL,
        age INTEGER CHECK (age >= 18) DEFAULT 18,
        phone TEXT CHECK (phone GLOB '+[0-9]*' OR (phone GLOB '[0-9]*' AND length(phone) = 10)), 
        nationality TEXT DEFAULT NULL,
        occupation TEXT DEFAULT NULL,
        contract_type TEXT DEFAULT NULL,
        income REAL CHECK (income >= 0) DEFAULT 0,
        work_mode TEXT DEFAULT NULL,
        bio TEXT DEFAULT NULL,
        hobbies TEXT DEFAULT NULL,
        social_media TEXT DEFAULT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    
    # Add UNIQUE index to user_id if it doesn't exist 
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS unique_user_id ON renter_profiles (user_id);
    """)
    
    # Agent Profiles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        agent_profile_pic BLOB DEFAULT NULL,
        name TEXT DEFAULT NULL,
        phone TEXT CHECK (phone GLOB '+[0-9]*' OR (phone GLOB '[0-9]*' AND length(phone) = 10)),
        agency_name TEXT DEFAULT NULL,
        agency_address TEXT DEFAULT NULL,
        agency_website TEXT DEFAULT NULL,
        social_media TEXT DEFAULT NULL,
        working_days TEXT DEFAULT NULL,
        working_hours TEXT DEFAULT NULL,
        preferred_communication TEXT DEFAULT NULL,
        services TEXT DEFAULT NULL,     
        languages TEXT DEFAULT NULL,
        mission_statement TEXT DEFAULT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE   
    )
    """)
    
    # Add UNIQUE index to user_id if it doesn't exist
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS unique_user_id ON agent_profiles (user_id);
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
        pets BOOLEAN,
        pet_type TEXT,
        FOREIGN KEY (profile_id) REFERENCES renter_profiles(id) ON DELETE CASCADE
    )
    """)

    # # Add UNIQUE index to profile_id if it doesn't exist
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS unique_profile_id ON rental_preferences (profile_id);
    """)
    
    # Updated Renter Credit Score Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS renter_credit_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT CHECK (status IN ('Not Verified', 'Pending', 'Verified')) DEFAULT 'Not Verified',
        authorized BOOLEAN DEFAULT 0, -- 0 for False, 1 for True
        uploaded_file BOOLEAN DEFAULT 0, -- 0 for False, 1 for True
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()
    print("All tables created successfully.")
    


if __name__ == "__main__":
    create_tables()


# # def reinitialize_database():
# #     """Reinitialize the database by dropping and recreating all tables."""
# #     drop_tables()
# #     create_tables()
    
# def check_rental_preferences_schema():
#     """
#     Check the schema of the rental_preferences table and confirm if profile_id is UNIQUE.
#     """
#     conn = sqlite3.connect(DATABASE_PATH)
#     cursor = conn.cursor()

#     try:
#         # Check the schema of the rental_preferences table
#         cursor.execute("PRAGMA table_info(rental_preferences);")
#         table_info = cursor.fetchall()

#         print("Schema of rental_preferences table:")
#         print("cid | Name           | Type      | NotNull | Default | PK")
#         print("-------------------------------------------------------")
#         for column in table_info:
#             print(column)

#         # Check for UNIQUE constraints or indexes
#         cursor.execute("PRAGMA index_list(rental_preferences);")
#         indexes = cursor.fetchall()

#         print("\nIndexes on rental_preferences table:")
#         print("Index Name      | Unique")
#         print("----------------|--------")
#         for index in indexes:
#             print(f"{index[1]} | {'Yes' if index[2] else 'No'}")  # Access tuple elements by index

#     except sqlite3.Error as e:
#         print(f"Error checking schema: {e}")

#     finally:
#         conn.close()


# if __name__ == "__main__":
#     print("Reinitializing database...")
#     check_rental_preferences_schema()

