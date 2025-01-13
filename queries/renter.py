from db_setup import get_db_connection
from app.components.utils import hash_password  # Assuming you have the hash_password function in utils.py
import sqlite3
import streamlit as st
import json

# Save renter profile to the database
def save_renter_profile_to_db(user_id, profile_data):
    """Save or update renter profile data."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        renter_profile_pic_data = sqlite3.Binary(profile_data.get("profile_pic")) if profile_data.get("profile_pic") else None

        cursor.execute("""
        INSERT INTO renter_profiles (
            profile_pic, user_id, tagline, age, phone, nationality, occupation, contract_type,
            income, work_mode, bio, hobbies, social_media
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            profile_pic=excluded.profile_pic,
            tagline=excluded.tagline, 
            age=excluded.age,
            phone=excluded.phone, 
            nationality=excluded.nationality, 
            occupation=excluded.occupation,
            contract_type=excluded.contract_type, 
            income=excluded.income, 
            work_mode=excluded.work_mode,
            bio=excluded.bio, 
            hobbies=excluded.hobbies,
            social_media=excluded.social_media
        """, (
            renter_profile_pic_data,
            user_id,
            profile_data.get("tagline"),
            profile_data.get("age"),
            profile_data.get("phone"),
            profile_data.get("nationality"),
            profile_data.get("occupation"),
            profile_data.get("contract_type"),
            profile_data.get("income"),
            profile_data.get("work_mode"),
            profile_data.get("bio"),
            profile_data.get("hobbies"),
            profile_data.get("social_media")
        ))

        conn.commit()

        cursor.execute("SELECT id FROM renter_profiles WHERE user_id = ?", (user_id,))
        profile_id = cursor.fetchone()
        if profile_id:
            st.session_state["profile_id"] = profile_id[0]  # Save profile_id in session state
            return profile_id[0]

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()

    return None

# Load renter profile from the database
def load_renter_profile_from_db(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT id, profile_pic, tagline, age, phone, 
        nationality, occupation, contract_type, income, work_mode, bio, hobbies, social_media
        FROM renter_profiles WHERE user_id = ?
        """, (user_id,))
        return cursor.fetchone()

    finally:
        conn.close()
        
def get_all_renter_user_ids():
    """
    Retrieve all user IDs of users who have a renter profile.
    :return: List of user IDs.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Query to fetch all user IDs from renter_profiles
        cursor.execute("""
        SELECT user_id
        FROM renter_profiles
        """)

        # Fetch all user IDs as a list
        user_ids = [row["user_id"] for row in cursor.fetchall()]
        return user_ids

    except sqlite3.Error as e:
        raise ValueError(f"Error fetching renter user IDs: {e}")

    finally:
        conn.close()
        
def save_rental_preferences_to_db(profile_id, preferences_data):
    """
    Save or update rental preferences in the database.
    :param profile_id: The profile ID associated with the rental preferences.
    :param preferences_data: A dictionary containing the rental preferences.
    """
    conn = get_db_connection()
    
    try:
        cursor = conn.cursor()

        # Default values for missing data
        preferred_city = ", ".join(preferences_data.get("preferred_city", [])) or ""
        preferred_area = ", ".join(preferences_data.get("preferred_area", [])) or ""
        budget_min = preferences_data.get("budget_min", 0)
        budget_max = preferences_data.get("budget_max", 0)
        property_type = preferences_data.get("property_type", "")
        property_size_min = preferences_data.get("property_size_min", 0.0)
        property_size_max = preferences_data.get("property_size_min", 0.0)
        bedrooms = preferences_data.get("bedrooms", 0)
        bathrooms = preferences_data.get("bathrooms", 0)
        floor = preferences_data.get("floor", 0)
        number_of_people = preferences_data.get("number_of_people", 1)
        move_in_date = preferences_data.get("move_in_date", "")
        pets = preferences_data.get("pets", False)
        pet_type = preferences_data.get("pet_type", "")
        lease_duration = preferences_data.get("lease_duration", "")

        cursor.execute("""
            INSERT INTO rental_preferences (
                profile_id, preferred_city, preferred_area, budget_min, budget_max, 
                property_type, property_size_min, property_size_max, bedrooms, bathrooms, 
                floor, number_of_people, move_in_date, 
                pets, pet_type, lease_duration
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(profile_id) DO UPDATE SET
                preferred_city = excluded.preferred_city, 
                preferred_area = excluded.preferred_area,
                budget_min = excluded.budget_min, 
                budget_max = excluded.budget_max,
                property_type = excluded.property_type,
                property_size_min = excluded.property_size_min,
                property_size_max = excluded.property_size_max,
                bedrooms = excluded.bedrooms,
                bathrooms = excluded.bathrooms,
                floor = excluded.floor,
                number_of_people = excluded.number_of_people, 
                move_in_date = excluded.move_in_date,
                pets = excluded.pets, 
                pet_type = excluded.pet_type,
                lease_duration = excluded.lease_duration
        """, (
            profile_id,
            preferred_city,
            preferred_area,
            budget_min,
            budget_max,
            property_type,
            property_size_min,
            property_size_max,
            bedrooms,
            bathrooms,
            floor,
            number_of_people,
            move_in_date,
            pets,
            pet_type,
            lease_duration
        ))

        conn.commit()
        print("Rental preferences saved or updated successfully.")
        
    except sqlite3.Error as e:
        conn.rollback()  # Rollback if an error occurs
        raise ValueError(f"Database error while saving rental preferences: {e}")

    finally:
        conn.close()


# Load rental preferences from the database

def load_rental_preferences_from_db(profile_id):
    """
    Load rental preferences for a specific profile ID.
    :param profile_id: The ID of the renter profile.
    :return: A dictionary containing rental preferences, or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT preferred_city, preferred_area, budget_min, budget_max,property_type, 
        property_size_min, property_size_max, bedrooms, bathrooms, floor, number_of_people, 
        move_in_date, pets, pet_type, lease_duration
        FROM rental_preferences WHERE profile_id = ?
        """, (profile_id,))
        preferences = cursor.fetchone()

        if preferences:
            return {
                "preferred_city": preferences["preferred_city"],
                "preferred_area": preferences["preferred_area"],
                "budget_min": preferences["budget_min"],
                "budget_max": preferences["budget_max"],
                "property_type": preferences["property_type"],
                "property_size_min": preferences["property_size_min"],
                "property_size_max": preferences["property_size_max"],
                "bedrooms": preferences["bedrooms"],
                "bathrooms": preferences["bathrooms"],
                "floor": preferences["floor"],
                "number_of_people": preferences["number_of_people"],
                "move_in_date": preferences["move_in_date"],
                "pets": preferences["pets"],
                "pet_type": preferences["pet_type"],
                "lease_duration": preferences["lease_duration"]
            }
        return None

    finally:
        conn.close()
        
def update_rental_preferences(profile_id, filter_options):
    """
    Update rental preferences for a specific profile ID based on the given filter options.

    :param profile_id: The profile ID associated with the rental preferences.
    :param filter_options: A dictionary containing the fields to update and their new values.
    """
    conn = get_db_connection()
    
    try:
        cursor = conn.cursor()

        # Generate SQL dynamically based on provided filter options
        set_clause = ", ".join([f"{key} = ?" for key in filter_options.keys()])
        values = list(filter_options.values())
        values.append(profile_id)  # Add profile_id at the end for the WHERE clause

        query = f"""
        UPDATE rental_preferences
        SET {set_clause}
        WHERE profile_id = ?
        """

        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount > 0:
            print(f"Rental preferences for profile_id {profile_id} updated successfully.")
        else:
            print(f"No rental preferences found for profile_id {profile_id}.")

    except sqlite3.Error as e:
        conn.rollback()  # Rollback if an error occurs
        raise ValueError(f"Database error while updating rental preferences: {e}")

    finally:
        conn.close()


def save_credit_score(user_id, status, authorized, uploaded_file):
    """Save a renter's credit score to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO renter_credit_scores (user_id, status, authorized, uploaded_file)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, status, int(authorized), int(uploaded_file))
    )
    conn.commit()
    conn.close()
    print(f"Credit score for user_id {user_id} saved with status '{status}', authorized={authorized}, uploaded_file={uploaded_file}.")
    
    

def load_credit_scores(user_id=None):
    """
    Load renter credit scores from the database.
    
    Args:
        user_id (int, optional): User ID to filter by. If None, loads all credit scores.
    
    Returns:
        list of dict: List of credit scores with column mapping if user_id is None.
        dict or None: Dictionary with credit score details for the given user_id, or None if not found.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if user_id:
            cursor.execute(
                """
                SELECT status, authorized, uploaded_file 
                FROM renter_credit_scores 
                WHERE user_id = ?
                """,
                (user_id,)
            )
            row = cursor.fetchone()
            conn.close()
            if row:
                print(f"Credit score details for user_id {user_id} loaded successfully.")
                return {
                    "status": row[0],
                    "authorized": bool(row[1]),
                    "uploaded_file": bool(row[2])
                }
            else:
                print(f"No credit score found for user_id {user_id}.")
                return None
        else:
            cursor.execute("SELECT user_id, status, authorized, uploaded_file FROM renter_credit_scores")
            rows = cursor.fetchall()
            conn.close()

            # Map results to a list of dictionaries
            credit_scores = [
                {
                    "user_id": row[0],
                    "status": row[1],
                    "authorized": bool(row[2]),
                    "uploaded_file": bool(row[3])
                } for row in rows
            ]
            print("All credit scores loaded successfully.")
            return credit_scores

    except Exception as e:
        print(f"Error loading credit scores: {e}")
        return None if user_id else []
    
def delete_credit_score(user_id=None):
    """
    Delete renter credit score(s) from the database.

    Args:
        user_id (int, optional): User ID to filter by. If None, deletes all credit scores.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if user_id:
            # Delete specific user's credit score
            cursor.execute(
                """
                DELETE FROM renter_credit_scores
                WHERE user_id = ?
                """,
                (user_id,)
            )
            if cursor.rowcount > 0:
                print(f"Credit score for user_id {user_id} deleted successfully.")
            else:
                print(f"No credit score found for user_id {user_id}.")
        else:
            # Delete all credit scores
            cursor.execute("DELETE FROM renter_credit_scores")
            print("All credit scores deleted successfully.")

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"Error deleting credit scores: {e}")
        return False

# CREDIT SCORE ADMIN FUNCTIONS

def load_pending_credit_scores():
    """
    Load all pending renter credit scores for admin review.

    Returns:
        list of dict: List of pending credit scores with details.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch all pending credit scores
        cursor.execute(
            """
            SELECT user_id, status, authorized, uploaded_file, request_timestamp
            FROM renter_credit_scores
            WHERE status = 'Pending'
            """
        )
        rows = cursor.fetchall()
        conn.close()

        # Map results to a list of dictionaries
        pending_scores = [
            {
                "user_id": row[0],
                "status": row[1],
                "authorized": bool(row[2]),
                "uploaded_file": row[3],  # This is binary data
                "request_timestamp": row[4],
            } for row in rows
        ]

        print("All pending credit scores loaded successfully.")
        return pending_scores

    except Exception as e:
        print(f"Error loading pending credit scores: {e}")
        return []

def download_credit_score_file(user_id):
    """
    Retrieve the uploaded credit score file for a specific user.

    Args:
        user_id (int): The ID of the user whose file is to be downloaded.

    Returns:
        tuple: (file_data, success) where file_data is binary content or None, and success is a boolean.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the uploaded file for the specified user
        cursor.execute(
            """
            SELECT uploaded_file
            FROM renter_credit_scores
            WHERE user_id = ?
            """,
            (user_id,)
        )
        row = cursor.fetchone()
        conn.close()

        if row and row[0]:
            print(f"File for user_id {user_id} retrieved successfully.")
            return row[0], True  # Return the binary file data
        else:
            print(f"No uploaded file found for user_id {user_id}.")
            return None, False

    except Exception as e:
        print(f"Error downloading file for user_id {user_id}: {e}")
        return None, False

def update_credit_score_status(user_id, new_status):
    """
    Update the status of a renter's credit score.

    Args:
        user_id (int): The ID of the user whose credit score status is to be updated.
        new_status (str): The new status to set ('Verified' or 'Rejected').

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update the status for the specified user
        cursor.execute(
            """
            UPDATE renter_credit_scores
            SET status = ?, verification_timestamp = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            (new_status, user_id)
        )

        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            print(f"Credit score for user_id {user_id} updated to '{new_status}'.")
            return True
        else:
            conn.close()
            print(f"No credit score found for user_id {user_id}.")
            return False

    except Exception as e:
        print(f"Error updating credit score status for user_id {user_id}: {e}")
        return False
        
        
def load_renter_profile_with_credit_status(user_id):
    """
    Fetch the renter profile, username, and credit score status for a given user ID.
    
    Args:
        user_id (int): The ID of the user.
    
    Returns:
        dict: A dictionary containing renter profile, username, and credit score status, or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Query to fetch the renter profile and associated username and credit score status
        query = """
        SELECT 
            u.username, 
            rp.*, 
            rcs.status AS credit_score_status
        FROM users u
        LEFT JOIN renter_profiles rp ON u.id = rp.user_id
        LEFT JOIN renter_credit_scores rcs ON u.id = rcs.user_id
        WHERE u.id = ?
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        
        if result:
            # Convert the row to a dictionary
            return {
                "username": result["username"],
                "renter_profile": {
                    "profile_pic": result["profile_pic"],
                    "first_name": result["first_name"],
                    "surname": result["surname"],
                    "tagline": result["tagline"],
                    "age": result["age"],
                    "phone": result["phone"],
                    "nationality": result["nationality"],
                    "occupation": result["occupation"],
                    "contract_type": result["contract_type"],
                    "income": result["income"],
                    "work_mode": result["work_mode"],
                    "bio": result["bio"],
                    "hobbies": result["hobbies"],
                    "social_media": result["social_media"]
                },
                "credit_score_status": result["credit_score_status"]
            }
        # Return None if no results found for the user ID else return the dictionary
        return None
    
    finally:
        conn.close()
        
