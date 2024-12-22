import streamlit as st
import uuid
from navigation_buttons import home_button, back_button, log_out_button
import streamlit.components.v1 as components
from PIL import Image
from renter.renter_summary_profile import renter_summary_profile
from renter.renter_full_profile import renter_full_profile
from renter.edit_renter_profile import edit_renter_profile
from recommendations.recommendation import recommendation

def renter_dashboard():
    
    st.title("Renter Dashboard")
    st.write("Welcome to your dashboard! Here you can manage your profile, send recommendations, and explore properties.")
    renter_summary_profile()

    if st.button("Recommendations", key="recommendation_button"):
                st.session_state["current_page"] = "recommendation"
    # Available Properties
    with st.expander("Available Properties"):
        st.write("Based on your preferences, here are some properties you might like:")
        # Sample properties (In a real scenario, fetch from a database)
        properties = [
            {"name": "Downtown Apartment", "price": 1200, "location": "Los Angeles, Downtown", "rooms": 2},
            {"name": "Cozy Studio", "price": 900, "location": "Los Angeles, Westwood", "rooms": 1},
            {"name": "Spacious Family Home", "price": 2500, "location": "Los Angeles, Beverly Hills", "rooms": 4}
        ]

        for property in properties:
            st.write(f"**Name:** {property['name']}")
            st.write(f"**Price:** ${property['price']} per month")
            st.write(f"**Location:** {property['location']}")
            st.write(f"**Rooms:** {property['rooms']}")
            if st.button(f"View Details for {property['name']}", key=f"view_{property['name']}"):
                st.info(f"Details for {property['name']} are not yet implemented.")
            if st.button(f"Express Interest in {property['name']}", key=f"interest_{property['name']}"):
                # Simulate sending interest to the landlord's dashboard
                st.success(f"Your interest in {property['name']} has been sent to the landlord.")
            st.markdown("---")

def dashboard():
    # Ensure session state is initialized
    if "role" not in st.session_state:
        st.session_state["role"] = "Renter"

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "dashboard"

    # Navigation based on current_page
    if st.session_state["current_page"] == "view_full_profile":
        st.write("Full profile page not yet implemented.")
        if st.button("Back to Dashboard", key="back_to_dashboard_from_profile"):
            st.session_state["current_page"] = "dashboard"
        return

    if st.session_state["current_page"] == "create_renter_profile":
        st.write("Edit profile page not yet implemented.")
        if st.button("Back to Dashboard", key="back_to_dashboard_from_edit"):
            st.session_state["current_page"] = "dashboard"
        return
    
    # log out button 
        
    if "logout_confirmation" not in st.session_state:
                st.session_state["logout_confirmation"] = False
                
    # Create columns to align the log out button on the right
    col1, col2 = st.columns([6, 1])  # Adjust column proportions as needed
    with col2:
        if st.button("Log Out", key="log_out_button"):
            st.session_state["logout_confirmation"] = True
                    
    col3, col4 = st.columns([2, 1])
    with col4:
        if st.session_state["logout_confirmation"]:
            st.warning("Are you sure that you want to log out?")
            col_yes, col_no = st.columns([1,2])
            
            with col_yes:
                if st.button("Yes", key="confirm_logout"):
                    st.session_state.clear()
                    st.session_state["current_page"] = "landing"
                    st.success("You have been logged out.")
                    st.rerun()

            with col_no:
                if st.button("No", key="cancel_logout"):
                    st.session_state["logout_confirmation"] = False
                
    # Load dashboard based on role
                
    role = st.session_state.get("role", "Renter")
                
    role = st.selectbox("**Role**", ["Renter", "Landlord", "Agent"], key="signup_role", index=["Renter", "Landlord", "Agent"].index(role))

    if role == "Renter":
        renter_dashboard()
    elif role == "Landlord":
        st.write("Landlord Dashboard")
        # landlord_dashboard()
    elif role == "Agent":
        st.write("Agent Dashboard")
        # agent_dashboard()

if __name__ == "__main__":
    dashboard()


