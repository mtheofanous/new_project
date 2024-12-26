import streamlit as st
import uuid
from navigation_buttons import home_button, back_button, log_out_button
import streamlit.components.v1 as components
from PIL import Image

def renter_full_profile():
    
    back_button()
    
    profile_pic = st.session_state.get("profile_pic", "")
    username = st.session_state.get("username", "")
    name = st.session_state.get("name", "")
    tagline = st.session_state.get("tagline", "")
    email = st.session_state.get("email", "")
    age = st.session_state.get("age", "")
    phone = st.session_state.get("phone", "")
    nationality = st.session_state.get("national", "")
    occupation = st.session_state.get("occupation", "")
    contract_type = st.session_state.get("contract_type", "")
    work_mode = st.session_state.get("work_mode", "")
    city = st.session_state.get("city", "")
    area = st.session_state.get("area", "")
    budget_min = st.session_state.get("budget_min", "")
    budget_max = st.session_state.get("budget_max", "")
    property_type = st.session_state.get("property_type", "")
    rooms = st.session_state.get("rooms", "")
    num_people = st.session_state.get("num_people", "")
    move_in_date = st.session_state.get("move_in_date", "")
    lease_duration = st.session_state.get("lease_duration", "")
    pets = st.session_state.get("pets", "")
    pet_type = st.session_state.get("pet_type", "")
    bio = st.session_state.get("bio", "")
    hobbies = st.session_state.get("hobbies", "")
    income = st.session_state.get("income", "")
    uploaded_credit_score = st.session_state.get("uploaded_credit_score", "")
    credit_score_verified = st.session_state.get("status", "")
    landlord_name = st.session_state.get("landlord_name", "")
    landlord_email = st.session_state.get("landlord_email", "")
    landlord_phone = st.session_state.get("landlord_phone", "")
    recommendation_status = st.session_state.get("recommendation_status", "")
    recommendation_form = st.session_state.get("recommendation_form", "")
    
    st.title("Full Profile")

    # Profile Columns
    col1, col2 = st.columns(2)

    with col1:
        if profile_pic:
            st.image(profile_pic, width=200)
        st.markdown(f"##### **Name:** {name}")
        st.markdown(f"##### **Email:** {email}")
        st.markdown(f"##### **Age:** {age}")
        st.markdown(f"##### **Phone:** {phone}")
        st.markdown(f"##### **Nationality:** {nationality}")
        st.markdown(f"##### **Occupation:** {occupation}")
        st.markdown(f"##### **Contract Type:** {contract_type}")
        st.markdown(f"##### **Work Mode:** {work_mode}")

    with col2:
        st.markdown(f"##### **City:** {city}")
        st.markdown(f"##### **Area:** {area}")
        st.markdown(f"##### **Budget Range:** €{budget_min} - €{budget_max}")
        st.markdown(f"##### **Property Type:** {property_type}")
        st.markdown(f"##### **Rooms:** {rooms}")
        st.markdown(f"##### **Number of People:** {num_people}")
        st.markdown(f"##### **Move-in Date:** {move_in_date}")
        st.markdown(f"##### **Lease Duration:** {lease_duration}")
        st.markdown(f"##### **Pets:** {pets}")
        st.markdown(f"##### **Pet Type:** {pet_type}")

    st.markdown("---")

    # Additional Information
    st.subheader("Additional Information")

    st.markdown(f"##### **Bio:** {bio}")
    st.markdown(f"##### **Hobbies:** {hobbies}")
    st.markdown(f"##### **Income:** €{income}")
    if credit_score_verified == "Verified":
        st.markdown("##### **Credit Score verified 🟢**")
    elif credit_score_verified == "Not Verified":
        st.markdown("##### **Credit score not verified 🔴**")
    elif credit_score_verified == "Pending":
        st.markdown("##### **Credit score verification pending ⏳**")
    st.markdown(f"##### **Recommendation Status:** {recommendation_status}")

    st.markdown("---")
        
if __name__ == "__main__":
    renter_full_profile()