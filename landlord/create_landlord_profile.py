import streamlit as st
from navigation_buttons import home_button 
import overpy
from queries.landlord import save_landlord_profile_to_db

def create_landlord_profile():
    home_button()

    st.title("Create Landlord Profile")

    # Collect landlords's basic profile information
    with st.expander("Basic Information"):
        landlord_profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"], key="create_agent_profile_pic")
        phone = st.text_input("Phone Number:")
        
        # Phone number validation
        if phone and (not phone.isdigit() or len(phone) not in (10, 12)):
            st.error("Phone number must be 10 or 12 digits long and contain only numbers.")
            return

        social_media = st.text_input("Social Media Link (optional):")
        preferred_communication = st.text_input("Preferred Communication Methods:", "Email, Phone")
        languages = st.text_input("Languages Spoken:", "English, Greek")

    with st.expander("Additional Information"):
        about_me  = st.text_area("about_me (optional):")

    # Save Profile Button
    if st.button("Save Profile"):
        
        # Mandatory field validation
        if not phone:
            st.error("Phone Number are required fields.")
            return
        
        # Profile picture size validation
        if landlord_profile_pic and landlord_profile_pic.size > 5 * 1024 * 1024:
            st.error("Profile picture size should be less than 5 MB.")
            return
        
        # Build the profile dictionary
        landlord_profile = {
            "phone": phone,
            "landlord_profile_pic": landlord_profile_pic.read() if landlord_profile_pic else None,
            "social_media": social_media,
            "preferred_communication": preferred_communication,
            "languages": languages,
            "about_me": about_me
        }

        # Save the profile to the database
        st.session_state["landlord_profile"] = landlord_profile
        user_id = st.session_state["user_id"]
        
        with st.spinner("Saving Profile..."):
            try:
                landlord_profile_id = save_landlord_profile_to_db(user_id, landlord_profile)
                
                if not landlord_profile_id:
                    st.error("Failed to save profile. Please try again.")
                    return
                
                st.success("Profile saved successfully!")
                
                st.session_state["current_page"] = "dashboard"
                st.rerun()
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
                print(f"Error: {e}")
        

if __name__ == "__main__":
    create_landlord_profile()
