import streamlit as st
from navigation_buttons import back_button
from database import load_agent_profile_from_db, save_agent_profile_to_db

def edit_agent_profile():
    
    back_button()
    
    agent_profile = st.session_state["agent_profile"]
    
    st.title("Edit Agent Profile")
    
    # handle profile pic
    uploaded_file = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])
    agent_profile_pic = uploaded_file.read() if uploaded_file else agent_profile["agent_profile_pic"]
    if agent_profile_pic:
        st.image(agent_profile_pic, caption="Current Agent Profile Picture", width=150)
        
    # Basic Information
    with st.expander("Basic Information"):
        first_name = st.text_input("First Name", value=agent_profile["first_name"])
        last_name = st.text_input("Last Name", value=agent_profile["last_name"])
        phone = st.text_input("Phone Number", value=agent_profile["phone"])
        
        if phone and (not phone.isdigit() or len(phone) not in (10, 12)):
            st.error("Phone number must be 10 or 12 digits long and contain only numbers.")
            return
        
        agency_name = st.text_input("Agency Name", value=agent_profile["agency_name"])
        agency_address = st.text_input("Agency Address", value=agent_profile["agency_address"])
        agency_website = st.text_input("Agency Website", value=agent_profile["agency_website"])
        social_media = st.text_input("Social Media", value=agent_profile["social_media"])
        
    # Work Details
    with st.expander("Work Details"):
        working_days = st.text_input("Working Days", value=agent_profile["working_days"])
        working_hours = st.text_input("Working Hours", value=agent_profile["working_hours"])
        preferred_communication = st.text_input("Preferred Communication Methods", value=agent_profile["preferred_communication"])
        
    # Professional Background
    with st.expander("Professional Background"):
        services = st.text_input("Services Offered", value=agent_profile["services"])
        languages = st.text_input("Languages Spoken", value=agent_profile["languages"])
        
    with st.expander("Additional Information"):
        mission_statement = st.text_area("Mission Statement", value=agent_profile["mission_statement"])
        
    # Save changes
    if st.button("Save Profile"):
        try:
            agent_profile_pic_data = (
                uploaded_file.read() if uploaded_file else agent_profile["agent_profile_pic"]
            )
            
            updated_profile_data = {
                "agent_profile_pic": agent_profile_pic_data,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "agency_name": agency_name,
                "agency_address": agency_address,
                "agency_website": agency_website,
                "social_media": social_media,
                "working_days": working_days,
                "working_hours": working_hours,
                "preferred_communication": preferred_communication,
                "services": services,
                "languages": languages,
                "mission_statement": mission_statement,
            }
            
            user_id = st.session_state["user_id"]
            with st.spinner("Saving changes..."):
                save_agent_profile_to_db(user_id=user_id, profile_data=updated_profile_data)
                
                st.session_state["agent_profile"] = updated_profile_data
                st.success("Profile updated successfully!")
                st.session_state["current_page"] = "dashboard"
        except Exception as e:
            st.error("An error occurred while updating your profile.")
            print(f"Error: {e}")
