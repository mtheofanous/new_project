import streamlit as st
from renter.renter_summary_profile import renter_summary_profile
from renter.edit_renter_profile import edit_renter_profile
from agent.agent_summary_profile import agent_summary_profile
from landlord.landlord_summary_profile import landlord_summary_profile
from roles import get_user_roles

def renter_dashboard():
    
    st.title("Renter Dashboard")
    
    st.write("Welcome to your dashboard! Here you can manage your profile, send recommendations, and explore properties.")
    renter_summary_profile()
    
    if st.sidebar.button("Rental Preferences", key="rental_preferences_button"):
        st.session_state["current_page"] = "rental_preferences"

    if st.sidebar.button("Manage Recommendations", key="recommendation_button"):
        st.session_state["current_page"] = "recommendation"
                    
    if st.sidebar.button("Manage Credit Score", key="credit_score_button"):
        st.session_state["current_page"] = "credit_score"
                    
    if st.sidebar.button("Search Properties", key="search_properties_button"):
        st.session_state["current_page"] = "search_properties"
        
    if st.sidebar.button("Edit Profile", key="edit_profile_button"):
        st.session_state["current_page"] = 'edit_renter_profile'
  
    
                
def agent_dashboard():
    st.title("Agent Dashboard")
    st.write("Welcome to your dashboard! Here you can manage your profile, view listings, and interact with clients.")
    agent_summary_profile()
        
    if st.sidebar.button("Search Renters", key="search_renters_button"):
        st.session_state["current_page"] = "search_renters"
        st.rerun()
    
    if st.sidebar.button("Manage Listings", key="listing_button"):
        st.session_state["current_page"] = "listing"
        st.rerun()
            
                            
    if st.sidebar.button("Manage Client Reviews", key="client_reviews_button"):
        st.session_state["current_page"] = "client_reviews"
        st.rerun()
                    

# Landlord dashboard

def landlord_dashboard():
    st.title("Landlord Dashboard")
    st.write("Welcome to your dashboard! Here you can manage your profile, view your properties, and interact with tenants.")
    landlord_summary_profile()
        
    if st.sidebar.button("Search Tenants", key="search_tenants_button"):
        st.session_state["current_page"] = "search_tenants"
        st.rerun()
    
    if st.sidebar.button("Manage Listings", key="listing_button"):
        st.session_state["current_page"] = "listing"
        st.rerun()
                            
    if st.sidebar.button("Manage Tenant Reviews", key="tenant_reviews_button"):
        st.session_state["current_page"] = "tenant_reviews"
        st.rerun()
            
def dashboard():
    # Ensure session state is initialized
    if "role" not in st.session_state:
        st.session_state["role"] = "Renter"

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "dashboard"

    # log out button 
        
    if "logout_confirmation" not in st.session_state:
                st.session_state["logout_confirmation"] = False
                
    # Create columns to align the log out button on the right
    col1, col2, col3 = st.columns([6,1,2])  # Adjust column proportions as needed
    with col1:
        if st.button("Settings", key="settings_button"):
            st.session_state["current_page"] = "profile_settings"
    with col2:
        if st.button("❤️", key="favorites_button"):
            st.session_state["current_page"] = "display_favorites"
            
    with col3:
        if st.button("Log Out", key="log_out_button"):
            st.session_state["logout_confirmation"] = True
                    
    col4, col5 = st.columns([2, 1])
    with col5:
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
                
    # Load the user's roles
    user_id = st.session_state.get("user_id", None)
    
    roles = get_user_roles(user_id)

    if len(roles) == 0:
        st.error("You do not have any roles assigned to your account. Please contact support.")
        return
    elif len(roles) == 1:
        role = roles[0]
        
    elif len(roles) > 1:
        selected_role = st.selectbox("#### **Select Role**", roles, key="role_selectbox",
                                     index=roles.index(roles[0]))
        role = selected_role
                
    if role == "Renter":
        # save session state for the current role
        st.session_state["role"] = role
        renter_dashboard()
        
    elif role == "Landlord":
        st.session_state["role"] = role
        landlord_dashboard()
        
        # landlord_dashboard()
    elif role == "Agent":
        st.session_state["role"] = role
        agent_dashboard()

if __name__ == "__main__":
    dashboard()


