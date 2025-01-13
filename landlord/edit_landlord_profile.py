import streamlit as st
from navigation_buttons import back_button
from queries.landlord import *

def edit_landlord_profile():
    
    back_button()
    
    landlord_profile = st.session_state["landlord_profile"]
    
    st.title("Edit landlord Profile")
    
    # handle profile pic
    uploaded_file = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])
    landlord_profile_pic = uploaded_file.read() if uploaded_file else landlord_profile["landlord_profile_pic"]
    if landlord_profile_pic:
        st.image(landlord_profile_pic, caption="Current landlord Profile Picture", width=150)
        
    # Basic Information
    with st.expander("Basic Information"):
        phone = st.text_input("Phone Number", value=landlord_profile["phone"])
        
        if phone and (not phone.isdigit() or len(phone) not in (10, 12)):
            st.error("Phone number must be 10 or 12 digits long and contain only numbers.")
            return
        
        social_media = st.text_input("Social Media", value=landlord_profile["social_media"])
        
        preferred_communication = st.text_input("Preferred Communication Methods", value=landlord_profile["preferred_communication"])
        
        
    with st.expander("Additional Information"):
        about_me = st.text_area("Mission Statement", value=landlord_profile["about_me"])
        languages = st.text_input("Languages Spoken", value=landlord_profile["languages"])
        
    # Save changes
    if st.button("Save Profile"):
        try:
            landlord_profile_pic_data = (
                uploaded_file.read() if uploaded_file else landlord_profile["landlord_profile_pic"]
            )
            
            updated_profile_data = {
                "landlord_profile_pic": landlord_profile_pic_data,
                "phone": phone,
                "social_media": social_media,
                "preferred_communication": preferred_communication,
                "languages": languages,
                "about_me": about_me,
            }
            
            user_id = st.session_state["user_id"]
            with st.spinner("Saving changes..."):
                save_landlord_profile_to_db(user_id=user_id, profile_data=updated_profile_data)
                
                st.session_state["landlord_profile"] = updated_profile_data
                st.success("Profile updated successfully!")
                st.session_state["current_page"] = "dashboard"
        except Exception as e:
            st.error("An error occurred while updating your profile.")
            print(f"Error: {e}")
