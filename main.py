import streamlit as st
import sqlite3
from db_setup import get_db_connection, create_tables
from landing_page import landing_page
from forms import login_form, signup_form
from renter.create_renter_profile import create_renter_profile
from renter.edit_renter_profile import edit_renter_profile
from renter.renter_summary_profile import renter_summary_profile
from renter.renter_full_profile import renter_full_profile
from dashboard import dashboard
from recommendations.recommendation import recommendation


# Save renter profile to the database
def save_profile_to_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    user_id = st.session_state.get("user_id")
    name = st.session_state.get("name", "")
    age = st.session_state.get("age", None)
    phone = st.session_state.get("phone", "")
    nationality = st.session_state.get("nationality", "")
    occupation = st.session_state.get("occupation", "")
    contract_type = st.session_state.get("contract_type", "")
    income = st.session_state.get("income", 0.0)
    work_mode = st.session_state.get("work_mode", "")

    # Save renter profile
    cursor.execute("""
    INSERT INTO renter_profiles (user_id, name, age, phone, nationality, occupation, contract_type, income, work_mode)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        name=excluded.name, age=excluded.age, phone=excluded.phone,
        nationality=excluded.nationality, occupation=excluded.occupation,
        contract_type=excluded.contract_type, income=excluded.income, work_mode=excluded.work_mode
    """, (user_id, name, age, phone, nationality, occupation, contract_type, income, work_mode))

    # Save rental preferences
    preferred_city = st.session_state.get("preferred_city", "")
    preferred_area = st.session_state.get("preferred_area", "")
    budget_min = st.session_state.get("budget_min", 0.0)
    budget_max = st.session_state.get("budget_max", 0.0)
    property_type = st.session_state.get("property_type", "")
    rooms_needed = st.session_state.get("rooms_needed", 0)
    number_of_people = st.session_state.get("number_of_people", 0)
    move_in_date = st.session_state.get("move_in_date", None)
    lease_duration = st.session_state.get("lease_duration", "")
    pets = st.session_state.get("pets", False)
    pet_type = st.session_state.get("pet_type", "")

    cursor.execute("""
    INSERT INTO rental_preferences (profile_id, preferred_city, preferred_area, budget_min, budget_max, property_type, rooms_needed, number_of_people, move_in_date, lease_duration, pets, pet_type)
    VALUES ((SELECT id FROM renter_profiles WHERE user_id = ?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(profile_id) DO UPDATE SET
        preferred_city=excluded.preferred_city, preferred_area=excluded.preferred_area,
        budget_min=excluded.budget_min, budget_max=excluded.budget_max,
        property_type=excluded.property_type, rooms_needed=excluded.rooms_needed,
        number_of_people=excluded.number_of_people, move_in_date=excluded.move_in_date,
        lease_duration=excluded.lease_duration, pets=excluded.pets, pet_type=excluded.pet_type
    """, (user_id, preferred_city, preferred_area, budget_min, budget_max, property_type, rooms_needed, number_of_people, move_in_date, lease_duration, pets, pet_type))

    conn.commit()
    conn.close()


# Load renter profile from the database
def load_profile_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    user_id = st.session_state.get("user_id")
    # Load renter profile
    cursor.execute("""
    SELECT name, age, phone, nationality, occupation, contract_type, income, work_mode
    FROM renter_profiles WHERE user_id = ?
    """, (user_id,))
    profile = cursor.fetchone()

    if profile:
        st.session_state.update({
            "name": profile["name"],
            "age": profile["age"],
            "phone": profile["phone"],
            "nationality": profile["nationality"],
            "occupation": profile["occupation"],
            "contract_type": profile["contract_type"],
            "income": profile["income"],
            "work_mode": profile["work_mode"]
        })

    # Load rental preferences
    cursor.execute("""
    SELECT preferred_city, preferred_area, budget_min, budget_max, property_type, rooms_needed, number_of_people, move_in_date, lease_duration, pets, pet_type
    FROM rental_preferences WHERE profile_id = (SELECT id FROM renter_profiles WHERE user_id = ?)
    """, (user_id,))
    preferences = cursor.fetchone()

    if preferences:
        st.session_state.update({
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
        })

    conn.close()


def main():
    # Ensure database tables are created
    create_tables()

    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "landing"
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = 1  # Simulated logged-in user ID

    # Page routing
    if st.session_state["current_page"] == "landing":
        landing_page()
    elif st.session_state["current_page"] == "login":
        login_form()
    elif st.session_state["current_page"] == "signup":
        signup_form()
    elif st.session_state["current_page"] == "create_renter_profile":
        create_renter_profile()
        if st.button("Save Profile"):
            save_profile_to_db()
    elif st.session_state["current_page"] == "dashboard":
            # Automatically load the profile when the user navigates to the dashboard
        if "profile_loaded" not in st.session_state:
            load_profile_from_db()
            st.session_state["profile_loaded"] = True  # Ensure it doesn't reload unnecessarily
        dashboard()
    
        if st.button("Load Profile"):
            load_profile_from_db()
    elif st.session_state["current_page"] == "renter_full_profile":
        renter_full_profile()
    elif st.session_state["current_page"] == "edit_renter_profile":
        edit_renter_profile()
        if st.button("Save Changes"):
            save_profile_to_db()
    elif st.session_state["current_page"] == "recommendation":
        recommendation()


if __name__ == "__main__":
    main()
