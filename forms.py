import streamlit as st
from app.components.utils import authenticate_user, add_user  # Updated import path to match utils.py location
from navigation_buttons import home_button
from database import save_user_to_db 
from database import (
    load_user_from_db,
    load_renter_profile_from_db,
    load_rental_preferences_from_db,
    load_credit_scores_from_db,
    load_landlord_recommendations_from_db,
)
from app.components.utils import verify_password  # Import the password verification function

def login_form():
    """User login form."""
    # Back to Home Button
    home_button()

    st.title("Log In")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In", key="login_button"):
        try:
            # Fetch user data by email
            user = load_user_from_db(email=email)

            if user and verify_password(password, user["password_hash"]):  # Validate the password
                # Successful login
                st.success(f"Welcome back, {user['username']}!")
                st.session_state["logged_in"] = True
                st.session_state["user_id"] = user["id"]
                st.session_state["user"] = user["username"]
                st.session_state["role"] = user["role"]

                # Load additional data for the renter
                if user["role"] == "Renter":
                    profile = load_renter_profile_from_db(user["id"])
                    if profile:
                        st.session_state.update(profile)

                    preferences = load_rental_preferences_from_db(profile_id=profile["id"])
                    if preferences:
                        st.session_state.update(preferences)

                    credit_score = load_credit_scores_from_db(profile_id=profile["id"])
                    if credit_score:
                        st.session_state.update(credit_score)

                    landlord_recommendations = load_landlord_recommendations_from_db(renter_id=profile["id"])
                    if landlord_recommendations:
                        st.session_state["landlord_recommendations"] = landlord_recommendations

                    # Redirect to the renter dashboard
                    st.session_state["current_page"] = "dashboard"

                elif user["role"] == "Landlord":
                    # Landlord-specific loading logic can be added here
                    st.session_state["current_page"] = "dashboard"

                elif user["role"] == "Agent":
                    # Agent-specific loading logic can be added here
                    st.session_state["current_page"] = "dashboard"

            else:
                # Login failed
                st.error("Invalid email or password. Please try again.")

        except Exception as e:
            st.error(f"An error occurred during login: {e}")

def signup_form():
    """User signup form."""
    # Back to Home Button
    home_button()
    
    st.title("Sign Up")
    username = st.text_input("Username", key="signup_username")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
    role = st.selectbox("Role", ["Renter", "Landlord", "Agent"], key="signup_role")
    gbdr = st.checkbox("I agree to the Terms and Conditions", key="signup_gbdr")

    if st.button("Sign Up", key="signup_button"):
        if password != confirm_password:
            st.error("Passwords do not match.")
        elif not username or not email or not password or not role:
            st.error("All fields are required.")
        elif not gbdr:
            st.error("You must agree to the Terms and Conditions.")
        else:
            try:
                # Save the user to the database
                user_id = save_user_to_db(username, email, password, role)
                
                # Update session state
                st.session_state["signed_up"] = True
                st.session_state["user_id"] = user_id
                st.session_state["user"] = username
                st.session_state["email"] = email
                st.session_state["role"] = role
                st.session_state["logged_in"] = True

                # Redirect to the appropriate profile creation page
                if role == "Renter":
                    st.session_state["current_page"] = "create_renter_profile"
                elif role == "Landlord":
                    st.session_state["current_page"] = "create_landlord_profile"
                elif role == "Agent":
                    st.session_state["current_page"] = "create_agent_profile"

                st.success("Account created successfully!")

            except ValueError as e:
                st.error(str(e))

if __name__ == "__main__":
    st.sidebar.title("Navigation")
    choice = st.sidebar.selectbox("Choose Action", ["Log In", "Sign Up"])
    if choice == "Log In":
        login_form()
    elif choice == "Sign Up":
        signup_form()
