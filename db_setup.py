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
        first_name TEXT DEFAULT NULL,
        last_name TEXT DEFAULT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_logout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    # Roles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL UNIQUE
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
        profile_pic BLOB,
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE   
    )
    """)
    
    # Add UNIQUE index to user_id if it doesn't exist
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS unique_user_id ON agent_profiles (user_id);
    """)
    
#   Landlord Profiles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS landlord_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        profile_pic BLOB DEFAULT NULL,
        phone TEXT CHECK (phone GLOB '+[0-9]*' OR (phone GLOB '[0-9]*' AND length(phone) = 10)),
        social_media TEXT DEFAULT NULL,
        preferred_communication TEXT DEFAULT NULL,
        languages TEXT DEFAULT NULL,
        about_me TEXT DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    
# property interest table       
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS property_interest (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        status TEXT DEFAULT 'Pending',
        status_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        interest_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(property_id, user_id),
        FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # Add a trigger to keep track of the number of interested users per property
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS update_interest_count
    AFTER INSERT ON property_interest
    BEGIN
        UPDATE properties
        SET interest_count = COALESCE(interest_count, 0) + 1
        WHERE id = NEW.property_id;
    END;
    """)
    
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS decrement_interest_count
    AFTER DELETE ON property_interest
    BEGIN
        UPDATE properties
        SET interest_count = interest_count - 1
        WHERE id = OLD.property_id;
    END;
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
        property_size_min REAL,
        property_size_max REAL,
        bedrooms INTEGER,
        bathrooms INTEGER,
        floor INTEGER,
        number_of_people INTEGER,
        move_in_date DATE,
        pets BOOLEAN,
        pet_type TEXT,
        lease_duration TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (profile_id) REFERENCES renter_profiles(id) ON DELETE CASCADE
    )
    """)

    # # Add UNIQUE index to profile_id if it doesn't exist
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS unique_profile_id ON rental_preferences (profile_id);
    """)
    
    # Renter Credit Score Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS renter_credit_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,        -- Unique identifier for each credit score record
        user_id INTEGER NOT NULL,                    -- The ID of the renter
        status TEXT DEFAULT 'Not Verified',               -- Status of the credit score: 'Pending', 'Verified', 'Not Verified'
        score INTEGER,                               -- Numeric credit score, if available
        authorized BOOLEAN DEFAULT 0,                -- Whether the renter authorized a credit check
        uploaded_file BLOB,                          -- Uploaded credit score file (if applicable), stored as binary
        request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When the credit score was requested
        verification_timestamp TIMESTAMP,            -- When the credit score was verified
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE, -- Link to users table
        UNIQUE (user_id)                             -- Ensure one credit score entry per renter
    )
    """)
    
    
    # Add UNIQUE index to user_id if it doesn't exist
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS unique_user_id ON renter_credit_scores (user_id);
    """)
    
    # Properties Table (if not already created)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        friendly_name TEXT,
        property_type TEXT NOT NULL,
        property_size REAL NOT NULL,
        property_location TEXT NOT NULL,
        property_price REAL NOT NULL,
        price_per_sqm REAL,
        bedrooms INTEGER,
        bathrooms INTEGER,
        floor INTEGER,
        year_built INTEGER,
        condition TEXT,
        renovation_year INTEGER,
        energy_class TEXT,
        availability TEXT,
        available_from TEXT,
        heating_method TEXT,
        interest_count INTEGER DEFAULT 0,
        zone TEXT,
        creation_method TEXT CHECK (creation_method IN ('manual', 'url')) NOT NULL DEFAULT 'manual',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(property_location, property_size, property_type, floor, bedrooms, user_id) -- Composite unique constraint
    )
    """)
    
    # Increment Interest Count Trigger
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS increment_interest_count
    AFTER INSERT ON property_interest
    BEGIN
        UPDATE properties
        SET interest_count = COALESCE(interest_count, 0) + 1
        WHERE id = NEW.property_id;
    END;
    """)

    # Decrement Interest Count Trigger
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS decrement_interest_count
    AFTER DELETE ON property_interest
    BEGIN
        UPDATE properties
        SET interest_count = interest_count - 1
        WHERE id = OLD.property_id;
    END;
    """)

    
    # property images table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS property_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        image_src TEXT DEFAULT NULL,
        image_blob BLOB DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # Relationship Table: Property Ownership
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS property_ownership (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        role TEXT CHECK (role IN ('landlord', 'agent')) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE(property_id, user_id, role) -- Prevent duplicate ownership records
    )
    """)


    # Favorites Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,  -- The user marking the favorite
        favorite_type TEXT CHECK (favorite_type IN ('renter', 'landlord', 'agent', 'property')) NOT NULL,  -- Type of the favorite
        favorite_id INTEGER NOT NULL,  -- ID of the renter, landlord, agent, or property
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp when the favorite was added
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,  -- User who is adding the favorite
        UNIQUE (user_id, favorite_type, favorite_id)  -- Prevents duplicate favorites for the same user
    )
    """)

    conn.commit()
    conn.close()
    print("Favorites table created successfully.")
    


if __name__ == "__main__":
    create_tables()



