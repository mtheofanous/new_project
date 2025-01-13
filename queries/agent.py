from db_setup import get_db_connection
from app.components.utils import hash_password  # Assuming you have the hash_password function in utils.py
import sqlite3
import streamlit as st
import json

# Save agent profile to the database
def save_agent_profile_to_db(user_id, profile_data):
    """Save or update agent profile data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        agent_profile_pic_data = sqlite3.Binary(profile_data.get("agent_profile_pic")) if profile_data.get("agent_profile_pic") else None
        
        cursor.execute("""
        INSERT INTO agent_profiles (
            agent_profile_pic, user_id, phone, agency_name, agency_address,
            agency_website, social_media, working_days, working_hours, preferred_communication, 
            services, languages, mission_statement
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            agent_profile_pic=excluded.agent_profile_pic,
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
        SELECT id, agent_profile_pic, phone, agency_name, agency_address, agency_website,
        social_media, working_days, working_hours, preferred_communication, 
        services, languages, mission_statement
        FROM agent_profiles WHERE user_id = ?
        """, (user_id,))
        return cursor.fetchone()

    finally:
        conn.close()