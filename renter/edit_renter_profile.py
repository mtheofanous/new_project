import streamlit as st
import uuid
from navigation_buttons import back_button 
from queries.renter import save_renter_profile_to_db

def edit_renter_profile():
    
    back_button()
    
    renter_profile = st.session_state["renter_profile"]

    user_id = st.session_state.get("user_id", None)
    
    
    st.title("Edit Your Renter Profile")

    # Profile Header
    st.header("Profile Header")
    
    # Handle profile picture upload
    uploaded_file = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"], key="new_profile_pic")
    profile_pic = uploaded_file.read() if uploaded_file else renter_profile["profile_pic"]
    if profile_pic:
        st.image(profile_pic, caption="Current Renter Profile Picture", width=150)

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


    # About Me
    with st.expander("About Me"):
        bio = st.text_area("Bio", value=renter_profile["bio"], key="new_profile_bio")
        hobbies = st.text_input("Hobbies & Interests (comma-separated)", value=renter_profile["hobbies"], key="new_profile_hobbies")

    # Save profile button
    if st.button("Save Profile", key="save_edit_profile"):
        try:
            # Read uploaded file content or fallback to session state
            renter_profile_pic_data = (
                uploaded_file.read() if uploaded_file else renter_profile.get("profile_pic", None)
            )

            # Collect updated profile data
            updated_profile_data = {
                "profile_pic": renter_profile_pic_data,
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
                "social_media": social_media,
            }


            # Save updated renter profile data to the database
            user_id = st.session_state["user_id"]
            with st.spinner("Updating your profile..."):
                save_renter_profile_to_db(user_id, updated_profile_data)

                st.session_state["renter_profile"] = updated_profile_data

                st.success("Your profile has been updated successfully!")
                st.session_state["current_page"] = "dashboard"

        except Exception as e:
            st.error("An error occurred while updating your profile.")
            print(f"Error: {e}")

if __name__ == "__main__":
    edit_renter_profile()