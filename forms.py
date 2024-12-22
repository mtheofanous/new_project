import streamlit as st
from app.components.utils import authenticate_user, add_user
from navigation_buttons import home_button, back_button 

def login_form():
    
    # Back to Home Button
    home_button()
    
    st.title("Log In")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Log In", key="login_button"):
        user = authenticate_user(email, password)
        if user:
            st.success(f"Welcome back, {user[1]}!")
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user[0]  # Store user_id
            st.session_state["user"] = user[1]
            st.session_state["role"] = user[4]
            # Redirect to role-specific dashboard
            if user[4] == "Renter":
                st.session_state["current_page"] = "dashboard"
            elif user[4] == "Landlord":
                st.session_state["current_page"] = "dashboard"
            elif user[4] == "Agent":
                st.session_state["current_page"] = "dashboard"
        else:
            st.error("Invalid email or password. Please try again.")

def signup_form():
    
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
        else:
            user_id = add_user(username, email, password, role)
            if user_id:
                st.success("Account created successfully.")
                st.session_state["signed_up"] = True
                st.session_state["user_id"] = user_id  # Store user_id
                if role == "Renter":
                    st.session_state["current_page"] = "create_renter_profile"
                elif role == "Landlord":
                    st.session_state["current_page"] = "create_landlord_profile"
                elif role == "Agent":
                    st.session_state["current_page"] = "create_agent_profile"
            else:
                st.error("Username or email already exists. Please try a different one.")
                
            # save user data
            st.session_state["user"] = username
            st.session_state["email"] = email
            st.session_state["password"] = password
            st.session_state["role"] = role
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user_id
         

if __name__ == "__main__":
    st.sidebar.title("Navigation")
    choice = st.sidebar.selectbox("Choose Action", ["Log In", "Sign Up"])
    if choice == "Log In":
        login_form()
    elif choice == "Sign Up":
        signup_form()
