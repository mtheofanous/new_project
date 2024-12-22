import hashlib
import uuid

# Mock database for users
database = {
    "users": []  # List of user dictionaries with keys: id, username, email, password_hash, role
}

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
    for user in database["users"]:
        if user["email"] == email and verify_password(password, user["password_hash"]):
            return user  # Return user record if authentication succeeds
    return None

def add_user(username, email, password, role):
    """Adds a new user to the mock database."""
    # Check if email already exists
    for user in database["users"]:
        if user["email"] == email:
            return None  # Email already exists

    user_id = str(uuid.uuid4())
    password_hash = hash_password(password)
    new_user = {
        "id": user_id,
        "username": username,
        "email": email,
        "password_hash": password_hash,
        "role": role
    }
    database["users"].append(new_user)
    return user_id  # Return the new user's ID
