import streamlit as st
from landing_page import landing_page
from forms import login_form, signup_form
from renter.create_renter_profile import create_renter_profile
from renter.edit_renter_profile import edit_renter_profile
from renter.renter_summary_profile import renter_summary_profile
from renter.renter_full_profile import renter_full_profile
from dashboard import dashboard, renter_full_profile
from recommendations.recommendation import recommendation

def main():
    # Initialize session state variables
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "landing"
    # Routing
    if st.session_state["current_page"] == "landing":
        landing_page()
    elif st.session_state["current_page"] == "login":
        login_form()
    elif st.session_state["current_page"] == "signup":
        signup_form()
    elif st.session_state["current_page"] == "create_renter_profile":
        create_renter_profile()
    elif st.session_state["current_page"] == "dashboard":
        dashboard()
    elif st.session_state["current_page"] == "renter_full_profile":
        renter_full_profile()
    elif st.session_state["current_page"] == "edit_renter_profile":
        edit_renter_profile()
    elif st.session_state["current_page"] == "recommendation":
        recommendation()

if __name__ == "__main__":
    main()
