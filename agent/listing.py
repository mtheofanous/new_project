import streamlit as st
from navigation_buttons import home_button, back_button, log_out_button
from app.components.utils import scrape_data_to_dict
from database import * 
from db_setup import get_db_connection
from agent.display_property import display_property
import base64


def listing():
    
    back_button()
    
    # Property Generator
    if "expander_open" not in st.session_state:
        st.session_state["expander_open"] = True

    
    st.header("Property Generator")
    with st.expander("**Property Generator**", expanded=st.session_state["expander_open"]):
        st.write("Enter a property URL to generate its profile.")
        
        choose_method = st.radio("Choose a method to input the property:",("Enter URL", "Manual Input"))

        if choose_method == "Enter URL":

            url = st.text_input("Property URL:", placeholder="Enter the property URL here")
            if st.button("Generate Profile"):
                if url: 
                    with st.spinner("Scraping data..."):
                        try:
                            property_data = scrape_data_to_dict(url)
                            
                            # images
                            images = property_data.get('images', [])
                            
                            characteristics = property_data.get('characteristics', {})
                            
                            # floor
                            floor = characteristics['Floor'] if 'Floor' in characteristics else None
                            
                            floor = floor.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").strip()
                            floor = int(floor) if floor else None
                            
                            st.success("Data scraped successfully!")
        
                            
                            property = {
                                
                                "friendly_name": property_data.get('friendly_name', 'No Friendly Name'),
                                "property_type": property_data.get('property_type', 'No Property Type'), # cannot be None or empty 
                                "property_size": property_data.get('property_size', 0.0) if property_data.get('property_size') else 0.0,
                                "property_location": property_data.get('property_location', 'No Property Location'),
                                "property_price": property_data.get('property_price', 0.0) if property_data.get('property_price') else 0.0,
                                "price_per_sqm": property_data.get('price_per_sqm', 0.0) if property_data.get('price_per_sqm') else 0.0,
                                "bedrooms": characteristics.get('Bedrooms', 0) if characteristics.get('Bedrooms') else 0,
                                "bathrooms": characteristics.get('Bathrooms', 0) if characteristics.get('Bathrooms') else 0,
                                "floor": floor,
                                "year_built": characteristics.get('Year Built', 1990) if characteristics.get('Year Built') else 1990,
                                "condition": characteristics.get('Condition', 'N/A'),
                                "renovation_year": characteristics.get('Renovation Year', 2000) if characteristics.get('Renovation Year') else 2000,
                                "energy_class": characteristics.get('Energy Class', 'N/A'),
                                "availability": characteristics.get('Availability', 'N/A'),
                                "available_from": characteristics.get('Available From', 'N/A'),
                                "heating_method": characteristics.get('Heating Method', 'N/A'),
                                "zone": characteristics.get('Zone', 'N/A'),
                                "creation_method": "url"
                            }
                                                        
                            user_id = st.session_state.get("user_id")
                            property_id = save_property_to_db(property, user_id)
                            
                            # save images
                            save_property_image_to_db(property_id, user_id, images)
                            
                            if 'role' not in st.session_state:
                                st.session_state["role"] = "agent"
                            
                            role = st.session_state.get("role")
                            if role:
                                role = role.lower()
                            else:
                                raise ValueError("Role not set. Please set the role to 'landlord' or 'agent'.")
                            if role not in ['landlord', 'agent']:
                                raise ValueError("Invalid role. Please ensure the role is set to 'landlord' or 'agent'.")

                            save_property_ownership(property_id, user_id, role)
                            st.success("Property saved successfully!")
                                                     
                            # close the expander
                            st.session_state["expander_open"] = False
                            
                            st.rerun()
                    
                                                                                   
                        
                        except Exception as e:
                            st.error(f"An error occurred: {e}")
                            
                else:
                    st.warning("Please enter a URL.")
                    
        elif choose_method == "Manual Input":
            
            # add manual input fields
            friendly_name = st.text_input("Friendly Name:", placeholder="Enter the friendly name here")
            property_type = st.text_input("Property Type:", placeholder="Enter the property type here")
            property_size = st.text_input("Property Size:", placeholder="Enter the property size here")
            property_location = st.text_input("Property Location:", placeholder="Enter the property location here")
            property_price = st.text_input("Property Price:", placeholder="Enter the property price here")
            price_per_sqm = st.text_input("Price per sqm:", placeholder="Enter the price per sqm here")
            bedrooms = st.text_input("Bedrooms:", placeholder="Enter the number of bedrooms here")
            bathrooms = st.text_input("Bathrooms:", placeholder="Enter the number of bathrooms here")
            floor = st.text_input("Floor:", placeholder="Enter the floor number here")
            year_built = st.text_input("Year Built:", placeholder="Enter the year built here")
            condition = st.text_input("Condition:", placeholder="Enter the condition here")
            renovation_year = st.text_input("Renovation Year:", placeholder="Enter the renovation year here")
            energy_class = st.text_input("Energy Class:", placeholder="Enter the energy class here")
            availability = st.text_input("Availability:", placeholder="Enter the availability here")
            available_from = st.text_input("Available From:", placeholder="Enter the available from here")
            heating_method = st.text_input("Heating Method:", placeholder="Enter the heating method here")
            zone = st.text_input("Zone:", placeholder="Enter the zone here")
            
            if st.button("Save Property"):
                property = {
                    "friendly_name": friendly_name,
                    "property_type": property_type,
                    "property_size": property_size,
                    "property_location": property_location,
                    "property_price": property_price,
                    "price_per_sqm": price_per_sqm,
                    "bedrooms": bedrooms,
                    "bathrooms": bathrooms,
                    "floor": floor,
                    "year_built": year_built,
                    "condition": condition,
                    "renovation_year": renovation_year,
                    "energy_class": energy_class,
                    "availability": availability,
                    "available_from": available_from,
                    "heating_method": heating_method,
                    "zone": zone,
                    "creation_method": "manual"
                }
                
                
                user_id = st.session_state.get("user_id")
                property_id = save_property_to_db(property, user_id)
                
                save_property_image_to_db(property_id, user_id, images)
                
                if 'role' not in st.session_state:
                    st.session_state["role"] = "agent"
                
                role = st.session_state.get("role")
                if role:
                    role = role.lower()
                else:
                    raise ValueError("Role not set. Please set the role to 'landlord' or 'agent'.")
                if role not in ['landlord', 'agent']:
                    raise ValueError("Invalid role. Please ensure the role is set to 'landlord' or 'agent'.")
                
                save_property_ownership(property_id, user_id, role)
                st.success("Property saved successfully!")
                st.rerun()
                # close the expander
                st.session_state["expander_open"] = False             

# Listing Page

    # Header for Property Listing
    st.header("Property Listing")
    columnas_values = ["**NICKNAME**", "**TYPE**", "**LOCATION**", "**PRICE**", "**SIZE**", "**BEDROOMS**",
                       "**BATHROOMS**", "**FLOOR**", "**YEAR BUILT**", "**CONDITION**", 
                       "**RENOVATION**", "**ENERGY CLASS**", "**AVAILABILITY**", "**FROM**", 
                       "**HEATING**", "**ZONE**"]
    columnas = st.columns(len(columnas_values) + 3)
    for col, value in zip(columnas, columnas_values):
        col.write(value)
        
    # Check if user is logged in
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("User not logged in.")
        return

    if "role" not in st.session_state:
        st.session_state["role"] = "agent"

    role = st.session_state.get("role", "").lower()
    if not role:
        raise ValueError("Role not set. Please set the role to 'landlord' or 'agent'.")
  
    # Load properties
    properties = load_properties_by_user(user_id, role)
            
    # Display properties
    if not properties:
        st.write("You have no properties listed yet.")
    else:
        for property in properties:
            display_property(property)

                                            

if __name__ == "__main__":
    listing()
