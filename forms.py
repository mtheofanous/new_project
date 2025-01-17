import streamlit as st
from app.components.utils import authenticate_user, add_user  # Updated import path to match utils.py location
from navigation_buttons import home_button
from queries.user import save_user_to_db, load_user_from_db
from queries.renter import load_renter_profile_from_db, load_rental_preferences_from_db, load_credit_scores
from queries.agent import load_agent_profile_from_db
from queries.landlord import load_landlord_profile_from_db
from queries.property import load_properties_by_user
from app.components.utils import verify_password  # Import the password verification function
from roles import assign_role_to_user, get_user_roles

            
def login_form():
    """User login form."""
    # Back to Home Button
    home_button()
    
    st.title("Log In")
    
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Log In", key="login_button"):
        
        try:
            
            if email.strip():
                user = load_user_from_db(email=email)
            else:
                st.error("Please enter a valid email address.")
                return
                        
            if not user:
                st.error("User not found. Please check your email or sign up.")
                return
            
            if not verify_password(password, user["password_hash"]):
                st.error("Invalid password. Please try again.")
                return
            
            # Successful login
            st.success(f"Welcome back, {user['username']}!")
            roles = get_user_roles(user["id"])
            
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user["id"]
            st.session_state["user"] = user["username"]
            st.session_state["first_name"] = user["first_name"]
            st.session_state["last_name"] = user["last_name"]
            st.session_state["email"] = user["email"]

            if roles[0] == "Renter":
                
                st.session_state["user_id"] = user["id"]
                st.session_state["user"] = user["username"]
                st.session_state["first_name"] = user["first_name"]
                st.session_state["last_name"] = user["last_name"]
                st.session_state["role"] = roles
                st.session_state["email"] = user["email"]
                
                profile = load_renter_profile_from_db(user["id"])
                credit_score = load_credit_scores(user["id"])
                if profile:
                    st.session_state["renter_profile"] = profile
                if credit_score:
                    st.session_state["credit_score"] = credit_score

                preferences = load_rental_preferences_from_db(profile_id=profile["id"])
                if preferences:
                    st.session_state["rental_preferences"] = preferences

                st.session_state["current_page"] = "dashboard"
                st.rerun()

            elif roles[0] == "Landlord":
                
                st.session_state["user_id"] = user["id"]
                st.session_state["user"] = user["username"]
                st.session_state["first_name"] = user["first_name"]
                st.session_state["last_name"] = user["last_name"]
                st.session_state["role"] = roles
                st.session_state["email"] = user["email"]
                
                profile = load_landlord_profile_from_db(user["id"])
                properties = load_properties_by_user(user["id"], role=roles[0])
                if profile:
                    st.session_state["landlord_profile"] = profile
                if properties:
                    st.session_state["properties"] = properties
                
                st.session_state["current_page"] = "dashboard"
                st.rerun()

            elif roles[0] == "Agent":
                
                st.session_state["user_id"] = user["id"]
                st.session_state["user"] = user["username"]
                st.session_state["first_name"] = user["first_name"]
                st.session_state["last_name"] = user["last_name"]
                st.session_state["role"] = roles
                st.session_state["email"] = user["email"]
                
                profile = load_agent_profile_from_db(user["id"])
                properties = load_properties_by_user(user["id"], role=roles[0])
                
                if profile:
                    st.session_state["agent_profile"] = profile
                if properties:
                    st.session_state["properties"] = properties
                
                st.session_state["current_page"] = "dashboard"
                st.rerun()

        except Exception as e:
            st.error(f"An error occurred during login: {e}")


def signup_form():
    """User signup form."""
    # Back to Home Button
    home_button()
    
    st.title("Sign Up")
    username = st.text_input("Username", key="signup_username")
    first_name = st.text_input("First Name", key="signup_first_name")
    last_name = st.text_input("Last Name", key="signup_last_name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
    role = st.selectbox("Role", ["Renter", "Landlord", "Agent"], key="signup_role")
    gbdr = st.checkbox("I agree to the Terms and Conditions", key="signup_gbdr")
    
    # ensure that email has no spaces and is small caps
    email = email.strip().lower()

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
                user_id = save_user_to_db(username, first_name, last_name, email, password)
                
                # assign the selected role to the user
                assign_role_to_user(user_id, role)
                
                # Update session state
                st.session_state["signed_up"] = True
                st.session_state["user_id"] = user_id
                st.session_state["user"] = username
                st.session_state["first_name"] = first_name
                st.session_state["last_name"] = last_name
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
