import streamlit as st
from queries.landlord import *
from queries.user import load_user_from_db

# landlord_summary_profile
def landlord_summary_profile():
    
    if "landlord_profile" not in st.session_state:
        st.session_state["current_page"] = "create_landlord_profile"
        st.error("Please create your landlord profile.")
        st.rerun()
        
    else:
        
        user_id = st.session_state.get("user_id", None)
        
        user = load_user_from_db(user_id)
    
        landlord_profile = st.session_state.get("landlord_profile")
        
        landlord_profile_pic = landlord_profile["landlord_profile_pic"]
        
        # Profile Summary
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if landlord_profile_pic:
                st.image(landlord_profile_pic, width=200)
            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("👁️", key="view_full_profile_button"):
                    st.session_state["current_page"] = "landlord_full_profile"
            with c2:
                if st.button("✏️", key="edit_profile_button"):
                    st.session_state["current_page"] = "edit_landlord_profile"
        with col2:
            st.write(f"**Username:** {user['username']}")
            st.write(f"**About me:** {landlord_profile['about_me']}")
            st.write(f"**Social Media:** {landlord_profile['social_media']}")
if __name__ == "__main__":
    landlord_summary_profile()
    