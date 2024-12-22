import hashlib
import uuid
from db_setup import get_db_connection


def hash_password(password):
    """Hashes a password for secure storage."""
    salt = uuid.uuid4().hex
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{hashed}${salt}"


def verify_password(password, hashed):
    """Verifies a password against a stored hash."""
    try:
        hash_part, salt = hashed.split('$')
        return hashlib.sha256((password + salt).encode()).hexdigest() == hash_part
    except ValueError:
        return False


def authenticate_user(email, password):
    """Authenticates a user by email and password."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve the user record by email
    cursor.execute("SELECT id, username, email, password_hash, role FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    # If user exists and password matches, return user data
    if user and verify_password(password, user["password_hash"]):
        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
        }

    # If authentication fails, return None
    return None


def add_user(username, email, password, role):
    """Adds a new user to the SQLite database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if email already exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return None  # Email already exists

    # Hash the password
    password_hash = hash_password(password)

    # Insert new user into the database
    cursor.execute("""
    INSERT INTO users (username, email, password_hash, role)
    VALUES (?, ?, ?, ?)
    """, (username, email, password_hash, role))

    # Commit the transaction and retrieve the new user ID
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return user_id  # Return the new user's ID
