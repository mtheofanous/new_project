import streamlit as st
from navigation_buttons import home_button, back_button, log_out_button
from app.components.utils import scrape_data_to_dict
from database import load_properties_by_user, save_property_ownership, save_property_to_db, get_users_for_property
from db_setup import get_db_connection
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
                            
                            characteristics = property_data.get('characteristics', {})
                            
                            st.success("Data scraped successfully!")
                            
                            property = {
                                "property_type": property_data.get('property_type', 'No Property Type'), # cannot be None or empty 
                                "property_size": property_data.get('property_size', 'No Property Size'),
                                "property_location": property_data.get('property_location', 'No Property Location'),
                                "property_price": property_data.get('property_price', 'No Property Price'),
                                "price_per_sqm": property_data.get('price_per_sqm', 'N/A'),
                                "bedrooms": characteristics.get('Bedrooms', 'N/A'),
                                "bathrooms": characteristics.get('Bathrooms', 'N/A'),
                                "floor": characteristics.get('Floor', 'N/A'),
                                "year_built": characteristics.get('Year Built', 'N/A'),
                                "condition": characteristics.get('Condition', 'N/A'),
                                "renovation_year": characteristics.get('Renovation Year', 'N/A'),
                                "energy_class": characteristics.get('Energy Class', 'N/A'),
                                "availability": characteristics.get('Availability', 'N/A'),
                                "available_from": characteristics.get('Available From', 'N/A'),
                                "heating_method": characteristics.get('Heating Method', 'N/A'),
                                "zone": characteristics.get('Zone', 'N/A'),
                                "creation_method": "url"
                            }
                                                        
                            property_id = save_property_to_db(property)                        
                            user_id = st.session_state.get("user_id")
                            
                            
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
                
                property_id = save_property_to_db(property)
                user_id = st.session_state.get("user_id")
                
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
            
    st.header("Property Listing")

    # Display property listings for the current user
    with st.expander("**Property Listing**"):
        st.write("Here you can view and manage your property listings.")
        
        user_id = st.session_state.get("user_id")
        if not user_id:
            st.error("User not logged in.")
            return
        
        if 'role' not in st.session_state:
            st.session_state["role"] = "agent"
        
        role = st.session_state.get("role")
        if role:
            role = role.lower()
        else:
            raise ValueError("Role not set. Please set the role to 'landlord' or 'agent'.")
        
        properties = load_properties_by_user(user_id, role) 

        try:
            # properties = load_properties_by_user(user_id)
            if not properties:
                st.write("You have no properties listed yet.")
            else:
                for property in properties:
                    st.write(f"**Type:** {property.get('property_type', 'N/A')}")
                    st.write(f"**Location:** {property.get('property_location', 'N/A')}")
                    st.write(f"**Price:** €{property.get('property_price', 'N/A')}")
                    st.write(f"**Size:** {property.get('property_size', 'N/A')} sq.m.")
                    st.write(f"**Bedrooms:** {property.get('bedrooms', 'N/A')}")
                    st.write(f"**Floor:** {property.get('floor', 'N/A')}")

                    # Fetch and display associated users
                    users = get_users_for_property(property['id'])
                    st.write(f"**Associated Users:**")
                    if users:
                        for user in users:
                            role_icon = "👨‍💼" if user["role"] == "agent" else "🏠"
                            st.write(f"{role_icon} **{user['username']}** | **Email**: {user['email']} | **Role**: {user['role']}")
                    else:
                        st.write("No users associated with this property.")

                    # Action buttons for properties
                    # delete property
                    if st.button(f"Delete Property ID {property['id']}", key=f"delete_{property['id']}"):
                        st.info(f"Deleting Property ID {property['id']} is not yet implemented.")
  
                    st.markdown("---")

        except Exception as e:
            st.error(f"Error loading properties: {e}")


if __name__ == "__main__":
    listing()
# def listing():
    
#     back_button()
    
#     property_generator()
    
#     st.title("Property Listing")
    
#     with st.expander("Property Listing"):
#         st.write("Here you can view and manage your property listings.")
#         user_id = st.session_state["user_id"]
#         properties = load_properties_by_user(user_id)
        
#         if not properties:
#             st.write("You have no properties listed yet.")
#         else:
#             for property in properties:
#                 st.write(f"**Property ID:** {property['id']}")
#                 st.write(f"**Name:** {property['name']}")
#                 st.write(f"**Location:** {property['location']}")
#                 st.write(f"**Price:** ${property['price']} per month")
#                 st.write(f"**Rooms:** {property['rooms']}")
#                 st.write(f"**Status:** {property['status']}")
#                 users = get_users_for_property(property['id'])
#                 st.write(f"**Users:**")
#                 for user in users:
#                     st.write(f"Username: {user['username']}, Email: {user['email']}, Role: {user['role']}")
#                 if st.button(f"View Details for Property ID {property['id']}", key=f"view_{property['id']}"):
#                     st.info(f"Details for Property ID {property['id']} are not yet implemented.")
#                 if st.button(f"Edit Property ID {property['id']}", key=f"edit_{property['id']}"):
#                     st.info(f"Editing Property ID {property['id']} is not yet implemented.")
#                 st.markdown("---")
    
    
    
           
    
            
# if __name__ == "__main__":
#     listing()