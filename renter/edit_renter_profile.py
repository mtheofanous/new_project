import streamlit as st
import uuid
from navigation_buttons import home_button, back_button 
from renter.rental_preferences import rental_preferences
from database import save_renter_profile_to_db, save_rental_preferences_to_db

def edit_renter_profile():
    back_button()
    
    renter_profile = st.session_state["renter_profile"]
    # preferences_data = st.session_state["rental_preferences"]

    st.title("Edit Your Renter Profile")

    # Profile Header
    st.header("Profile Header")
    
    # Handle profile picture upload
    uploaded_file = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"], key="new_profile_pic")
    profile_pic = uploaded_file.read() if uploaded_file else renter_profile["profile_pic"]
    if profile_pic:
        st.image(profile_pic, caption="Current Profile Picture", width=150)

    first_name = st.text_input("First Name", value=renter_profile["first_name"], key="new_profile_first_name")
    surname = st.text_input("Surname", value=renter_profile["surname"], key="new_profile_name")
    tagline = st.text_input("Tagline", value=renter_profile["tagline"], key="new_profile_tagline")

    # Personal Details
    with st.expander("Personal Details"):
        age = st.number_input("Age", min_value=18, max_value=100, step=1, value=renter_profile['age'], key="new_profile_age")
        phone = st.text_input("Phone Number", value=renter_profile['phone'], key="new_profile_phone")
        social_media = st.text_input("Social Media", value=renter_profile['social_media'], key="new_profile_social_media")
        nationality = st.text_input("Nationality", value=renter_profile['nationality'], key="new_profile_nationality")
        occupation = st.text_input("Occupation", value=renter_profile["occupation"], key="new_profile_occupation")
        contract_type = st.selectbox(
            "Contract Type",
            ["Permanent", "Contract", "Freelancer", "Unemployed"],
            index=["Permanent", "Contract", "Freelancer", "Unemployed"].index(renter_profile["contract_type"]),
            key="new_profile_contract"
        )
        income = st.number_input("Monthly Income (€)", min_value=0, step=100, value=(int(renter_profile["income"])), key="new_profile_income")
        work_mode = st.radio(
            "Work Mode",
            ["Remote", "On-site", "Hybrid"],
            index=["Remote", "On-site", "Hybrid"].index(renter_profile["work_mode"]),
            key="new_profile_work_mode"
        )

    # # Rental Preferences (call rental_preferences function)
    # with st.expander("Rental Preferences"):
    #     rental_preferences()  # This will load the rental preferences form for editing.

    # About Me
    with st.expander("About Me"):
        bio = st.text_area("Bio", value=renter_profile["bio"], key="new_profile_bio")
        hobbies = st.text_input("Hobbies & Interests (comma-separated)", value=renter_profile["hobbies"], key="new_profile_hobbies")

    # Save profile button
    if st.button("Save Profile", key="save_edit_profile"):
        try:
            # Read uploaded file content or fallback to session state
            profile_pic_data = (
                uploaded_file.read() if uploaded_file else renter_profile.get("profile_pic", None)
            )

            # Collect updated profile data
            updated_profile_data = {
                "profile_pic": profile_pic_data,
                "first_name": st.session_state.get("new_profile_first_name", ""),
                "surname": st.session_state.get("new_profile_name", ""),
                "tagline": st.session_state.get("new_profile_tagline", ""),
                "age": st.session_state.get("new_profile_age", 0),
                "phone": st.session_state.get("new_profile_phone", ""),
                "nationality": st.session_state.get("new_profile_nationality", ""),
                "occupation": st.session_state.get("new_profile_occupation", ""),
                "contract_type": st.session_state.get("new_profile_contract", ""),
                "income": st.session_state.get("new_profile_income", 0),
                "work_mode": st.session_state.get("new_profile_work_mode", ""),
                "bio": st.session_state.get("new_profile_bio", ""),
                "hobbies": st.session_state.get("new_profile_hobbies", ""),
                "social_media": st.session_state.get("new_profile_social_media", ""),
            }

            # # Collect updated rental preferences data from session state
            # updated_preferences_data = {
            #     "preferred_city": st.session_state.get("new_profile_city", ""),
            #     "preferred_area": st.session_state.get("new_profile_areas", ""),
            #     "budget_min": st.session_state["rental_preferences"]["budget_min"],
            #     "budget_max": st.session_state["rental_preferences"]["budget_max"],
            #     "property_type": st.session_state.get("new_profile_property_type", ""),
            #     "rooms_needed": st.session_state.get("new_profile_rooms", ""),
            #     "num_people": st.session_state.get("new_profile_people", ""),
            #     "move_in_date": st.session_state.get("new_profile_move_in", ""),
            #     "pets": st.session_state.get("new_profile_pets", ""),
            #     "pet_type": st.session_state.get("new_profile_pet_type", ""),
            #     "lease_duration": st.session_state.get("new_profile_lease_duration", "")
            # }

            # Save updated renter profile data to the database
            user_id = st.session_state.get("user_id")
            with st.spinner("Updating your profile..."):
                save_renter_profile_to_db(user_id, updated_profile_data)

                # Save updated rental preferences to the database
                # profile_id = st.session_state.get("profile_id")  # Assuming profile ID is available
                # save_rental_preferences_to_db(profile_id, updated_preferences_data)

                st.session_state["renter_profile"] = updated_profile_data
                # st.session_state["rental_preferences"] = updated_preferences_data

                st.success("Your profile has been updated successfully!")
                st.session_state["current_page"] = "dashboard"

        except Exception as e:
            st.error("An error occurred while updating your profile.")
            print(f"Error: {e}")
