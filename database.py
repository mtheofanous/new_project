from db_setup import get_db_connection
from app.components.utils import hash_password  # Assuming you have the hash_password function in utils.py
import sqlite3

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
        cursor.execute("""
        INSERT INTO renter_profiles (
            profile_pic, user_id, name, tagline, age, phone, nationality, occupation, contract_type,
            income, work_mode, bio, hobbies, social_media
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            profile_pic=excluded.profile_pic, 
            name=excluded.name, 
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
            profile_data.get("profile_pic"),
            user_id,
            profile_data.get("name"),
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
        # Fetch the profile_id of the inserted or updated row
        cursor.execute("SELECT id FROM renter_profiles WHERE user_id = ?", (user_id,))
        profile_id = cursor.fetchone()
        if profile_id:
            return profile_id[0]  # Return the profile_id

    finally:
        conn.close()
    return None  # Return None if no profile ID is found

# Load renter profile from the database
def load_renter_profile_from_db(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT id, profile_pic, name, tagline, age, phone, nationality, occupation, contract_type, income, work_mode, bio, hobbies
        FROM renter_profiles WHERE user_id = ?
        """, (user_id,))
        return cursor.fetchone()

    finally:
        conn.close()
        

def save_rental_preferences_to_db(profile_id, preferences_data):
    """
    Save or update rental preferences in the database.
    :param profile_id: The profile ID associated with the rental preferences.
    :param preferences_data: A dictionary containing the rental preferences.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO rental_preferences (
            profile_id, preferred_city, preferred_area, budget_min, budget_max, 
            property_type, rooms_needed, number_of_people, move_in_date, 
            pets, pet_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            pet_type = excluded.pet_type
        """, (
            profile_id,
            preferences_data.get("preferred_city"),
            preferences_data.get("preferred_area"),
            preferences_data.get("budget_min"),
            preferences_data.get("budget_max"),
            preferences_data.get("property_type"),
            preferences_data.get("rooms_needed"),
            preferences_data.get("number_of_people"),
            preferences_data.get("move_in_date"),
            preferences_data.get("pets"),
            preferences_data.get("pet_type")
        ))

        conn.commit()
        print("Rental preferences saved or updated successfully.")
        

    except sqlite3.Error as e:
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
        SELECT preferred_city, preferred_area, budget_min, budget_max, property_type, rooms_needed, number_of_people, move_in_date, pets, pet_type
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
                "pet_type": preferences["pet_type"]
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

# Save landlord recommendations to the database
def save_landlord_recommendations_to_db(renter_id, recommendations):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        for recommendation in recommendations:
            cursor.execute("""
            INSERT INTO landlord_recommendations (renter_id, landlord_name, landlord_email, landlord_phone, status)
            VALUES (?, ?, ?, ?, ?)
            """, (
                renter_id,
                recommendation.get("landlord_name"),
                recommendation.get("landlord_email"),
                recommendation.get("landlord_phone"),
                recommendation.get("status")
            ))

        conn.commit()

    finally:
        conn.close()
        







        
# Load credit scores from the database

def load_credit_scores_from_db(profile_id):
    """
    Load credit score information for a specific profile ID.
    :param profile_id: The ID of the renter profile.
    :return: A dictionary containing credit score details, or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT credit_score_verified, uploaded_document
        FROM credit_scores WHERE profile_id = ?
        """, (profile_id,))
        credit_score = cursor.fetchone()

        if credit_score:
            return {
                "credit_score_verified": credit_score["credit_score_verified"],
                "uploaded_document": credit_score["uploaded_document"]
            }
        return None

    finally:
        conn.close()


# Load landlord recommendations from the database
def load_landlord_recommendations_from_db(renter_id):
    """
    Load all landlord recommendations for a specific renter ID.
    :param renter_id: The ID of the renter profile.
    :return: A list of dictionaries containing landlord recommendations.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT landlord_name, landlord_email, landlord_phone, status
        FROM landlord_recommendations WHERE renter_id = ?
        """, (renter_id,))
        recommendations = cursor.fetchall()

        return [
            {
                "landlord_name": recommendation["landlord_name"],
                "landlord_email": recommendation["landlord_email"],
                "landlord_phone": recommendation["landlord_phone"],
                "status": recommendation["status"]
            }
            for recommendation in recommendations
        ]

    finally:
        conn.close()



