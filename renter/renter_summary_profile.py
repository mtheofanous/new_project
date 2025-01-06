import streamlit as st
import uuid
from navigation_buttons import home_button, back_button, log_out_button
import streamlit.components.v1 as components
from PIL import Image

        
def renter_summary_profile():
    
    # if renter_profile is not created then go to create_renter_profile
    if "renter_profile" not in st.session_state:
        st.session_state["current_page"] = "create_renter_profile"
        
    else:
        
        renter_profile = st.session_state.get("renter_profile")

        profile_pic = renter_profile["profile_pic"]
        name = f"{renter_profile['first_name']} {renter_profile['surname']}"
        tagline = renter_profile["tagline"]
        # if status is not set then credit_score_verified is Not Verified
        if "status" not in st.session_state:
            st.session_state["status"] = "Not Verified"

        status = st.session_state.get("status")
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
            if status == "Verified":
                st.write("**Credit Score: Verified 🟢**")
            elif status == "Not Verified":
                st.write("**Credit Score: Not Verified 🔴**")
            else:
                st.write("**Credit Score: Pending ⏳**")
            st.write(f"**Recommendation Status:** {recommendation_status}")