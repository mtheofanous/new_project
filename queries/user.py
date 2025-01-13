from db_setup import get_db_connection
from app.components.utils import hash_password  # Assuming you have the hash_password function in utils.py
import sqlite3
import streamlit as st
import json


def save_user_to_db(username, first_name, last_name, email, password):
    """
    Save a new user to the database.
    :param username: The user's username.
    :param email: The user's email address.
    :param password: The user's password.
    :return: The ID of the newly created user.
    
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Hash the password for security
    hashed_password = hash_password(password)

    try:
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            raise ValueError("Email already exists. Please use a different email.")

        # Insert the new user
        cursor.execute("""
        INSERT INTO users (username, first_name, last_name, email, password_hash)
        VALUES (?, ?, ?, ?, ?)
        """, (username, first_name, last_name, email, hashed_password))

        conn.commit()
        
        return cursor.lastrowid  # Return the user ID of the new user

    except sqlite3.IntegrityError as e:
        raise ValueError("A user with this email already exists.") from e
    except sqlite3.Error as e:
        raise ValueError(f"Database error: {e}")

    finally:
        conn.close()
        
# Update the username for a specific user
def update_username(user_id, new_username):
    """
    Update the username for a specific user.
    :param user_id: The ID of the user.
    :param new_username: The new username.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        UPDATE users
        SET username = ?
        WHERE id = ?
        """, (new_username, user_id))
        
        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Database error while updating username: {e}")
    finally:
        conn.close()
        
# Update the email for a specific user
def update_email(user_id, new_email):
    """
    Update the email for a specific user.
    :param user_id: The ID of the user.
    :param new_email: The new email.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Ensure the new email is not already in use
        cursor.execute("SELECT id FROM users WHERE email = ?", (new_email,))
        if cursor.fetchone():
            raise ValueError("Email already exists. Please use a different email.")

        cursor.execute("""
        UPDATE users
        SET email = ?
        WHERE id = ?
        """, (new_email, user_id))
        
        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Database error while updating email: {e}")
    finally:
        conn.close()
        
# Update the first name and last name for a specific user

def update_user_name(user_id, new_first_name, new_last_name):
    """
    Update the first name and last name for a specific user.
    :param user_id: The ID of the user.
    :param new_first_name: The new first name.
    :param new_last_name: The new last name.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        UPDATE users
        SET first_name = ?, last_name = ?
        WHERE id = ?
        """, (new_first_name, new_last_name, user_id))
        
        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Database error while updating name: {e}")
    finally:
        conn.close()

# Update the password for a specific user
def update_user_password(user_id, new_password):
    """
    Update the password for a specific user.
    :param user_id: The ID of the user.
    :param new_password: The new password.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Hash the new password for security
    hashed_password = hash_password(new_password)

    try:
        cursor.execute("""
        UPDATE users
        SET password_hash = ?
        WHERE id = ?
        """, (hashed_password, user_id))
        
        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Database error while updating password: {e}")
    finally:
        conn.close()
        
def load_user_from_db(user_id=None, email=None):
    """
    Load a user by ID or email.
    :param user_id: The user's ID (optional).
    :param email: The user's email (optional).
    :return: A dictionary containing the user's details, or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if user_id and email:
            raise ValueError("Provide only one of user_id or email, not both.")
        elif user_id:
            query = "SELECT id, username, first_name, last_name, email, password_hash FROM users WHERE id = ?"
            cursor.execute(query, (user_id,))
        elif email:
            query = "SELECT id, username, first_name, last_name, email, password_hash FROM users WHERE email = ?"
            cursor.execute(query, (email,))
        else:
            raise ValueError("Either user_id or email must be provided.")

        user = cursor.fetchone()

        if user:
            return {
                "id": user["id"],
                "username": user["username"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "email": user["email"],
                "password_hash": user["password_hash"]
            }
        return None

    except sqlite3.Error as e:
        raise ValueError(f"Database error: {e}")

    finally:
        conn.close()