from db_setup import get_db_connection
from app.components.utils import hash_password  # Assuming you have the hash_password function in utils.py
import sqlite3
import streamlit as st

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
            profile_pic, user_id, first_name, surname, tagline, age, phone, nationality, occupation, contract_type,
            income, work_mode, bio, hobbies, social_media
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            profile_pic=excluded.profile_pic,
            first_name=excluded.first_name,
            surname=excluded.surname, 
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
            profile_data.get("surname"),
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
        SELECT id, profile_pic, first_name, surname, tagline, age, phone, nationality, occupation, contract_type, income, work_mode, bio, hobbies, social_media
        FROM renter_profiles WHERE user_id = ?
        """, (user_id,))
        return cursor.fetchone()

    finally:
        conn.close()
        

import sqlite3

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
        rooms_needed = preferences_data.get("rooms_needed", 0)
        number_of_people = preferences_data.get("number_of_people", 1)
        move_in_date = preferences_data.get("move_in_date", "")
        pets = preferences_data.get("pets", False)
        pet_type = preferences_data.get("pet_type", "")
        lease_duration = preferences_data.get("lease_duration", "")

        cursor.execute("""
            INSERT INTO rental_preferences (
                profile_id, preferred_city, preferred_area, budget_min, budget_max, 
                property_type, rooms_needed, number_of_people, move_in_date, 
                pets, pet_type, lease_duration
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(profile_id) DO UPDATE SET
                preferred_city = excluded.preferred_city, 
                preferred_area = excluded.preferred_area,
                budget_min = excluded.budget_min, 
                budget_max = excluded.budget_max,
                property_type = excluded.property_type, 
                rooms_needed = excluded.rooms_needed,
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
            rooms_needed,
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
        SELECT preferred_city, preferred_area, budget_min, budget_max, property_type, rooms_needed, number_of_people, move_in_date, pets, pet_type, lease_duration
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
                "rooms_needed": preferences["rooms_needed"],
                "number_of_people": preferences["number_of_people"],
                "move_in_date": preferences["move_in_date"],
                "pets": preferences["pets"],
                "pet_type": preferences["pet_type"],
                "lease_duration": preferences["lease_duration"]
            }
        return None

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

# Save agent profile to the database
def save_agent_profile_to_db(user_id, profile_data):
    """Save or update agent profile data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        agent_profile_pic_data = sqlite3.Binary(profile_data.get("agent_profile_pic")) if profile_data.get("agent_profile_pic") else None
        
        cursor.execute("""
        INSERT INTO agent_profiles (
            agent_profile_pic, user_id, name, phone, agency_name, agency_address,
            agency_website, social_media, working_days, working_hours, preferred_communication, 
            services, languages, mission_statement
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            agent_profile_pic=excluded.agent_profile_pic, 
            name=excluded.name, 
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
            profile_data.get("name"),
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
        SELECT id, agent_profile_pic, name, phone, agency_name, agency_address, agency_website,
        social_media, working_days, working_hours, preferred_communication, 
        services, languages, mission_statement
        FROM agent_profiles WHERE user_id = ?
        """, (user_id,))
        return cursor.fetchone()

    finally:
        conn.close()
        

# Save property data to the database

def save_property_to_db(property_data):
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
            property_type, property_size, property_location, property_price,
            price_per_sqm, bedrooms, bathrooms, floor, year_built, condition,
            renovation_year, energy_class, availability, available_from,
            heating_method, zone, creation_method
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
            property_data.get("creation_method", "manual")
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


def load_properties_by_user(user_id, role=None):
    """
    Load properties associated with a specific user.
    :param user_id: The ID of the user.
    :param role: Optional role ('landlord' or 'agent') to filter by.
    :return: List of property dictionaries.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT p.*
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
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        raise ValueError(f"Database error while loading properties for user: {e}")
    finally:
        conn.close()
        

def get_users_for_property(property_id):
    """
    Fetch users (landlords and agents) associated with a property.
    :param property_id: The ID of the property.
    :return: List of dictionaries containing user details and roles.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT u.username, u.email, po.role
        FROM property_ownership po
        JOIN users u ON po.user_id = u.id
        WHERE po.property_id = ?
        """
        cursor.execute(query, (property_id,))
        rows = cursor.fetchall()
        return [{"username": row["username"], "email": row["email"], "role": row["role"]} for row in rows]
    except Exception as e:
        raise ValueError(f"Error loading users for property: {e}")
    finally:
        conn.close()