import streamlit as st
from navigation_buttons import back_button
from queries.renter import get_all_renter_user_ids
from renter.renter_full_profile import display_renter_full_profile
from renter.renter_summary_profile import display_renter_summary_profile

def search_renters():
    
    back_button()
    
    """
    Allow agents to search renters using filters and display their full profiles,
    with an option to clear filters and view all renters.
    """

    # Page header
    st.title("Search Renters")
    st.markdown("Use the filters below to search for renters or clear filters to view all renters.")

    # Search filters
    st.sidebar.header("Filter Renters")
    min_age = st.sidebar.number_input("Minimum Age", min_value=18, step=1, value=18)
    max_age = st.sidebar.number_input("Maximum Age", min_value=18, step=1)
    nationality = st.sidebar.text_input("Nationality")
    min_income = st.sidebar.number_input("Minimum Income (€)", min_value=0.0, step=1000.0, value=0.0)
    max_income = st.sidebar.number_input("Maximum Income (€)", min_value=0.0, step=1000.0)
    preferred_city = st.sidebar.text_input("Preferred City")
    preferred_area = st.sidebar.text_input("Preferred Area")
    budget_min = st.sidebar.number_input("Minimum Budget (€)", min_value=0.0, step=100.0, value=0.0)
    budget_max = st.sidebar.number_input("Maximum Budget (€)", min_value=0.0, step=100.0)
    pets = st.sidebar.selectbox("Pets", ["Any", "Yes", "No"])

    # Buttons: Search and Clear Filters
    filter_options = {}
    if st.sidebar.button("Search"):
        filter_options = {
            "min_age": min_age,
            "max_age": max_age,
            "nationality": nationality,
            "min_income": min_income,
            "max_income": max_income,
            "preferred_city": preferred_city,
            "preferred_area": preferred_area,
            "budget_min": budget_min,
            "budget_max": budget_max,
            "pets": pets if pets != "Any" else None,
        }

    if st.sidebar.button("Clear Filters"):
        filter_options = {}  # Clear all filter criteria

    # Fetch renters based on filter options (or fetch all if no filters)
    # renters = find_matching_renters_dict(filter_options) if filter_options else find_matching_renters_dict({})
    renters = get_all_renter_user_ids()
    
    
    
    if not renters:
        st.warning("No renters found in the database.")
        return
    else:
        st.success(f"Found {len(renters)} renter(s).")
        num = 1
        for index, renter in enumerate(renters):
            with st.container(border=True):
                toggle_key = f"renter_full_profile_{index}_{num}"
                if toggle_key not in st.session_state:
                    st.session_state[toggle_key] = False
                    
                if st.button("View Full Profile", key=f'{toggle_key}_button_{num}'):
                    # Toggle the display of the full profile
                    st.session_state[toggle_key] = not st.session_state[toggle_key]
                    num += 1
                    
                if st.session_state[toggle_key]:
                    display_renter_full_profile(renter)
                    
                num += 1
                
                display_renter_summary_profile(renter)
   
# Main Function to Load the Page
if __name__ == "__main__":
    search_renters()


