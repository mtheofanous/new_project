import streamlit as st
from navigation_buttons import back_button
from queries.landlord import *
from queries.user import load_user_from_db
def landlord_full_profile():
    
    back_button()
    
    user_id = st.session_state.get("user_id", None)
    
    user = load_user_from_db(user_id)
    
    landlord_profile = load_landlord_profile_from_db(user_id)
    
    landlord_profile = st.session_state["landlord_profile"]
    
    st.title("landlord Profile")
    
    st.markdown("---")
    
    # Profile Columns
    col1, col2 = st.columns(2)
    
    with col1:
        if landlord_profile["landlord_profile_pic"]:
            st.image(landlord_profile["landlord_profile_pic"], width=200)
        st.markdown(f"##### **Username:** {user['username']}")
        st.markdown(f"##### **Phone:** {landlord_profile['phone']}")
        st.markdown(f"##### **Social Media:** {landlord_profile['social_media']}")
    
        st.markdown(f"##### **Preferred Communication:** {landlord_profile['preferred_communication']}")
        
        st.markdown(f"##### **Languages Spoken:** {landlord_profile['languages']}")
        
        # Additional Information
        st.subheader("Additional Information")
        st.markdown(f"##### **Abour me:** {landlord_profile['about_me']}")
        
    st.markdown("---")
    
    # Edit Profile Button
    if st.button("Edit Profile"):
        st.session_state["current_page"] = "edit_landlord_profile"
        
if __name__ == "__main__":
    landlord_full_profile()