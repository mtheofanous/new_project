import streamlit as st
from navigation_buttons import home_button

def landing_page():
    # Back to Home Button
    left_column, right_column = st.columns([2.5, 1])
    with left_column:
        home_button()
    
    with right_column:
        # Login/Sign-in Section
        login_col, signup_col = st.columns([1, 1], gap='small')
        with login_col:
            if st.button("Log In", key="login_button"):
                st.session_state["current_page"] = "login"
        
        with signup_col:
            if st.button("Sign Up", key="signup_button"):
                st.session_state["current_page"] = "signup"

    # Page Title
    st.title("Welcome to RentEasy!")
    st.subheader("Connecting renters with landlords and real estate agents seamlessly.")

    # Platform Information
    st.write("""
    ### About RentEasy:
    - **For Renters**: Easily find and rent properties matching your preferences.
    - **For Landlords/Agents**: Manage tenant profiles, verify recommendations, and more.
    - Safe, secure, and user-friendly.
    """)

if __name__ == "__main__":
    landing_page()
