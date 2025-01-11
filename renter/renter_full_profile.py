import streamlit as st
import uuid
from navigation_buttons import home_button, back_button, log_out_button
import streamlit.components.v1 as components
from PIL import Image

def renter_full_profile():
    
    back_button()
    
    renter_profile = st.session_state["renter_profile"]
    
    email = st.session_state.get("email", "")
    credit_score_verified = st.session_state.get("status", "")
    recommendation_status = st.session_state.get("recommendation_status", "")
    
    st.title("Full Profile")
    
    st.markdown("---")

    # Profile Columns
    col1, col2 = st.columns(2)

    with col1:
        if renter_profile["profile_pic"]:
            st.image(renter_profile["profile_pic"], width=200)
        st.markdown(f"##### **Name:** {renter_profile['first_name']} {renter_profile['last_name']}")
        st.markdown(f"##### **Email:** {email}")
        st.markdown(f"##### **Age:** {renter_profile['age']}")
        st.markdown(f"##### **Phone:** {renter_profile['phone']}")
        st.markdown(f"##### **Social Media:** {renter_profile['social_media']}")
        st.markdown(f"##### **Nationality:** {renter_profile['nationality']}")
        st.markdown(f"##### **Occupation:** {renter_profile['occupation']}")
        st.markdown(f"##### **Contract Type:** {renter_profile['contract_type']}")
        st.markdown(f"##### **Income:** €{renter_profile['income']}")
        st.markdown(f"##### **Work Mode:** {renter_profile['work_mode']}")


    with col2:
        # Additional Information
        st.subheader("Additional Information")
        st.markdown(f"##### **Tagline:** {renter_profile['tagline']}")
        st.markdown(f"##### **Bio:** {renter_profile['bio']}")
        st.markdown(f"##### **Hobbies:** {renter_profile['hobbies']}")
        
        if credit_score_verified == "Verified":
            st.markdown("##### **Credit Score verified 🟢**")
        elif credit_score_verified == "Not Verified":
            st.markdown("##### **Credit score not verified 🔴**")
        elif credit_score_verified == "Pending":
            st.markdown("##### **Credit score verification pending ⏳**")
        st.markdown(f"##### **Recommendation Status:** {recommendation_status}")

    

    st.markdown("---")
    
    # Edit Profile Button
    if st.button("Edit Profile"):
        st.session_state["current_page"] = "edit_renter_profile"

        
if __name__ == "__main__":
    renter_full_profile()