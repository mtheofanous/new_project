import streamlit as st
import uuid
from navigation_buttons import back_button
from queries.renter import load_renter_profile_from_db, load_credit_scores, load_rental_preferences_from_db
from queries.user import load_user_from_db

def display_renter_full_profile(user_id):
    
    user = load_user_from_db(user_id)
    
    renter_profile = load_renter_profile_from_db(user_id)
    
    rental_info = load_rental_preferences_from_db(user_id)
    
    profile_pic = renter_profile["profile_pic"] if renter_profile else None 
    
    pet = rental_info["pet_type"] if rental_info else "No pets"
    
    budget_range = (
        f"€{rental_info['budget_min']} - €{rental_info['budget_max']}"
        if rental_info and rental_info.get("budget_min") and rental_info.get("budget_max")
        else "No specified budget"
    )
    
    number_of_people = rental_info["number_of_people"] if rental_info else "Not specified"
    
    move_in_date = rental_info["move_in_date"] if rental_info else "Not specified"
    
        
    credit_score = load_credit_scores(user_id)
    
    credit_score_verified = credit_score["status"] if credit_score else "Not Verified"
    
    recommendation_status = st.session_state.get("recommendation_status", "")
    
    st.title("Full Profile")
    
    st.markdown("---")
    
    # Define CSS for LinkedIn-style design
    st.markdown(
        """
        <style>
        
        /* Profile picture styling */
        .profile-picture {
            border-radius: 50%;
            width: 150px;
            height: 150px;
            object-fit: cover;
            margin-bottom: 20px;
        }

        /* Header section for name and tagline */
        .profile-header {
            text-align: left;
            margin-bottom: 20px;
        }
        .profile-header h2 {
            font-size: 28px;
            color: #2C3E50;
            margin-bottom: 5px;
        }
        .profile-header h4 {
            font-size: 18px;
            color: #7F8C8D;
            margin-bottom: 15px;
        }

        /* Section headers */
        .section-header {
            font-size: 20px;
            font-weight: bold;
            color: #34495E;
            margin-top: 20px;
            margin-bottom: 10px;
            border-bottom: 2px solid #EAEDED;
            padding-bottom: 5px;
        }

        /* Info rows */
        .info-row {
            font-size: 16px;
            color: #34495E;
            margin-bottom: 10px;
        }
        .info-row strong {
            font-weight: bold;
        }

        /* Additional info like credit score */
        .additional-info {
            margin-top: 15px;
            font-size: 16px;
        }
        .credit-score {
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
        }
        .credit-score.verified {
            color: #27AE60;
        }
        .credit-score.not-verified {
            color: #E74C3C;
        }
        .credit-score.pending {
            color: #F39C12;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
  
    with st.container(border=True):
        
           # Two-column layout
        col1, col2 = st.columns([1, 3])
        
        # Left column: Profile picture and basic details
        with col1:
            st.markdown("<div class='customer-container'>", unsafe_allow_html=True)
            with st.container(border=True):
                # Profile picture
                if profile_pic:
                    st.image(profile_pic, width=150, caption=None, output_format="auto", clamp=False)
                else:
                    st.image("https://via.placeholder.com/150", width=150)  # Placeholder image
                    
            # Credit Score Section
            st.markdown("<div class='section-header'>Credit Score</div>", unsafe_allow_html=True)
            if credit_score_verified == "Verified":
                st.markdown("<div class='credit-score verified'>Verified 🟢</div>", unsafe_allow_html=True)
            elif credit_score_verified == "Not Verified":
                st.markdown("<div class='credit-score not-verified'>Not Verified 🔴</div>", unsafe_allow_html=True)
            elif credit_score_verified == "Pending":
                st.markdown("<div class='credit-score pending'>Verification Pending ⏳</div>", unsafe_allow_html=True)

            # Recommendation Status
            st.markdown("<div class='section-header'>Recommendation Status</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-row'>{recommendation_status}</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # Right column: Profile details
        with col2:
            st.markdown("<div class='profile-container'>", unsafe_allow_html=True)

            # Profile header
            st.markdown(
                f"""
                <div class="profile-header">
                    <h2>{user['username']}</h2>
                    <h4>{renter_profile['tagline']}</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Additional Information Section
            st.markdown("<div class='section-header'>Basic Information</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-row'><strong>Email:</strong> {user['email']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-row'><strong>Phone:</strong> {renter_profile['phone']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-row'><strong>Age:</strong> {renter_profile['age']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-row'><strong>Nationality:</strong> {renter_profile['nationality']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-row'><strong>Occupation:</strong> {renter_profile['occupation']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-row'><strong>Income:</strong> €{renter_profile['income']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-row'><strong>Work Mode:</strong> {renter_profile['work_mode']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-row'><strong>Contract Type:</strong> {renter_profile['contract_type']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-row'><strong>Social Media:</strong> {renter_profile['social_media']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-row'><strong>Number of persons:</strong> {number_of_people}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-row'><strong>Pets:</strong> {pet}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-row'><strong>Budget:</strong> {budget_range}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='info-row'><strong>Move in date:</strong> {move_in_date}</div>", unsafe_allow_html=True)
            

            st.markdown("</div>", unsafe_allow_html=True)


def renter_full_profile():
    
    back_button()
    
    user_id = st.session_state.get("user_id", str(uuid.uuid4()))
    
    display_renter_full_profile(user_id)
    
    # Edit Profile Button
    if st.button("Edit Profile"):
        st.session_state["current_page"] = "edit_renter_profile"

        
if __name__ == "__main__":
    renter_full_profile()