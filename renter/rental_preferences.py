import streamlit as st
import datetime
from navigation_buttons import home_button, back_button
from database import save_rental_preferences_to_db
 
def rental_preferences():
    
    back_button()
    
    if "rental_preferences" not in st.session_state:
        rental_preferences_data = {}
    else:
        rental_preferences_data = st.session_state["rental_preferences"]
    cities = ["Athens", "Thessaloniki", "Patras", "Heraklion", "Other"]
    default_city = rental_preferences_data["preferred_city"] if "preferred_city" in rental_preferences_data else "Athens"
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
    
    previously_selected_areas = rental_preferences_data.get("preferred_area", [])
    
    previously_selected_areas = [area for area in previously_selected_areas if area in all_areas]

    # Allow the user to choose areas for the selected cities
    area = st.multiselect(
        "Preferred Areas",
        options=all_areas,
        default=previously_selected_areas,
        key="new_profile_areas"
    )
    
    # Check if "All" is selected for areas
    if "All" in area:
        area = [a for a in all_areas if a != "All"]
    
    # Initialize session state for min and max budget
    if "rental_preferences" not in st.session_state:
        rental_preferences_data["budget_min"] = 100.0
    if "rental_preferences" not in st.session_state:
        rental_preferences_data["budget_max"] = 2000.0
    
    budget_min, budget_max = st.slider(
        "Budget Range (€)",
        100.0,
        3000.0,
        value=(rental_preferences_data["budget_min"], rental_preferences_data["budget_max"]),
        step=50.0,
        key="budget_slider"
    )

    property_type = st.selectbox(
        "Type of Property",
        ["Apartment", "House", "Shared Accommodation"],
        index=["Apartment", "House", "Shared Accommodation"].index(rental_preferences_data.get("property_type", "Apartment")),
        key="new_profile_property_type"
    )
    
    # Initialize session state for min and max property size
    if "rental_preferences" not in st.session_state:
        rental_preferences_data["property_size_min"] = 10.0
    if "rental_preferences" not in st.session_state:
        rental_preferences_data["property_size_max"] = 500.0
    
    property_size_min, property_size_max = st.slider(
        "Property Size (m²)",
        10.0,
        500.0,
        value=(rental_preferences_data.get("property_size_min", 10.0), rental_preferences_data.get("property_size_max", 500.0)),
        step=5.0,
        key="property_size_slider"
    )
    
    bedrooms = st.number_input(
        "Number of Rooms Needed",
        min_value=1,
        step=1,
        value=rental_preferences_data.get("bedrooms", 1),
        key="new_profile_rooms"
    )
    
    bathrooms = st.number_input(
        "Number of Bathrooms Needed",
        min_value=1,
        step=1,
        value=rental_preferences_data.get("bathrooms", 1),
        key="new_profile_bathrooms"
    )
    
    floor = st.number_input(
        "Floor",
        min_value=0,
        step=1,
        value=rental_preferences_data.get("floor", 0),
        key="new_profile_floor"
    )
    
    num_people = st.number_input(
        "Number of People (including yourself)",
        min_value=1,
        step=1,
        value=rental_preferences_data.get("num_people", 1),
        key="new_profile_people"
    )
    move_in_date = st.date_input(
        "Move-in Date",
        value=rental_preferences_data.get("move_in_date", datetime.date.today()),
        key="new_profile_move_in"
    )
    lease_duration = st.selectbox(
        "Lease Duration",
        ["Short-term", "Long-term", "Flexible"],
        index=["Short-term", "Long-term", "Flexible"].index(rental_preferences_data.get("lease_duration", "Flexible")),
        key="new_profile_lease_duration"
    )
    pets = st.radio(
        "Do you have pets?",
        ["No", "Yes"],
        index=["No", "Yes"].index(rental_preferences_data.get("pets", "No")),
        key="new_profile_pets"
    )
    pet_type = st.text_input(
        "Pet Type (e.g., Dog, Cat)",
        value=rental_preferences_data.get("pet_type", ""),
        key="new_profile_pet_type"
    ) if pets == "Yes" else None
    
    # save button
    if st.button("Save Preferences", key="updated_rental_preferences"):
        
    # Save rental preferences to session state
        rental_preferences_data = {
            "preferred_city": city,
            "preferred_area": area,
            "budget_min": budget_min,
            "budget_max": budget_max,
            "property_type": property_type,
            "property_size_min": property_size_min,
            "property_size_max": property_size_max,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "floor": floor,
            "num_people": num_people,
            "move_in_date": move_in_date,
            "lease_duration": lease_duration,
            "pets": pets,
            "pet_type": pet_type
        }

        # Save rental preferences to session state
        st.session_state["rental_preferences"]  = rental_preferences_data
        
        # Save rental preferences to database
        user_id = st.session_state.get("user_id")
        
        with st.spinner("Saving rental preferences..."):
            try:
                save_rental_preferences_to_db(user_id, rental_preferences_data)
                st.success("Rental preferences saved successfully!")
                st.session_state["current_page"] = "dashboard"
                
                st.session_state["rental_preferences"] = rental_preferences_data
            except Exception as e:
                st.error("Failed to save rental preferences. Please try again.")
                st.error(e)
                
if __name__ == "__main__":
    rental_preferences()
