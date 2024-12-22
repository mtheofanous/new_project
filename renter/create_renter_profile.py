import streamlit as st
import uuid
from navigation_buttons import home_button, back_button 
from credit_score.credit_score import income_credit_score
# from recommendations.recommendation import recommendation_form
from database import save_renter_profile_to_db, save_rental_preferences_to_db

def create_renter_profile():
    username = st.session_state.get("user", "User")
    email = st.session_state.get("email", "Email")
    
    # Back to Home Button
    home_button()
    
    st.title("Create Your Renter Profile")
    st.write("Welcome! Let's set up your renter profile so landlords and agents can get to know you.")

    # Profile Header
    st.header("Profile Header")
    username = st.text_input("Username", key="new_profile_username", value=username)
    name = st.text_input("Full Name", placeholder="John Doe", key="new_profile_name")
    tagline = st.text_input("Tagline", placeholder="Looking for a cozy apartment in downtown LA", key="new_profile_tagline")
    profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"], key="new_profile_pic")

    # Personal Details
    with st.expander("Personal Details"):
        email = st.text_input("Email", key="new_profile_email", value=email)
        age = st.number_input("Age", min_value=18, max_value=100, step=1, key="new_profile_age")
        phone = st.text_input("Phone Number", key="new_profile_phone")
        nationality = st.text_input("Nationality", placeholder="e.g., American", key="new_profile_nationality")
        occupation = st.text_input("Occupation", placeholder="e.g., Software Engineer", key="new_profile_occupation")
        contract_type = st.selectbox("Contract Type", ["Permanent", "Contract", "Freelancer", "Unemployed"], key="new_profile_contract")
        income = st.number_input("Monthly Income ($)", min_value=0, step=100, key="new_profile_income")
        work_mode = st.radio("Work Mode", ["Remote", "On-site", "Hybrid"], key="new_profile_work_mode")

    # Rental Preferences
    with st.expander("Rental Preferences"):
        city = st.selectbox("Preferred City", ["Athens", "Thessaloniki", "Patras", "Heraklion", "Other"], key="new_profile_city")
        areas = {
            "Athens": ["Plaka", "Kolonaki", "Glyfada", "Marousi", "Kifisia"],
            "Thessaloniki": ["Ladadika", "Toumba", "Panorama", "Pylaia", "Thermi"],
            "Patras": ["Psila Alonia", "Rio", "Agios Andreas", "Vrachneika"],
            "Heraklion": ["Knossos", "Ammoudara", "Poros", "Agios Nikolaos"],
            "Other": ["Specify Other"]
        }
        area = st.selectbox("Preferred Area", areas.get(city, ["Specify Other"]), key="new_profile_area")
        if area == "Specify Other":
            area = st.text_input("Specify your area", placeholder="Enter area name", key="new_profile_area_other")
        budget_min, budget_max = st.slider("Budget Range ($)", 500, 5000, (1000, 3000), key="new_profile_budget")
        property_type = st.selectbox("Type of Property", ["Apartment", "House", "Shared Accommodation"], key="new_profile_property_type")
        rooms = st.number_input("Number of Rooms Needed", min_value=1, step=1, key="new_profile_rooms")
        num_people = st.number_input("Number of People (including yourself)", min_value=1, step=1, key="new_profile_people")
        move_in_date = st.date_input("Move-in Date", key="new_profile_move_in")
        lease_duration = st.selectbox("Lease Duration", ["Short-term", "Long-term", "Flexible"], key="new_profile_lease_duration")
        pets = st.radio("Do you have pets?", ["No", "Yes"], key="new_profile_pets")
        pet_type = st.text_input("Pet Type (e.g., Dog, Cat)", key="new_profile_pet_type") if pets == "Yes" else None

    # About Me
    with st.expander("About Me"):
        bio = st.text_area("Bio", placeholder="Write something about yourself...", key="new_profile_bio")
        hobbies = st.text_input("Hobbies & Interests (comma-separated)", key="new_profile_hobbies")

    # Save profile button
    if st.button("Save Profile", key="save_new_profile"):
        try:
            # Save renter profile to database
            profile_data = {
                "profile_pic": profile_pic.read() if profile_pic else None,
                "name": name,
                "tagline": tagline,
                "age": age,
                "phone": phone,
                "nationality": nationality,
                "occupation": occupation,
                "contract_type": contract_type,
                "income": income,
                "work_mode": work_mode,
                "bio": bio,
                "hobbies": hobbies
            }
            user_id = st.session_state["user_id"]
            save_renter_profile_to_db(user_id, profile_data)

            # Save rental preferences to database
            preferences_data = {
                "preferred_city": city,
                "preferred_area": area,
                "budget_min": budget_min,
                "budget_max": budget_max,
                "property_type": property_type,
                "rooms_needed": rooms,
                "number_of_people": num_people,
                "move_in_date": move_in_date,
                "lease_duration": lease_duration,
                "pets": pets,
                "pet_type": pet_type
            }
            profile_id = st.session_state["profile_id"]  # Ensure profile_id is stored during the renter profile save
            save_rental_preferences_to_db(profile_id, preferences_data)

            st.success("Profile and rental preferences saved successfully!")
            st.session_state["current_page"] = "dashboard"  # Redirect to the renter dashboard

        except Exception as e:
            st.error(f"An error occurred while saving your profile: {e}")


if __name__ == "__main__":
    create_renter_profile()

