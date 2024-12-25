import sqlite3
from db_setup import get_db_connection

def add_role(role_name):
    """Add a new role to the roles table."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO roles (role) VALUES (?)", (role_name,))
        conn.commit()
    except sqlite3.IntegrityError:
        # Role already exists
        print(f"Role '{role_name}' already exists.")
    finally:
        conn.close()

def assign_role_to_user(user_id, role_name):
    """Assign a specific role to a user."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Ensure the role exists in the roles table
        cursor.execute("SELECT id FROM roles WHERE role = ?", (role_name,))
        role = cursor.fetchone()

        if role:
            role_id = role['id']
        else:
            # If the role doesn't exist, insert it
            cursor.execute("INSERT INTO roles (role) VALUES (?)", (role_name,))
            role_id = cursor.lastrowid

        # Insert the user-role relationship into user_roles table
        cursor.execute("""
        INSERT OR IGNORE INTO user_roles (user_id, role_id) 
        VALUES (?, ?)
        """, (user_id, role_id))

        conn.commit()

    finally:
        conn.close()

def get_user_roles(user_id):
    """Retrieve all roles assigned to a user."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT r.role
    FROM roles r
    JOIN user_roles ur ON r.id = ur.role_id
    WHERE ur.user_id = ?
    """, (user_id,))

    roles = [row['role'] for row in cursor.fetchall()]
    conn.close()
    return roles

def remove_role_from_user(user_id, role_name):
    """Remove a specific role from a user."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM user_roles 
    WHERE user_id = ? AND role_id = (
        SELECT id FROM roles WHERE role = ?
    )
    """, (user_id, role_name))

    conn.commit()
    conn.close()

def get_users_with_role(role_name):
    """Retrieve all users with a specific role."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT u.username, u.email
    FROM users u
    JOIN user_roles ur ON u.id = ur.user_id
    JOIN roles r ON r.id = ur.role_id
    WHERE r.role = ?
    """, (role_name,))

    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users
