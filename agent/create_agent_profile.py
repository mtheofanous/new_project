import streamlit as st
from navigation_buttons import home_button 
import overpy
from queries.agent import save_agent_profile_to_db

def create_agent_profile():
    home_button()

    st.title("Create Rental Agent Profile")

    # Collect agent's basic profile information
    with st.expander("Basic Information"):
        agent_profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"], key="create_agent_profile_pic")
        agency_name = st.text_input("Agency Name:")
        phone = st.text_input("Phone Number:")
        
        # Phone number validation
        if phone and (not phone.isdigit() or len(phone) not in (10, 12)):
            st.error("Phone number must be 10 or 12 digits long and contain only numbers.")
            return

        agency_address = st.text_input("Agency Address:")
        agency_website = st.text_input("Agency Website (optional):")
        social_media = st.text_input("Social Media Link (optional):")

    with st.expander("Work Details"):
        working_days = st.text_input("Working Days:", "Monday - Friday")
        working_hours = st.text_input("Working Hours:", "9:00 AM - 5:00 PM")
        preferred_communication = st.text_input("Preferred Communication Methods:", "Email, Phone")

    with st.expander("Professional Background"):
        services = st.text_input("Services Offered:", "Tenant Matching, Landlord Support, Lease Preparation")
        languages = st.text_input("Languages Spoken:", "English, Greek")

    with st.expander("Additional Information"):
        mission_statement = st.text_area("Mission Statement (optional):")

    # Save Profile Button
    if st.button("Save Profile"):
        
        # Mandatory field validation
        if not agency_name or not phone:
            st.error("Agency Name, and Phone Number are required fields.")
            return
        
        # Profile picture size validation
        if agent_profile_pic and agent_profile_pic.size > 5 * 1024 * 1024:
            st.error("Profile picture size should be less than 5 MB.")
            return
        
        # Build the profile dictionary
        agent_profile = {
            "phone": phone,
            "agent_profile_pic": agent_profile_pic.read() if agent_profile_pic else None,
            "agency_name": agency_name,
            "agency_address": agency_address,
            "agency_website": agency_website,
            "social_media": social_media,
            "working_days": working_days,
            "working_hours": working_hours,
            "preferred_communication": preferred_communication,
            "services": services,
            "languages": languages,
            "mission_statement": mission_statement
        }

        # Save the profile to the database
        st.session_state["agent_profile"] = agent_profile
        user_id = st.session_state["user_id"]
        
        with st.spinner("Saving Profile..."):
            try:
                agent_profile_id = save_agent_profile_to_db(user_id, agent_profile)
                
                if not agent_profile_id:
                    st.error("Failed to save profile. Please try again.")
                    return
                
                st.success("Profile saved successfully!")
                st.session_state["current_page"] = "dashboard"
            except Exception as e:
                st.error(f"An error occurred: {e}")
                print(f"Error: {e}")
        

if __name__ == "__main__":
    create_agent_profile()
