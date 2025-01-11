import streamlit as st
import sqlite3
from db_setup import get_db_connection, create_tables
from landing_page import landing_page
from forms import login_form, signup_form
from renter.create_renter_profile import create_renter_profile
from renter.edit_renter_profile import edit_renter_profile
from renter.renter_full_profile import renter_full_profile
from agent.create_agent_profile import create_agent_profile
from agent.edit_agent_profile import edit_agent_profile
from agent.agent_full_profile import agent_full_profile
from agent.agent_summary_profile import agent_summary_profile
from agent.edit_property import edit_property_with_images
from agent.preview_property import preview_property
from agent.search_renters import search_renters
from agent.listing import listing
from dashboard import dashboard
from renter.recommendations.recommendation import recommendation
from renter.credit_score.credit_score import credit_score
from renter.rental_preferences import rental_preferences
from renter.search_properties import search_properties
from renter.renter_preview_property import renter_preview_property
from favorites import display_favorites
from settings import profile_settings
from renter.search_properties import search_properties



def main():
    # Ensure database tables are created
    create_tables()

    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "landing"
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    if "profile_loaded" not in st.session_state:
        st.session_state["profile_loaded"] = False
        
    # Page routing
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
    elif st.session_state["current_page"] == "credit_score":
        credit_score()
    elif st.session_state["current_page"] == "profile_settings":
        profile_settings()
    elif st.session_state["current_page"] == "create_agent_profile":
        create_agent_profile()
    elif st.session_state["current_page"] == "edit_agent_profile":
        edit_agent_profile()
    elif st.session_state["current_page"] == "agent_full_profile":
        agent_full_profile()
    elif st.session_state["current_page"] == "agent_summary_profile":
        agent_summary_profile()
    elif st.session_state["current_page"] == "search_renters":
        search_renters()
    elif st.session_state["current_page"] == "search_properties":
        search_properties()
    elif st.session_state["current_page"] == "display_favorites":
        display_favorites()

    elif st.session_state["current_page"] == "rental_preferences":
        rental_preferences()
    elif st.session_state["current_page"] == "listing":
        listing()
    elif st.session_state["current_page"] == "edit_property":
        edit_property_with_images()
    elif st.session_state["current_page"] == "preview_property":
        selected_property = st.session_state.get("selected_property", None)
        if selected_property:
            preview_property(selected_property)
        else:
            st.error("No property selected for preview.")
    elif st.session_state["current_page"] == "renter_preview_property":
        renter_selected_property = st.session_state.get("renter_selected_property", None)
        if renter_selected_property:
            renter_preview_property(renter_selected_property)
        else:
            st.error("No property selected for preview.")
    


if __name__ == "__main__":
    main()

