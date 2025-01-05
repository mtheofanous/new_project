import streamlit as st
import uuid
from navigation_buttons import home_button, back_button, log_out_button
import streamlit.components.v1 as components
from renter.rental_preferences import rental_preferences
from PIL import Image

def renter_full_profile():
    
    back_button()
    
 
    # rental_preferences_data = rental_preferences()
    
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
        st.markdown(f"##### **Name:** {renter_profile['first_name']} {renter_profile['surname']}")
        st.markdown(f"##### **Email:** {email}")
        st.markdown(f"##### **Age:** {renter_profile['age']}")
        st.markdown(f"##### **Phone:** {renter_profile['phone']}")
        st.markdown(f"##### **Social Media:** {renter_profile['social_media']}")
        st.markdown(f"##### **Nationality:** {renter_profile['nationality']}")
        st.markdown(f"##### **Occupation:** {renter_profile['occupation']}")
        st.markdown(f"##### **Contract Type:** {renter_profile['contract_type']}")
        st.markdown(f"##### **Income:** €{renter_profile['income']}")
        st.markdown(f"##### **Work Mode:** {renter_profile['work_mode']}")

    # with col2:
    #     st.markdown(f"##### **City:** {rental_preferences_data['preferred_city']}")
    #     st.markdown(f"##### **Area:** {rental_preferences_data['preferred_area']}")
    #     st.markdown(f"##### **Budget Range:** €{rental_preferences_data['budget_min']} - €{rental_preferences_data['budget_max']}")
    #     st.markdown(f"##### **Property Type:** {rental_preferences_data['property_type']}")
    #     st.markdown(f"##### **Rooms:** {rental_preferences_data.get('rooms_needed')}")
    #     st.markdown(f"##### **Number of People:** {rental_preferences_data.get('num_people')}")
    #     st.markdown(f"##### **Move-in Date:** {rental_preferences_data['move_in_date']}")
    #     st.markdown(f"##### **Lease Duration:** {rental_preferences_data['lease_duration']}")
    #     st.markdown(f"##### **Pets:** {rental_preferences_data['pets']}")
    #     st.markdown(f"##### **Pet Type:** {rental_preferences_data['pet_type']}")
    
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

    
        
if __name__ == "__main__":
    renter_full_profile()