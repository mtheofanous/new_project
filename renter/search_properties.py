import streamlit as st
import datetime
from navigation_buttons import home_button, back_button
from database import update_rental_preferences
from queries.filters import find_matching_properties_dict
from renter.renter_display_property import renter_display_property
# initialize session state rental_preferences

def search_properties():
    
    st.header("Search Properties")
    
    back_button()
    
    rental_preferences = st.session_state.get("rental_preferences")
    
    user_id = st.session_state.get("user_id")
    
    profile_id = st.session_state.get("profile_id")
    
    # profile
    
    # start with the filter options for the properties (budget_min, budget_max, property_type, property_size_min, property_size_max, bedrooms, bathrooms, floor)
    st.write("**Filter Options:**")
    
    with st.container(border=True):
        with st.expander("Filter Options Help"):
        
            col1, col2 = st.columns([1, 1])
            
            with col2:
                if "budget_min" not in rental_preferences:
                    rental_preferences["budget_min"] = 200.0
                if "budget_max" not in rental_preferences:
                    rental_preferences["budget_max"] = 2000.0
                if "property_type" not in rental_preferences:
                    rental_preferences["property_type"] = "Apartment"
                if "property_size_min" not in rental_preferences:
                    rental_preferences["property_size_min"] = 10.0
                if "property_size_max" not in rental_preferences:
                    rental_preferences["property_size_max"] = 300.0
                if "bedrooms" not in rental_preferences:
                    rental_preferences["bedrooms"] = 1
                if "bathrooms" not in rental_preferences:
                    rental_preferences["bathrooms"] = 1
                if "floor" not in rental_preferences:
                    rental_preferences["floor"] = 0
                    
                budget_min, budget_max = st.slider(
                    "Budget Range (€)",
                    100.0,
                    3000.0,
                    value=(rental_preferences["budget_min"], rental_preferences["budget_max"]),
                    step=50.0,
                    key="budget_slider"
                )
                
                
                property_size_min, property_size_max = st.slider(
                    "Property Size (m²)",
                    10.0,
                    500.0,
                    value=(rental_preferences.get("property_size_min", 10.0), rental_preferences.get("property_size_max", 500.0)),
                    step=5.0,
                    key="property_size_slider"
                )
                
            with col1:
                property_type = st.selectbox(
                    "Type of Property",
                    ["Apartment", "House", "Shared Accommodation"],
                    index=["Apartment", "House", "Shared Accommodation"].index(rental_preferences.get("property_type", "Apartment")),
                    key="property_type"
                )
                bedrooms = st.number_input(
                    "Number of Rooms Needed",
                    min_value=1,
                    step=1,
                    value=rental_preferences.get("bedrooms", 1),
                    key="rooms"
                )
                
                bathrooms = st.number_input(
                    "Number of Bathrooms Needed",
                    min_value=1,
                    step=1,
                    value=rental_preferences.get("bathrooms", 1),
                    key="bathrooms"
                )
                
                floor = st.number_input(
                    "Floor",
                    min_value=0,
                    step=1,
                    value=rental_preferences.get("floor", 0),
                    key="floor"
                )
            
    filter_options = {
        "budget_min": budget_min,
        "budget_max": budget_max,
        "property_type": property_type,
        "property_size_min": property_size_min,
        "property_size_max": property_size_max,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "floor": floor
    }
    st.session_state["rental_preferences"] = filter_options
    
    # button to update rental preferences

    choose = st.selectbox("Update Rental Preferences", ["No", "Yes"])
        
    if choose == "Yes":
        update_rental_preferences(profile_id, filter_options)
        st.success("Rental preferences updated successfully.")
    else:
        pass
    
    # get the properties based on the filter options
    properties = find_matching_properties_dict(filter_options)

    # display the properties
    if not properties:
        st.write("No properties found with the given filter options.")
    else:
        st.write("**Properties Found:**")
        
        columnas_values = ["**TYPE**", "**LOCATION**", "**PRICE**", "**SIZE**", "**BEDROOMS**",
                    "**BATHROOMS**", "**FLOOR**", "**YEAR BUILT**", "**CONDITION**", 
                    "**RENOVATION**", "**AVAILABILITY**", "**FROM**"
                    ]
        columnas = st.columns(len(columnas_values) + 3)
        columnas[0].write("")
        for col, value in zip(columnas[1:], columnas_values):
            col.write(value)
            
        for property in properties:
            renter_display_property(property)
                    
if __name__ == "__main__":
    search_properties()
                    
                
    
        
    