from db_setup import get_db_connection
from app.components.utils import hash_password  # Assuming you have the hash_password function in utils.py
import sqlite3
import streamlit as st
import json

def save_landlord_profile_to_db(user_id, profile_data):
    """Save or update landlord profile data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        landlord_profile_pic_data = sqlite3.Binary(profile_data.get("landlord_profile_pic")) if profile_data.get("landlord_profile_pic") else None
        
        cursor.execute("""
        INSERT INTO landlord_profiles (
            profile_pic, user_id, phone, social_media, preferred_communication, 
            languages, about_me
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            profile_pic=excluded.profile_pic,
            phone=excluded.phone, 
            social_media=excluded.social_media,
            preferred_communication=excluded.preferred_communication,
            languages=excluded.languages,
            about_me=excluded.about_me
        """, (
            landlord_profile_pic_data,
            user_id,
            profile_data.get("phone"),
            profile_data.get("social_media"),
            profile_data.get("preferred_communication"),
            profile_data.get("languages"),
            profile_data.get("about_me"),
        ))
        
        conn.commit()
        
        # Fetch the profile_id of the inserted or updated row
        cursor.execute("SELECT id FROM landlord_profiles WHERE user_id = ?", (user_id,))
        landlord_profile_id = cursor.fetchone()
        if landlord_profile_id:
            return landlord_profile_id[0]  # Return the landlord_profile_id
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()
        
    return None  # Return None if no landlord profile ID is found

# Load landlord profile from the database
def load_landlord_profile_from_db(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT id, profile_pic, phone,
        social_media, preferred_communication, 
        languages, about_me
        FROM landlord_profiles WHERE user_id = ?
        """, (user_id,))
        return cursor.fetchone()

    finally:
        conn.close()