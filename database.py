from db_setup import get_db_connection
from app.components.utils import hash_password  # Assuming you have the hash_password function in utils.py
import sqlite3
import streamlit as st
import json


def save_user_to_db(username, email, password):
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
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
        """, (username, email, hashed_password))

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
            query = "SELECT id, username, email, password_hash FROM users WHERE id = ?"
            cursor.execute(query, (user_id,))
        elif email:
            query = "SELECT id, username, email, password_hash FROM users WHERE email = ?"
            cursor.execute(query, (email,))
        else:
            raise ValueError("Either user_id or email must be provided.")

        user = cursor.fetchone()

        if user:
            return {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "password_hash": user["password_hash"]
            }
        return None

    except sqlite3.Error as e:
        raise ValueError(f"Database error: {e}")

    finally:
        conn.close()


# Save renter profile to the database
def save_renter_profile_to_db(user_id, profile_data):
    """Save or update renter profile data."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        renter_profile_pic_data = sqlite3.Binary(profile_data.get("profile_pic")) if profile_data.get("profile_pic") else None

        cursor.execute("""
        INSERT INTO renter_profiles (
            profile_pic, user_id, first_name, last_name, tagline, age, phone, nationality, occupation, contract_type,
            income, work_mode, bio, hobbies, social_media
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            profile_pic=excluded.profile_pic,
            first_name=excluded.first_name,
            last_name=excluded.last_name, 
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
            profile_data.get("first_name"),
            profile_data.get("last_name"),
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
        SELECT id, profile_pic, first_name, last_name, tagline, age, phone, 
        nationality, occupation, contract_type, income, work_mode, bio, hobbies, social_media
        FROM renter_profiles WHERE user_id = ?
        """, (user_id,))
        return cursor.fetchone()

    finally:
        conn.close()
        
        
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
        
# save property interest to the database
        
def save_property_interest(property_id, user_id):
    """
    Save a user's interest in a property.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert the user's interest in the property
        cursor.execute("""
        INSERT INTO property_interest (property_id, user_id)
        VALUES (?, ?)
        """, (property_id, user_id))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        # The user already expressed interest in this property
        return False

    finally:
        conn.close()
        

# Delete property interest from the database
        
def delete_property_interest(property_id, user_id):
    """
    Remove a user's interest in a property.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        DELETE FROM property_interest
        WHERE property_id = ? AND user_id = ?
        """, (property_id, user_id))

        if cursor.rowcount > 0:  # Check if any rows were deleted
            conn.commit()
            return True  # Successfully removed interest
        else:
            return False  # No interest to delete

    finally:
        conn.close()
        
def update_renter_interest_status(property_id, user_id, status):
    """
    Update the status of a renter's interest in a property.

    :param property_id: The ID of the property.
    :param user_id: The ID of the renter.
    :param status: The new status ('Accepted' or 'Rejected').
    :return: bool: True if the update was successful, False otherwise.
    """
    conn = get_db_connection()
    
    try:
        cursor = conn.cursor()

        # Ensure the status is either 'Accepted' or 'Rejected'
        if status not in ['Accepted', 'Rejected']:
            raise ValueError("Status must be 'Accepted' or 'Rejected'.")

        # Update the status in the property_interest table
        cursor.execute("""
        UPDATE property_interest
        SET status = ?
        WHERE property_id = ? AND user_id = ?
        """, (status, property_id, user_id))

        if cursor.rowcount > 0:
            conn.commit()
            print(f"Status for user_id {user_id} on property_id {property_id} updated to '{status}'.")
            return True
        else:
            print(f"No interest found for user_id {user_id} on property_id {property_id}.")
            return False

    except sqlite3.Error as e:
        conn.rollback()  # Rollback changes on error
        print(f"Error updating status for user_id {user_id} on property_id {property_id}: {e}")
        return False

    finally:
        conn.close()

def load_renters_by_interest_status(property_id, status):
    """
    Load all renters who have a specific status for a given property.

    :param property_id: The ID of the property.
    :param status: The status to filter by ('Pending', 'Accepted', or 'Rejected').
    :return: list: A list of renter user IDs with the specified status.
    """
    conn = get_db_connection()
    
    try:
        cursor = conn.cursor()

        # Query renters with the specified status
        cursor.execute("""
        SELECT user_id
        FROM property_interest
        WHERE property_id = ? AND status = ?
        """, (property_id, status))

        rows = cursor.fetchall()
        conn.close()

        # Extract user IDs from the rows
        user_ids = [row[0] for row in rows]
        print(f"{len(user_ids)} renters with status '{status}' found for property_id {property_id}.")
        return user_ids

    except sqlite3.Error as e:
        print(f"Error loading renters with status '{status}' for property_id {property_id}: {e}")
        return []

    finally:
        conn.close()



def has_expressed_interest(property_id, user_id):
    """
    Check if a user has already expressed interest in a property.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT 1 FROM property_interest
        WHERE property_id = ? AND user_id = ?
        """, (property_id, user_id))
        return cursor.fetchone() is not None  # True if interest exists

    finally:
        conn.close()
        
def load_renter_ids_for_property(property_id):
    """
    Load all user IDs of renters who have expressed interest in a specific property.

    :param property_id: The ID of the property.
    :return: A list of user IDs.
    """
    conn = get_db_connection()
    
    try:
        cursor = conn.cursor()

        # Query to fetch user IDs
        cursor.execute("""
        SELECT user_id
        FROM property_interest
        WHERE property_id = ?
        """, (property_id,))

        rows = cursor.fetchall()
        conn.close()

        # Extract user IDs from the rows
        user_ids = [row[0] for row in rows]

        print(f"{len(user_ids)} renters found for property_id {property_id}.")
        return user_ids

    except sqlite3.Error as e:
        print(f"Error loading renter IDs for property_id {property_id}: {e}")
        return []

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


# Save agent profile to the database
def save_agent_profile_to_db(user_id, profile_data):
    """Save or update agent profile data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        agent_profile_pic_data = sqlite3.Binary(profile_data.get("agent_profile_pic")) if profile_data.get("agent_profile_pic") else None
        
        cursor.execute("""
        INSERT INTO agent_profiles (
            agent_profile_pic, user_id, first_name, last_name,phone, agency_name, agency_address,
            agency_website, social_media, working_days, working_hours, preferred_communication, 
            services, languages, mission_statement
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            agent_profile_pic=excluded.agent_profile_pic,
            first_name=excluded.first_name,
            last_name=excluded.last_name, 
            phone=excluded.phone, 
            agency_name=excluded.agency_name,
            agency_address=excluded.agency_address,
            agency_website=excluded.agency_website,
            social_media=excluded.social_media,
            working_days=excluded.working_days,
            working_hours=excluded.working_hours,
            preferred_communication=excluded.preferred_communication,
            services=excluded.services,
            languages=excluded.languages,
            mission_statement=excluded.mission_statement
        """, (
            agent_profile_pic_data,
            user_id,
            profile_data.get("first_name"),
            profile_data.get("last_name"),
            profile_data.get("phone"),
            profile_data.get("agency_name"),
            profile_data.get("agency_address"),
            profile_data.get("agency_website"),
            profile_data.get("social_media"),
            profile_data.get("working_days"),
            profile_data.get("working_hours"),
            profile_data.get("preferred_communication"),
            profile_data.get("services"),
            profile_data.get("languages"),
            profile_data.get("mission_statement"),
        ))
        
        conn.commit()
        
        # Fetch the profile_id of the inserted or updated row
        cursor.execute("SELECT id FROM agent_profiles WHERE user_id = ?", (user_id,))
        agent_profile_id = cursor.fetchone()
        if agent_profile_id:
            return agent_profile_id[0]  # Return the agent_profile_id
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()
        
    return None  # Return None if no agent profile ID is found

# Load agent profile from the database
def load_agent_profile_from_db(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT id, agent_profile_pic, first_name, last_name, phone, agency_name, agency_address, agency_website,
        social_media, working_days, working_hours, preferred_communication, 
        services, languages, mission_statement
        FROM agent_profiles WHERE user_id = ?
        """, (user_id,))
        return cursor.fetchone()

    finally:
        conn.close()
        

# Save property data to the database

def save_property_to_db(property_data, user_id):
    """
    Save property data to the database.
    :param property_data: Dictionary containing property details.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Insert the property
        cursor.execute("""
        INSERT INTO properties (
            friendly_name, property_type, property_size, property_location, property_price,
            price_per_sqm, bedrooms, bathrooms, floor, year_built, condition,
            renovation_year, energy_class, availability, available_from,
            heating_method, zone, creation_method, user_id, interest_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """, (
            property_data.get("friendly_name"),
            property_data.get("property_type"),
            property_data.get("property_size"),
            property_data.get("property_location"),
            property_data.get("property_price"),
            property_data.get("price_per_sqm"),
            property_data.get("bedrooms"),
            property_data.get("bathrooms"),
            property_data.get("floor"),
            property_data.get("year_built"),
            property_data.get("condition"),
            property_data.get("renovation_year"),
            property_data.get("energy_class"),
            property_data.get("availability"),
            property_data.get("available_from"),
            property_data.get("heating_method"),
            property_data.get("zone"),
            property_data.get("creation_method", "manual"),
            property_data.get("interest_count", 0),
            user_id
        ))
        conn.commit()
        return cursor.lastrowid  #
    # Return the ID of the newly created property
    except sqlite3.IntegrityError as e:
        # Provide more specific error details
        raise ValueError(
            "A property with these characteristics already exists. "
            "Ensure that location, size, type, floor, and bedrooms are unique."
        ) from e
    except sqlite3.Error as e:
        raise ValueError(f"Database error while saving property: {e}")
    finally:
        conn.close()
        
# SAVE PROPERTY IMAGES TO THE DATABASE

def save_property_image_to_db(property_id, user_id, images):
    """
    Save property images (URLs or binary data) to the database.
    :param property_id: ID of the associated property.
    :param user_id: ID of the user uploading the images.
    :param images: List of dictionaries containing 'src' or 'blob'.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        for image in images:
            cursor.execute("""
                INSERT INTO property_images (property_id, user_id, image_src, image_blob)
                VALUES (?, ?, ?, ?)
            """, (
                property_id,
                user_id,
                image.get("src"),
                image.get("blob"),
            ))
        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Error saving property images: {e}")
    finally:
        conn.close()
        
# Save the relationship between a property and a user (landlord or agent)

def save_property_ownership(property_id, user_id, role):
    """
    Save the relationship between a property and a user (landlord or agent).
    :param property_id: ID of the property.
    :param user_id: ID of the landlord or agent.
    :param role: Role of the user ('landlord' or 'agent').
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if ownership already exists
        cursor.execute("""
        SELECT 1 FROM property_ownership
        WHERE property_id = ? AND user_id = ? AND role = ?
        """, (property_id, user_id, role))
        if cursor.fetchone():
            return  # Relationship already exists, no need to insert
        
        # Insert ownership
        cursor.execute("""
        INSERT INTO property_ownership (property_id, user_id, role)
        VALUES (?, ?, ?)
        """, (property_id, user_id, role))
        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Database error while saving property ownership: {e}")
    finally:
        conn.close()
        

# Load properties by user ID
import sqlite3
from db_setup import get_db_connection

def load_property_by_id(property_id):
    """
    Load a property by its ID.
    :param property_id: ID of the property to load.
    :return: A dictionary containing property details, or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT id, friendly_name, property_type, property_size, property_location, property_price, 
               price_per_sqm, bedrooms, bathrooms, floor, year_built, condition,
               renovation_year, energy_class, availability, available_from,
               heating_method, zone, creation_method, interest_count
        FROM properties
        WHERE id = ?
        """, (property_id,))
        property_data = cursor.fetchone()

        if property_data:
            return dict(property_data)
        return None
    except sqlite3.Error as e:
        raise ValueError(f"Database error while loading property: {e}")
    finally:
        conn.close()

def update_property_in_db(property_id, updated_data, user_id):
    """
    Update property details in the database.
    :param property_id: ID of the property to update.
    :param updated_data: Dictionary containing updated property details.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        UPDATE properties
        SET friendly_name = ?, property_type = ?, property_size = ?, property_location = ?, 
            property_price = ?, price_per_sqm = ?, bedrooms = ?, bathrooms = ?, 
            floor = ?, year_built = ?, condition = ?, renovation_year = ?, 
            energy_class = ?, availability = ?, available_from = ?, 
            heating_method = ?, zone = ?, creation_method = ?, interest_count = ?
        WHERE id = ?
        """, (
            updated_data.get("friendly_name"),
            updated_data.get("property_type"),
            updated_data.get("property_size"),
            updated_data.get("property_location"),
            updated_data.get("property_price"),
            updated_data.get("price_per_sqm"),
            updated_data.get("bedrooms"),
            updated_data.get("bathrooms"),
            updated_data.get("floor"),
            updated_data.get("year_built"),
            updated_data.get("condition"),
            updated_data.get("renovation_year"),
            updated_data.get("energy_class"),
            updated_data.get("availability"),
            updated_data.get("available_from"),
            updated_data.get("heating_method"),
            updated_data.get("zone"),
            updated_data.get("creation_method", "manual"),
            updated_data.get("interest_count"),
            user_id 
        ))
        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Database error while updating property: {e}")
    finally:
        conn.close()
        
def delete_property_from_db(property_id):
    """
    Delete a property from the database.
    :param property_id: ID of the property to delete.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM properties WHERE id = ?", (property_id,))
        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Database error while deleting property: {e}")
    finally:
        conn.close()
        

def load_property_images(property_id):
    """
    Load property images for a given property ID.
    :param property_id: ID of the property to load images for.
    :return: A list of image dictionaries, or an empty list if no images are found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT image_src, image_blob
        FROM property_images
        WHERE property_id = ?
        """, (property_id,))
        rows = cursor.fetchall()
        images = [{"src": row["image_src"], "blob": row["image_blob"]} for row in rows]
        return images
    except sqlite3.Error as e:
        raise ValueError(f"Database error while loading property images: {e}")
    finally:
        conn.close()
        

        
def replace_property_images(property_id, user_id, images):
    """
    Replace all images for a given property.
    :param property_id: ID of the property.
    :param user_id: ID of the user uploading the images.
    :param images: List of dictionaries containing 'src' or 'blob'.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Delete existing images for the property
        cursor.execute("""
        DELETE FROM property_images WHERE property_id = ?
        """, (property_id,))
        
        # Insert new images
        for image in images:
            cursor.execute("""
            INSERT INTO property_images (property_id, user_id, image_src, image_blob)
            VALUES (?, ?, ?, ?)
            """, (
                property_id,
                user_id,
                image.get("src"),
                image.get("blob"),
            ))
        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Database error while replacing property images: {e}")
    finally:
        conn.close()



def load_properties_by_user(user_id, role=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT p.*, (
            SELECT json_group_array(
                json_object(
                    'src', COALESCE(pi.image_src, '')
                )
            )
            FROM property_images pi
            WHERE pi.property_id = p.id
        ) AS images
        FROM properties p
        INNER JOIN property_ownership po ON p.id = po.property_id
        WHERE po.user_id = ?
        """
        params = [user_id]
        if role:
            query += " AND po.role = ?"
            params.append(role)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        properties = []
        for row in rows:
            property_data = dict(row)
            # Parse the images JSON string
            if property_data.get("images"):
                property_data["images"] = json.loads(property_data["images"])
            else:
                property_data["images"] = []  # Default to an empty list if no images
            properties.append(property_data)
        return properties
    
    except sqlite3.Error as e:
        raise ValueError(f"Database error while loading properties for user: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON for property images: {e}")
    finally:
        conn.close()
        

# Load property images including BLOBs
def load_property_images_with_blobs(property_id):
    """
    Load property images including BLOBs.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT image_src, image_blob
        FROM property_images
        WHERE property_id = ?
        """, (property_id,))
        rows = cursor.fetchall()
        images = [{"src": row["image_src"], "blob": row["image_blob"]} for row in rows]
        return images
    except sqlite3.Error as e:
        raise ValueError(f"Database error while loading property images with blobs: {e}")
    finally:
        conn.close()

        
def get_users_for_similar_properties(property_id):
    """
    Fetch users (landlords and agents) associated with properties having similar characteristics.
    :param property_id: The ID of the reference property.
    :return: List of dictionaries containing user details and roles.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Fetch the characteristics of the reference property
        query = """
        SELECT property_type, property_size, property_location, floor, bedrooms
        FROM properties
        WHERE id = ?
        """
        cursor.execute(query, (property_id,))
        reference_property = cursor.fetchone()

        if not reference_property:
            raise ValueError(f"Property ID {property_id} not found.")

        # Find all properties with the same characteristics
        query = """
        SELECT id FROM properties
        WHERE property_type = ? AND property_size = ? AND property_location = ? AND floor = ? AND bedrooms = ?
        """
        cursor.execute(query, reference_property)
        similar_property_ids = [row["id"] for row in cursor.fetchall()]

        if not similar_property_ids:
            return []

        # Fetch users associated with the similar properties
        query = """
        SELECT u.username, u.email, po.role
        FROM property_ownership po
        JOIN users u ON po.user_id = u.id
        WHERE po.property_id IN ({})
        """.format(", ".join(["?"] * len(similar_property_ids)))  # Dynamically generate the placeholders
        cursor.execute(query, similar_property_ids)
        rows = cursor.fetchall()
        return [{"username": row["username"], "email": row["email"], "role": row["role"]} for row in rows]

    except Exception as e:
        raise ValueError(f"Error loading users for similar properties: {e}")
    finally:
        conn.close()