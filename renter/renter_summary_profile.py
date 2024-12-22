import streamlit as st
import uuid
from navigation_buttons import home_button, back_button, log_out_button
import streamlit.components.v1 as components
from PIL import Image

        
def renter_summary_profile():

    profile_pic = st.session_state.get("profile_pic", "")
    name = st.session_state.get("name", "")
    tagline = st.session_state.get("tagline", "")
    email = st.session_state.get("email", "")
    phone = st.session_state.get("phone", "")
    city = st.session_state.get("city", "")
    area = st.session_state.get("area", "")
    budget_min = st.session_state.get("budget_min", "")
    budget_max = st.session_state.get("budget_max", "")
    credit_score_verified = st.session_state.get("credit_score_verified", "")
    recommendation_status = st.session_state.get("recommendation_status", "")
    
    # Profile Summary
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if profile_pic:
            st.image(profile_pic, width=200)
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("👁️", key="view_full_profile_button"):
                st.session_state["current_page"] = "renter_full_profile"
        with c2:
            if st.button("✏️", key="edit_profile_button"):
                st.session_state["current_page"] = "edit_renter_profile"
    with col2:

        st.write(f"**Name:** {name}")
        st.write(f"**Tagline:** {tagline}")
        if credit_score_verified == True:
            st.markdown("**Credit Score verified ✅**")
        elif credit_score_verified == False:
            st.markdown("**Credit score not verified ❌**")
        st.write(f"**Recommendation Status:** {recommendation_status}")