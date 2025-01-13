import streamlit as st
from navigation_buttons import back_button
from queries.filters import find_matching_renters_dict
from queries.renter import get_all_renter_user_ids
from renter.renter_full_profile import renter_full_profile

def search_tenants():
    """
    Streamlit interface for searching renters based on filter criteria.
    """
    back_button()
    st.title("Search Renters")

    # Sidebar Filters
    st.sidebar.header("Filter Renters")
    

    # Filters for Renter Profiles
    
    st.sidebar.subheader("Renter Profiles")
    with st.sidebar.expander("Renter Profiles"):
        min_age = st.sidebar.number_input("Minimum Age", min_value=18, step=1)
        max_age = st.sidebar.number_input("Maximum Age", min_value=18, step=1)
        nationality = st.sidebar.text_input("Nationality")
        contract_type = st.sidebar.text_input("Contract Type")
        min_income = st.sidebar.number_input("Minimum Income (€)", min_value=0.0, step=1000.0)
        max_income = st.sidebar.number_input("Maximum Income (€)", min_value=0.0, step=1000.0)
        work_mode = st.sidebar.text_input("Work Mode")

    # Filters for Rental Preferences
    st.sidebar.subheader("Rental Preferences")
    with st.sidebar.expander("Renter Profiles"):
        preferred_city = st.sidebar.text_input("Preferred City")
        preferred_area = st.sidebar.text_input("Preferred Area")
        budget_min = st.sidebar.number_input("Minimum Budget (€)", min_value=0.0, step=50.0)
        budget_max = st.sidebar.number_input("Maximum Budget (€)", min_value=0.0, step=50.0)
        property_type = st.sidebar.selectbox("Property Type", ["Any", "Apartment", "House", "Studio", "Shared Room"])
        bedrooms = st.sidebar.number_input("Minimum Bedrooms", min_value=0, step=1)
        bathrooms = st.sidebar.number_input("Minimum Bathrooms", min_value=0, step=1)
        floor = st.sidebar.number_input("Minimum Floor", min_value=0, step=1)
        number_of_people = st.sidebar.number_input("Number of People", min_value=1, step=1)
        move_in_date = st.sidebar.date_input("Move-in Date")
        pets = st.sidebar.selectbox("Pets", ["Any", "Yes", "No"])
        lease_duration = st.sidebar.selectbox("Lease Duration", ["Any", "Short-Term", "Long-Term"])

    # Filters for Credit Score
    st.sidebar.subheader("Additional Filters")
    credit_score_status = st.sidebar.selectbox("Credit Score Status", ["Any", "Verified", "Not Verified", "Pending"])

    renters = get_all_renter_user_ids()
    
    # if renters is empty, display a message and return
    if not renters:
        st.warning("No renters found in the database.")
        return
    else:
        st.success(f"Found {len(renters)} renter(s).")
        for renter in renters:
            renter_full_profile(renter)
            st.markdown("---")
    # # Submit Button
    # if st.sidebar.button("Search"):
    #     # Prepare filter options for the query
    #     filter_options = {
    #         "min_age": min_age,
    #         "max_age": max_age,
    #         "nationality": nationality,
    #         "contract_type": contract_type,
    #         "min_income": min_income,
    #         "max_income": max_income,
    #         "work_mode": work_mode,
    #         "preferred_city": preferred_city,
    #         "preferred_area": preferred_area,
    #         "budget_min": budget_min,
    #         "budget_max": budget_max,
    #         "property_type": property_type,
    #         "bedrooms": bedrooms,
    #         "bathrooms": bathrooms,
    #         "floor": floor,
    #         "number_of_people": number_of_people,
    #         "move_in_date": move_in_date,
    #         "pets": pets,
    #         "lease_duration": lease_duration,
    #         "credit_score_status": credit_score_status,
    #     }

    #     # Fetch matching renters
    #     renters = find_matching_renters_dict(filter_options)

    #     # Display results
    #     if renters:
    #         st.write(f"Found {len(renters)} renter(s):")
    #         for renter in renters:
    #             # st.write(f"Name: {renter['first_name']} {renter['last_name']}")
    #             st.write(f"profile_id {renter['profile_id']}")

    #             # with st.expander(f"View Profile: {renter['first_name']} {renter['last_name']}"):
    #             #     if renter["profile_pic"]:
    #             #         st.image(renter["profile_pic"], caption="Profile Picture", width=150)
    #             #     st.markdown(
    #             #         f"""
    #             #         <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
    #             #             <h3 style="color: #2C3E50; margin-bottom: 15px;">{renter['first_name']} {renter['last_name']}</h3>
    #             #             <p><strong>Age:</strong> {renter['age']} years</p>
    #             #             <p><strong>Nationality:</strong> {renter['nationality']}</p>
    #             #             <p><strong>Contract Type:</strong> {renter['contract_type']}</p>
    #             #             <p><strong>Income:</strong> €{renter['income']}</p>
    #             #             <p><strong>Work Mode:</strong> {renter['work_mode']}</p>
    #             #             <p><strong>Preferred City:</strong> {renter['preferred_city']}</p>
    #             #             <p><strong>Preferred Area:</strong> {renter['preferred_area']}</p>
    #             #             <p><strong>Budget Range:</strong> €{renter['budget_min']} - €{renter['budget_max']}</p>
    #             #             <p><strong>Property Type:</strong> {renter['property_type']}</p>
    #             #             <p><strong>Bedrooms:</strong> {renter['bedrooms']}</p>
    #             #             <p><strong>Bathrooms:</strong> {renter['bathrooms']}</p>
    #             #             <p><strong>Floor:</strong> {renter['floor']}</p>
    #             #             <p><strong>Number of People:</strong> {renter['number_of_people']}</p>
    #             #             <p><strong>Move-in Date:</strong> {renter['move_in_date']}</p>
    #             #             <p><strong>Pets Allowed:</strong> {renter['pets']}</p>
    #             #             <p><strong>Lease Duration:</strong> {renter['lease_duration']}</p>
    #             #             <p><strong>Credit Score Status:</strong> {renter['credit_score_status']}</p>
    #             #         </div>
    #             #         """,
    #             #         unsafe_allow_html=True
    #             #     )
    #             st.write("---")
    #     else:
    #         st.warning("No renters found with the specified filters.")

if __name__ == "__main__":
    search_tenants()

