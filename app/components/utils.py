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
    except ValueError as e:
        print(f"Invalid hashed format: {hashed}. Error: {e}")
        return False
    
def update_user_password(user_id, new_password):
    """Update a user's password in the database."""
    if len(new_password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    conn = get_db_connection()
    cursor = conn.cursor()
    # Hash the new password
    new_password_hash = hash_password(new_password)
    # Update the password in the database
    cursor.execute(
        """
        UPDATE users
        SET password_hash = ?
        WHERE id = ?
        """,
        (new_password_hash, user_id)
    )
    conn.commit()
    conn.close()
    print(f"Password updated successfully for user_id {user_id}.")


def authenticate_user(email, password):
    """Authenticates a user by email and password."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve the user record and their roles by email
    query = """
    SELECT u.id, u.username, u.email, u.password_hash, r.role
    FROM users u
    LEFT JOIN user_roles ur ON u.id = ur.user_id
    LEFT JOIN roles r ON ur.role_id = r.id
    WHERE u.email = ?
    """
    cursor.execute(query, (email,))
    rows = cursor.fetchall()
    conn.close()

    # If no user is found, return None
    if not rows:
        return None

    # Extract the user's data (assumes user data is consistent across rows)
    user_data = {
        "id": rows[0]["id"],
        "username": rows[0]["username"],
        "email": rows[0]["email"],
        "password_hash": rows[0]["password_hash"],
        "roles": [row["role"] for row in rows if row["role"]]  # Collect all roles
    }

    # Verify the password
    if verify_password(password, user_data["password_hash"]):
        # Remove the password_hash before returning user data for security reasons
        user_data.pop("password_hash")
        return user_data
    else:
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

def delete_user_account(user_id):
    """Delete a user's account from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Delete the user account
    cursor.execute(
        """
        DELETE FROM users
        WHERE id = ?
        """,
        (user_id,)
    )
    conn.commit()
    conn.close()
    print(f"User account with user_id {user_id} deleted successfully.")


