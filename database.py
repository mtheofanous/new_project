from db_setup import get_db_connection
from app.components.utils import hash_password  # Assuming you have the hash_password function in utils.py
import sqlite3

def save_user_to_db(username, email, password, role):
    """
    Save a new user to the database during sign-up.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Hash the user's password
        password_hash = hash_password(password)

        # Insert the new user into the users table
        cursor.execute("""
        INSERT INTO users (username, email, password_hash, role)
        VALUES (?, ?, ?, ?)
        """, (username, email, password_hash, role))

        # Commit the changes
        conn.commit()

        # Get the ID of the newly inserted user
        user_id = cursor.lastrowid
        return user_id  # Return the new user's ID

    except sqlite3.IntegrityError:
        # Handle duplicate email error
        conn.rollback()
        raise ValueError("A user with this email already exists. Please use a different email.")

    finally:
        conn.close()

# Save renter profile to the database
def save_renter_profile_to_db(user_id, profile_data):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO renter_profiles (profile_pic, user_id, name, email,tagline, age, phone, nationality, occupation, contract_type, income, work_mode, bio, hobbies)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            profile_pic=excluded.profile_pic, name=excluded.name, email=excluded.email,tagline=excluded.tagline, age=excluded.age,
            phone=excluded.phone, nationality=excluded.nationality, occupation=excluded.occupation,
            contract_type=excluded.contract_type, income=excluded.income, work_mode=excluded.work_mode,
            bio=excluded.bio, hobbies=excluded.hobbies
        """, (
            profile_data.get("profile_pic"),
            user_id,
            profile_data.get("name"),
            profile_data.get("tagline"),
            profile_data.get("email"),
            profile_data.get("age"),
            profile_data.get("phone"),
            profile_data.get("nationality"),
            profile_data.get("occupation"),
            profile_data.get("contract_type"),
            profile_data.get("income"),
            profile_data.get("work_mode"),
            profile_data.get("bio"),
            profile_data.get("hobbies")
        ))

        conn.commit()

    finally:
        conn.close()
        
# Save rental preferences to the database
def save_rental_preferences_to_db(profile_id, preferences_data):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO rental_preferences (profile_id, preferred_city, preferred_area, budget_min, budget_max, property_type, rooms_needed, number_of_people, move_in_date, lease_duration, pets, pet_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(profile_id) DO UPDATE SET
            preferred_city=excluded.preferred_city, preferred_area=excluded.preferred_area,
            budget_min=excluded.budget_min, budget_max=excluded.budget_max,
            property_type=excluded.property_type, rooms_needed=excluded.rooms_needed,
            number_of_people=excluded.number_of_people, move_in_date=excluded.move_in_date,
            lease_duration=excluded.lease_duration, pets=excluded.pets, pet_type=excluded.pet_type
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
            preferences_data.get("lease_duration"),
            preferences_data.get("pets"),
            preferences_data.get("pet_type")
        ))

        conn.commit()

    finally:
        conn.close()

# Save credit scores to the database
def save_credit_scores_to_db(profile_id, credit_score_data):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO credit_scores (profile_id, credit_score_verified, uploaded_document)
        VALUES (?, ?, ?)
        ON CONFLICT(profile_id) DO UPDATE SET
            credit_score_verified=excluded.credit_score_verified, uploaded_document=excluded.uploaded_document
        """, (
            profile_id,
            credit_score_data.get("credit_score_verified"),
            credit_score_data.get("uploaded_document")
        ))

        conn.commit()

    finally:
        conn.close()
        
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


# Load user from the database
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
        if user_id:
            cursor.execute("SELECT id, username, email, password_hash, role FROM users WHERE id = ?", (user_id,))
        elif email:
            cursor.execute("SELECT id, username, email, password_hash, role FROM users WHERE email = ?", (email,))
        else:
            raise ValueError("Either user_id or email must be provided.")

        user = cursor.fetchone()

        if user:
            return {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "password_hash": user["password_hash"],
                "role": user["role"]
            }
        return None

    finally:
        conn.close()

# Load renter profile from the database
def load_renter_profile_from_db(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT profile_pic, name, email, tagline, age, phone, nationality, occupation, contract_type, income, work_mode, bio, hobbies
        FROM renter_profiles WHERE user_id = ?
        """, (user_id,))
        return cursor.fetchone()

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
        SELECT preferred_city, preferred_area, budget_min, budget_max, property_type, rooms_needed, number_of_people, move_in_date, lease_duration, pets, pet_type
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
                "lease_duration": preferences["lease_duration"],
                "pets": preferences["pets"],
                "pet_type": preferences["pet_type"]
            }
        return None

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



