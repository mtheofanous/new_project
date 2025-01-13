import streamlit as st
import uuid
import streamlit.components.v1 as components
from PIL import Image
from queries.renter import load_credit_scores, load_renter_profile_from_db
from queries.user import load_user_from_db
from renter.renter_full_profile import display_renter_full_profile

def display_renter_summary_profile(user_id):
    
    user = load_user_from_db(user_id)
    
    renter_profile = load_renter_profile_from_db(user_id)
    
    credit_score = load_credit_scores(user_id)
    
    credit_score_verified = credit_score["status"] if credit_score else "Not Verified"
    
    profile_pic = renter_profile["profile_pic"]

    recommendation_status = st.session_state.get("recommendation_status", "")
    
    # Profile Summary
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        with st.container(border=True):
            if profile_pic:
                st.image(profile_pic, width=200)
                toggle_key = f"renter_full_profile_{user['username']}"

    with col2:

        st.write(f"**Username:** {user['username']}")
        st.write(f"**Tagline:** {renter_profile['tagline']}")
        if credit_score_verified == "Verified":
            st.write("**Credit Score: Verified 🟢**")
        elif credit_score_verified == "Not Verified":
            st.write("**Credit Score: Not Verified 🔴**")
        else:
            st.write("**Credit Score: Pending ⏳**")
        st.write(f"**Recommendation Status:** {recommendation_status}")
    if toggle_key not in st.session_state:
        st.session_state[toggle_key] = False
        
    if st.button("View Full Profile", key=f'{toggle_key}_button'):
        # Toggle the display of the full profile
        st.session_state[toggle_key] = not st.session_state[toggle_key]
        
    if st.session_state[toggle_key]:
        display_renter_full_profile(user['id'])

        
def renter_summary_profile():
    
    # if renter_profile is not created then go to create_renter_profile
    if "renter_profile" not in st.session_state:
        st.session_state["current_page"] = "create_renter_profile"
        st.rerun()
        
    else:
        
        user_id = st.session_state.get("user_id", None)
        
        display_renter_summary_profile(user_id)
    
