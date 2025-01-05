import streamlit as st
import uuid
from navigation_buttons import home_button, back_button 
from renter.credit_score.credit_score import credit_score
from database import save_renter_profile_to_db, save_rental_preferences_to_db
from renter.rental_preferences import rental_preferences  # Import rental preferences
import datetime


def create_renter_profile():
    home_button()
    
    st.title("Create Your Renter Profile")

    # Renter Profile Inputs
    profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"], key="create_profile_pic")
    first_name = st.text_input("First Name")
    surname = st.text_input("Surname")
    tagline = st.text_input("Tagline")
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    phone = st.text_input("Phone Number")
    
    # Phone number validation
    if phone and (not phone.isdigit() or len(phone) not in (10, 12)):
        st.error("Phone number must be 10 or 12 digits long and contain only numbers.")
        return

    nationality = st.text_input("Nationality")
    nationality = nationality.replace(" ", "").capitalize()
    occupation = st.text_input("Occupation")
    contract_type = st.selectbox("Contract Type", ["Permanent", "Contract", "Freelancer", "Unemployed"])
    income = st.number_input("Monthly Net Income (€)", min_value=0, step=100)
    
    # Income validation
    if income < 0:
        st.error("Income must be a positive number or zero.")
        return
    else:
        income = int(income)

    work_mode = st.radio("Work Mode", ["Remote", "On-site", "Hybrid"])
    bio = st.text_area("Bio")
    hobbies = st.text_area("Hobbies")
    social_media = st.text_input("Social Media")

    # # Rental Preferences Inputs
    # rental_preferences()  # Call the rental preferences function

    # Save Profile Button
    if st.button("Save Profile"):
        # Mandatory field validation
        if not first_name or not surname:
            st.error("First Name and Surname are required fields.")
            return
        
        # Profile picture size validation
        if profile_pic and profile_pic.size > 5 * 1024 * 1024:  # 5 MB limit
            st.error("Profile picture size should be less than 5 MB.")
            return
        
        # Save renter profile to database
        profile_data = {
            "profile_pic": profile_pic.read() if profile_pic else None,  # Save as binary data
            "first_name": first_name,
            "surname": surname,
            "tagline": tagline,
            "age": age,
            "phone": phone,
            "nationality": nationality,
            "occupation": occupation,
            "contract_type": contract_type,
            "income": income,
            "work_mode": work_mode,
            "bio": bio,
            "hobbies": hobbies,
            "social_media": social_media
        }
        
        st.session_state["renter_profile"] = profile_data
        user_id = st.session_state.get("user_id")
        
        # Spinner for saving process
        with st.spinner("Saving your profile..."):
            try:
                profile_id = save_renter_profile_to_db(user_id, profile_data)

                # Check if profile_id is valid
                if not profile_id:
                    st.error("Failed to save profile. Profile ID is invalid.")
                    return
                
                # # Save rental preferences to database
                # rental_preferences_data = {
                #     "preferred_city": st.session_state.get("city", ""),
                #     "preferred_area": st.session_state.get("area", ""),
                #     "budget_min": st.session_state.get("budget_min", ""),
                #     "budget_max": st.session_state.get("budget_max", ""),
                #     "property_type": st.session_state.get("property_type", ""),
                #     "rooms_needed": st.session_state.get("rooms", ""),
                #     "num_people": st.session_state.get("num_people", ""),
                #     "move_in_date": st.session_state.get("move_in_date", ""),
                #     "pets": st.session_state.get("pets", ""),
                #     "pet_type": st.session_state.get("pet_type", ""),
                #     "lease_duration": st.session_state.get("lease_duration", "")
                # }
                
                # # Check if preferences data is valid
                # if not rental_preferences_data:
                #     st.error("Rental preferences are incomplete or missing.")
                #     return
                
                # # Save rental preferences
                # save_rental_preferences_to_db(profile_id, rental_preferences_data)
                # st.session_state["rental_preferences"] = rental_preferences_data

                st.success("Your profile has been created successfully!")
                st.session_state["current_page"] = "dashboard"
                
            except Exception as e:
                st.error("An error occurred while saving your profile.")
                print(f"Error: {e}")  # For debugging in the console/logs


if __name__ == "__main__":
    create_renter_profile()
