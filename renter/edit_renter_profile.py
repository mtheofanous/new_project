import streamlit as st
import uuid
from navigation_buttons import home_button, back_button 
from renter.rental_preferences import rental_preferences
from credit_score.credit_score import credit_score
from database import save_renter_profile_to_db, save_rental_preferences_to_db

def edit_renter_profile():
    back_button()

    st.title("Edit Your Renter Profile")

    # Profile Header
    st.header("Profile Header")
    
    # Handle profile picture upload
    uploaded_file = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"], key="new_profile_pic")
    profile_pic = uploaded_file.read() if uploaded_file else st.session_state.get("profile_pic")
    if profile_pic:
        st.image(profile_pic, caption="Current Profile Picture", width=150)

    username = st.text_input("Username", value=st.session_state.get("user", ""), key="new_profile_username")
    name = st.text_input("Full Name", value=st.session_state.get("name", ""), key="new_profile_name")
    tagline = st.text_input("Tagline", value=st.session_state.get("tagline", ""), key="new_profile_tagline")

    # Personal Details
    with st.expander("Personal Details"):
        email = st.text_input("Email", value=st.session_state.get("email", ""), key="new_profile_email")
        age = st.number_input("Age", min_value=18, max_value=100, step=1, value=st.session_state.get("age", 18), key="new_profile_age")
        phone = st.text_input("Phone Number", value=st.session_state.get("phone", ""), key="new_profile_phone")
        nationality = st.text_input("Nationality", value=st.session_state.get("nationality", ""), key="new_profile_nationality")
        occupation = st.text_input("Occupation", value=st.session_state.get("occupation", ""), key="new_profile_occupation")
        contract_type = st.selectbox(
            "Contract Type",
            ["Permanent", "Contract", "Freelancer", "Unemployed"],
            index=["Permanent", "Contract", "Freelancer", "Unemployed"].index(st.session_state.get("contract_type", "Permanent")),
            key="new_profile_contract"
        )
        income = st.number_input("Monthly Income (€)", min_value=0, step=100, value=st.session_state.get("income", 0), key="new_profile_income")
        work_mode = st.radio(
            "Work Mode",
            ["Remote", "On-site", "Hybrid"],
            index=["Remote", "On-site", "Hybrid"].index(st.session_state.get("work_mode", "Remote")),
            key="new_profile_work_mode"
        )

    # Rental Preferences
    with st.expander("Rental Preferences"):
        city = st.text_input("Preferred City", value=st.session_state.get("preferred_city", ""), key="new_profile_city")
        area = st.text_input("Preferred Area", value=st.session_state.get("preferred_area", ""), key="new_profile_area")
        budget_min = st.number_input("Minimum Budget (€)", min_value=0, step=100, value=st.session_state.get("budget_min", 0), key="new_profile_budget_min")
        budget_max = st.number_input("Maximum Budget (€)", min_value=0, step=100, value=st.session_state.get("budget_max", 0), key="new_profile_budget_max")
        property_type = st.selectbox(
            "Property Type",
            ["Apartment", "House", "Shared Accommodation"],
            index=["Apartment", "House", "Shared Accommodation"].index(st.session_state.get("property_type", "Apartment")),
            key="new_profile_property_type"
        )
        rooms = st.number_input("Number of Rooms Needed", min_value=1, step=1, value=st.session_state.get("rooms_needed", 1), key="new_profile_rooms")
        num_people = st.number_input("Number of People", min_value=1, step=1, value=st.session_state.get("number_of_people", 1), key="new_profile_people")
        move_in_date = st.date_input("Move-in Date", value=st.session_state.get("move_in_date", None), key="new_profile_move_in_date")
        pets = st.radio("Do you have pets?", ["No", "Yes"], index=False if st.session_state.get("pets") == "No" else True, key="new_profile_pets")
        pet_type = st.text_input("Pet Type (if any)", value=st.session_state.get("pet_type", ""), key="new_profile_pet_type")

    # About Me
    with st.expander("About Me"):
        bio = st.text_area("Bio", value=st.session_state.get("bio", ""), key="new_profile_bio")
        hobbies = st.text_input("Hobbies & Interests (comma-separated)", value=st.session_state.get("hobbies", ""), key="new_profile_hobbies")

    # Save profile button
    if st.button("Save Profile", key="save_edit_profile"):
        try:
            # Save renter profile to database
            profile_data = {
                "profile_pic": uploaded_file.read() if uploaded_file else st.session_state.get("profile_pic"),
                "name": name,
                "tagline": tagline,
                "email": email,
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
            profile_id = save_renter_profile_to_db(user_id, profile_data)

            # Store profile_id in session state
            st.session_state["profile_id"] = profile_id

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
                "pets": pets,
                "pet_type": pet_type
            }
            save_rental_preferences_to_db(profile_id, preferences_data)
            
            # Update session state
            st.session_state["profile_pic"] = profile_pic
            st.session_state["name"] = name
            st.session_state["tagline"] = tagline
            st.session_state["email"] = email
            st.session_state["age"] = age
            st.session_state["phone"] = phone
            st.session_state["nationality"] = nationality
            st.session_state["occupation"] = occupation
            st.session_state["contract_type"] = contract_type
            st.session_state["income"] = income
            st.session_state["work_mode"] = work_mode
            st.session_state["bio"] = bio
            st.session_state["hobbies"] = hobbies
            st.session_state["preferred_city"] = city
            st.session_state["preferred_area"] = area
            st.session_state["budget_min"] = budget_min
            st.session_state["budget_max"] = budget_max
            st.session_state["property_type"] = property_type
            st.session_state["rooms_needed"] = rooms
            st.session_state["number_of_people"] = num_people
            st.session_state["move_in_date"] = move_in_date
            st.session_state["pets"] = pets
            st.session_state["pet_type"] = pet_type
            
            st.success("Your renter profile has been updated successfully!")
            st.session_state["current_page"] = "dashboard"

        except Exception as e:
            st.error(f"An error occurred while updating your profile: {e}")



if __name__ == "__main__":
    edit_renter_profile()
