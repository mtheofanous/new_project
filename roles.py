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
    if not role_name or role_name.strip() == "":
        raise ValueError("Invalid role name. Role name cannot be empty or None.")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Ensure the role exists in the roles table
        cursor.execute("SELECT id FROM roles WHERE role = ?", (role_name,))
        role = cursor.fetchone()

        if role:
            role_id = role["id"]
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

    except sqlite3.IntegrityError as e:
        print(f"Database integrity error: {e}")
        raise

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
    if not role_name or role_name.strip() == "":
        raise ValueError("Invalid role name. Role name cannot be empty or None.")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Ensure the role exists in the roles table
        cursor.execute("SELECT id FROM roles WHERE role = ?", (role_name,))
        role = cursor.fetchone()

        if not role:
            raise ValueError(f"Role '{role_name}' does not exist in the database.")

        role_id = role["id"]

        # Delete the user-role relationship for the specific user and role
        cursor.execute("""
        DELETE FROM user_roles
        WHERE user_id = ? AND role_id = ?
        """, (user_id, role_id))

        # Commit the changes
        conn.commit()

        # Verify that only one role was deleted
        if cursor.rowcount == 0:
            print(f"No role '{role_name}' found for user_id {user_id}.")
        elif cursor.rowcount > 1:
            print(f"Warning: Multiple rows deleted for user_id {user_id} and role '{role_name}'.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise

    finally:
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
