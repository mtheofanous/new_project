import streamlit as st
from navigation_buttons import back_button
from database import load_agent_profile_from_db, save_agent_profile_to_db

def edit_agent_profile():
    
    back_button()
    
    agent_profile = load_agent_profile_from_db(user_id=st.session_state["user_id"])
    
    st.title("Edit Agent Profile")
    
    # handle profile pic
    uploaded_file = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])
    agent_profile_pic = uploaded_file.read() if uploaded_file else agent_profile["agent_profile_pic"]
    if agent_profile_pic:
        st.image(agent_profile_pic, caption="Current Profile Picture", width=150)
    
    # Collecting profile data
    profile_data = {
        "agent_profile_pic": agent_profile_pic,
        "name": st.text_input("Name", value=agent_profile["name"]),
        "phone": st.text_input("Phone Number", value=agent_profile["phone"]),
        "agency_name": st.text_input("Agency Name", value=agent_profile["agency_name"]),
        "agency_address": st.text_input("Agency Address", value=agent_profile["agency_address"]),
        "agency_website": st.text_input("Agency Website", value=agent_profile["agency_website"]),
        "social_media": st.text_input("Social Media", value=agent_profile["social_media"]),
        "working_days": st.text_input("Working Days", value=agent_profile["working_days"]),
        "working_hours": st.text_input("Working Hours", value=agent_profile["working_hours"]),
        "preferred_communication": st.text_input("Preferred Communication", value=agent_profile["preferred_communication"]),
        "services": st.text_area("Services Offered", value=agent_profile["services"]),
        "languages": st.text_input("Languages", value=agent_profile["languages"]),
        "mission_statement": st.text_area("Mission Statement", value=agent_profile["mission_statement"])
    }
    
    # Save changes
    if st.button("Save Changes"):
        save_agent_profile_to_db(
            user_id=st.session_state["user_id"], 
            profile_data=profile_data  # Pass the profile data as a dictionary
        )
        st.success("Profile updated successfully!")
        st.session_state["current_page"] = "dashboard"