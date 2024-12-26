import streamlit as st
from navigation_buttons import home_button 
import overpy
from database import load_user_from_db, save_agent_profile_to_db

def create_agent_profile():
    home_button()

    st.title("Create Rental Agent Profile")

    # Collect agent's basic profile information
    with st.expander("Basic Information"):
        name = st.text_input("Full Name:")
        phone = st.text_input("Phone Number:")
        agent_profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"], key="create_agent_profile_pic")
        agency_name = st.text_input("Agency Name:")
        agency_address = st.text_input("Agency Address:")
        agency_website = st.text_input("Agency Website (optional):")
        social_media = st.text_input("Social Media Link (optional):")

    with st.expander("Work Details"):
        working_days = st.multiselect("Working Days:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], default=["Monday", "Friday"])
        working_hours = st.slider("Working Hours:", 0, 24, (9, 17), format="%d:00")
        preferred_communication = st.multiselect("Preferred Communication Methods:", ["Phone", "Email", "Text", "In-person"], default=["Phone", "Email"])

    with st.expander("Professional Background"):
        services = st.multiselect("Services Offered:", ["Tenant Matching", "Landlord Support", "Lease Management", "Market Analysis"], default=["Tenant Matching"])
        languages = st.multiselect("Languages Spoken:", ["English", "Greek", "Italian","Spanish", "French", "Russian","Mandarin", "Arabic"], default=["English"])

    with st.expander("Additional Information"):
        mission_statement = st.text_area("Mission Statement (optional):")

    if st.button("Save Profile"):
        # Build the profile dictionary
        agent_profile = {
            "name": name,
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
            "mission_statement": mission_statement.strip()
        }

        # Save the profile to the database
        user_id = st.session_state.get("user_id")
        save_agent_profile_to_db(user_id, agent_profile)
        
        st.success("Profile saved successfully!")
        st.session_state["current_page"] = "dashboard"
        

if __name__ == "__main__":
    create_agent_profile()
