import streamlit as st
import uuid
from navigation_buttons import home_button, back_button 
from credit_score.credit_score import credit_score
# from recommendations.recommendation import recommendation_form
from database import save_renter_profile_to_db, save_rental_preferences_to_db

def create_renter_profile():
    
    st.title("Create Your Renter Profile")

    # Renter Profile Inputs
    profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"], key="create_profile_pic")
    name = st.text_input("Full Name")
    tagline = st.text_input("Tagline")
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    phone = st.text_input("Phone Number")
    if phone and (not phone.isdigit() or len(phone) != 10):
        st.error("Phone number must be 10 digits long and contain only numbers.")
    nationality = st.text_input("Nationality")
    occupation = st.text_input("Occupation")
    contract_type = st.selectbox("Contract Type", ["Permanent", "Contract", "Freelancer", "Unemployed"])
    income = st.number_input("Monthly Net Income (€)", min_value=0, step=100)
    work_mode = st.radio("Work Mode", ["Remote", "On-site", "Hybrid"])
    bio = st.text_area("Bio")
    hobbies = st.text_area("Hobbies")
    social_media = st.text_input("Social Media")

    # Rental Preferences Inputs
    preferred_city = st.text_input("Preferred City")
    preferred_area = st.text_input("Preferred Area")
    budget_min = st.number_input("Minimum Budget ($)", min_value=0, step=100)
    budget_max = st.number_input("Maximum Budget ($)", min_value=0, step=100)
    property_type = st.selectbox("Property Type", ["Apartment", "House", "Shared Accommodation"])
    rooms_needed = st.number_input("Number of Rooms", min_value=1, step=1)
    move_in_date = st.date_input("Move-in Date")
    pets = st.radio("Do you have pets?", ["No", "Yes"]) == "Yes"
    pet_type = st.text_input("Pet Type") if pets else None
    

    # Save Profile Button
    if st.button("Save Profile"):
        try:
            # Save renter profile to database
            profile_data = {
                "profile_pic": profile_pic.read() if profile_pic else None, # Read the file content if it exists
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
                "hobbies": hobbies,
                "social_media": social_media
            }
            
            # Generate a unique profile ID
            user_id = st.session_state.get("user_id")  # Assume user_id is in session_state
            profile_id = save_renter_profile_to_db(user_id, profile_data)

            # Save rental preferences to database
            preferences_data = {
                "preferred_city": preferred_city,
                "preferred_area": preferred_area,
                "budget_min": budget_min,
                "budget_max": budget_max,
                "property_type": property_type,
                "rooms_needed": rooms_needed,
                "move_in_date": move_in_date,
                "pets": pets,
                "pet_type": pet_type,
            }
            save_rental_preferences_to_db(profile_id, preferences_data)
            
            # save the session state of the profile
            st.session_state["profile_id"] = profile_id
            st.session_state["profile_pic"] = profile_pic
            st.session_state["name"] = name
            st.session_state["tagline"] = tagline
            st.session_state["age"] = age
            st.session_state["phone"] = phone
            st.session_state["nationality"] = nationality
            st.session_state["occupation"] = occupation
            st.session_state["contract_type"] = contract_type
            st.session_state["income"] = income
            st.session_state["work_mode"] = work_mode
            st.session_state["bio"] = bio
            st.session_state["hobbies"] = hobbies
            st.session_state["social_media"] = social_media
            st.session_state["preferred_city"] = preferred_city
            st.session_state["preferred_area"] = preferred_area
            st.session_state["budget_min"] = budget_min
            st.session_state["budget_max"] = budget_max
            st.session_state["property_type"] = property_type
            st.session_state["rooms_needed"] = rooms_needed
            st.session_state["move_in_date"] = move_in_date
            st.session_state["pets"] = pets
            st.session_state["pet_type"] = pet_type
            
            st.success("Your profile has been created successfully!")
            st.session_state["current_page"] = "dashboard"

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    create_renter_profile()

