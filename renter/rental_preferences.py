
import streamlit as st

def rental_preferences():
    cities = ["Athens", "Thessaloniki", "Patras", "Heraklion", "Other"]
    default_city = st.session_state.get("city", "Athens")
    if default_city not in cities:
        default_city = "Athens"
    
    city = st.multiselect(
        "Preferred City",
        options=cities,
        default=[default_city],
        key="new_profile_city"
    )
    
    # Get areas based on selected cities            
    areas = {
        "Athens": ["Plaka", "Kolonaki", "Glyfada", "Marousi", "Kifisia"],
        "Thessaloniki": ["Ladadika", "Toumba", "Panorama", "Pylaia", "Thermi"],
        "Patras": ["Psila Alonia", "Rio", "Agios Andreas", "Vrachneika"],
        "Heraklion": ["Knossos", "Ammoudara", "Poros", "Agios Nikolaos"],
        "Other": ["Specify Other"]
    }
    
    selected_areas = []
    for c in city:
        selected_areas += areas.get(c, [])
    
    # Add "All" to the list of areas
    all_areas = ['All'] + selected_areas
    
    # Allow the user to choose areas for the selected cities
    area = st.multiselect(
        "Preferred Areas",
        options=all_areas,
        default=[],
        key="new_profile_areas"
    )
    
    # Check if "All" is selected for areas
    if "All" in area:
        area = [a for a in all_areas if a != "All"] 
    # cities = ["Athens", "Thessaloniki", "Patras", "Heraklion", "Other"]
    # city = st.multiselect(
    #     "Preferred City",
    #     options=cities,
    #     default=[st.session_state.get("city", "Athens")],
    #     key="new_profile_city"
    # )
    # # Get areas based on selected cities            
    # areas = {
    #     "Athens": ["Plaka", "Kolonaki", "Glyfada", "Marousi", "Kifisia"],
    #     "Thessaloniki": ["Ladadika", "Toumba", "Panorama", "Pylaia", "Thermi"],
    #     "Patras": ["Psila Alonia", "Rio", "Agios Andreas", "Vrachneika"],
    #     "Heraklion": ["Knossos", "Ammoudara", "Poros", "Agios Nikolaos"],
    #     "Other": ["Specify Other"]
    # }
    # selected_areas = []
    # for c in city:
    #     selected_areas += areas.get(c, [])
    # # Allow the user to choose areas for the selected cities
    # all_areas = ['All'] + selected_areas
    
    # area = st.multiselect(
    #     "Preferred Areas",
    #     options=all_areas,
    #     default=[],
    #     key="new_profile_areas"
    # )
    
    # # Check if "All" is selected for areas
    # if "All" in area:
    #     area = [area for area in all_areas if area != "All"]
    
    budget_min, budget_max = st.slider("Budget Range ($)", 500, 5000, (st.session_state.get("budget_min", 1000), st.session_state.get("budget_max", 3000)), key="new_profile_budget")
    property_type = st.selectbox("Type of Property", ["Apartment", "House", "Shared Accommodation"], index=["Apartment", "House", "Shared Accommodation"].index(st.session_state.get("property_type", "Apartment")), key="new_profile_property_type")
    rooms = st.number_input("Number of Rooms Needed", min_value=1, step=1, value=st.session_state.get("rooms", 1), key="new_profile_rooms")
    num_people = st.number_input("Number of People (including yourself)", min_value=1, step=1, value=st.session_state.get("num_people", 1), key="new_profile_people")
    move_in_date = st.date_input("Move-in Date", value=st.session_state.get("move_in_date"), key="new_profile_move_in")
    lease_duration = st.selectbox("Lease Duration", ["Short-term", "Long-term", "Flexible"], index=["Short-term", "Long-term", "Flexible"].index(st.session_state.get("lease_duration", "Flexible")), key="new_profile_lease_duration")
    pets = st.radio("Do you have pets?", ["No", "Yes"], index=["No", "Yes"].index(st.session_state.get("pets", "No")), key="new_profile_pets")
    pet_type = st.text_input("Pet Type (e.g., Dog, Cat)", value=st.session_state.get("pet_type", ""), key="new_profile_pet_type") if pets == "Yes" else None
    
    st.session_state["city"] = city
    st.session_state["area"] = area
    st.session_state["budget_min"] = budget_min
    st.session_state["budget_max"] = budget_max
    st.session_state["property_type"] = property_type
    st.session_state["rooms"] = rooms
    st.session_state["num_people"] = num_people
    st.session_state["move_in_date"] = move_in_date
    st.session_state["lease_duration"] = lease_duration
    st.session_state["pets"] = pets
    st.session_state["pet_type"] = pet_type