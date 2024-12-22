import streamlit as st
import uuid
from navigation_buttons import home_button, back_button 
from renter.rental_preferences import rental_preferences
from credit_score.credit_score import income_credit_score
# from recommendations.recommendation import recommendation_form

def edit_renter_profile():
    
    back_button()
    
    username = st.session_state.get("user", "User")
    email = st.session_state.get("email", "Email")
    profile_pic = st.session_state.get("profile_pic", None)
    #     
    st.title("Edit Your Renter Profile")

    # Profile Header
    st.header("Profile Header")
    # Handle profile picture upload
    uploaded_file = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"], key="new_profile_pic")

    # Save the uploaded file to session state if uploaded
    if uploaded_file:
        st.session_state["profile_pic"] = uploaded_file

    # Display the profile picture if it exists in session state
    if "profile_pic" in st.session_state and st.session_state["profile_pic"] is not None:
        st.image(st.session_state["profile_pic"], caption="Current Profile Picture", width=150)
    else:
        st.info("No profile picture uploaded.")
    username = st.text_input("Username", value=st.session_state.get("user", ""), key="new_profile_username")
    name = st.text_input("Full Name", value=st.session_state.get("name", ""), key="new_profile_name")
    tagline = st.text_input("Tagline", value=st.session_state.get("tagline", ""), key="new_profile_tagline")

    # Personal Details
    with st.expander("Personal Details"):
        email = st.text_input("Email", value=st.session_state.get("email", ""), key="new_profile_email")
        age = st.number_input("Age", min_value=18, max_value=100, step=1, value=st.session_state.get("age", 18), key="new_profile_age")
        phone = st.text_input("Phone Number", value=st.session_state.get("phone", ""), key="new_profile_phone")
        nationality = st.text_input("Nationality", value=st.session_state.get("nationality", ""), key="new_profile_nationality")
        occupation = st.text_input("Occupation", value=st.session_state.get("occupation", ""), key="new_profile_occupation")
        contract_type = st.selectbox("Contract Type", ["Permanent", "Contract", "Freelancer", "Unemployed"], index=["Permanent", "Contract", "Freelancer", "Unemployed"].index(st.session_state.get("contract_type", "Permanent")), key="new_profile_contract")
        income = st.number_input("Monthly Income (€)", min_value=0, step=100, value=st.session_state.get("income", 0), key="new_profile_income")
        work_mode = st.radio("Work Mode", ["Remote", "On-site", "Hybrid"], index=["Remote", "On-site", "Hybrid"].index(st.session_state.get("work_mode", "Remote")), key="new_profile_work_mode")

    # Rental Preferences
    with st.expander("Rental Preferences"):
        rental_preferences()

    # About Me
    with st.expander("About Me"):
        bio = st.text_area("Bio", value=st.session_state.get("bio", ""), key="new_profile_bio")
        hobbies = st.text_input("Hobbies & Interests (comma-separated)", value=st.session_state.get("hobbies", ""), key="new_profile_hobbies")

    # Income and Credit Score
    with st.expander("Income and Credit Score"):
        income_credit_score()
        
    # Save profile button
    if st.button("Save Profile", key="save_edit_profile"):
        st.session_state["user"] = username
        st.session_state["email"] = email
        st.session_state["profile_pic"] = profile_pic
        st.session_state["name"] = name
        st.session_state["tagline"] = tagline
        st.session_state["age"] = age
        st.session_state["phone"] = phone
        st.session_state["nationality"] = nationality
        st.session_state["occupation"] = occupation
        st.session_state["contract_type"] = contract_type
        st.session_state["work_mode"] = work_mode
        st.session_state["bio"] = bio
        st.session_state["hobbies"] = hobbies
        st.session_state["income"] = income
        st.success("Your renter profile has been created successfully!")
        st.session_state["current_page"] = "dashboard"

if __name__ == "__main__":
    edit_renter_profile()
