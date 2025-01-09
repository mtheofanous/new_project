import streamlit as st
from navigation_buttons import home_button, back_button, log_out_button
from app.components.utils import scrape_data_to_dict
from database import * 
from db_setup import get_db_connection
from agent.edit_property import edit_property_with_images
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
                            
                            st.success("Data scraped successfully!")
                            
                            property = {
                                "friendly_name": property_data.get('friendly_name', 'No Friendly Name'),
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
    def proper(column, prop):
        property_images = prop.get('images', [])
        columnas = st.columns([2,1,3])
        
        if property_images:
            # First Image
            first_image = property_images[0]
            if first_image["src"]:
                columnas[0].image(first_image["src"], output_format="auto", width=200)
            elif first_image["blob"]:
                columnas[0].image(first_image["blob"], output_format="auto", width=200)
                
            if f"view_more_images_{prop['id']}" not in st.session_state:
                st.session_state[f"view_more_images_{prop['id']}"] = False

            # Toggle Button
            if columnas[1].button(
                "🔍",
                key=f"view_more_images_toggle_{prop['id']}"
            ):
                # Toggle the state
                st.session_state[f"view_more_images_{prop['id']}"] = not st.session_state[f"view_more_images_{prop['id']}"]

            # Conditional Display of Additional Images
            if st.session_state[f"view_more_images_{prop['id']}"]:
                additional_images = property_images[1:]  # Skip the main image
                for i in range(0, len(additional_images), 3):  # Display 3 images per row
                    additional_cols = st.columns(3)
                    for img_col, img in zip(additional_cols, additional_images[i:i+3]):
                        with img_col:
                            if img["src"]:
                                st.image(img["src"], width=150)
                            elif img["blob"]:
                                st.image(img["blob"], width=150)
        

        else:
            st.write("No images available.")

        # Property Details
        columnas[1].markdown(f"<h3> {prop['friendly_name']}- {prop['property_type']} - {prop['property_location']}</h3>", unsafe_allow_html=True)
        columnas[1].write(f"**Price:** €{round(prop.get('property_price', 'N/A'))}")
        columnas[1].write(f"**Size:** {round(prop.get('property_size', 'N/A'))} sqm")
        columnas[1].write(f"**Bedrooms:** {prop.get('bedrooms', 'N/A')}")
        columnas[2].write(f"**Bathrooms:** {prop.get('bathrooms', 'N/A')}")
        columnas[2].write(f"**Floor:** {prop.get('floor', 'N/A')}")
        columnas[2].write(f"**Year Built:** {prop.get('year_built', 'N/A')}")

        # View More Details
        
        with st.expander("📂", expanded=False):
            st.write(f"**Condition:** {prop.get('condition', 'N/A')}")
            st.write(f"**Renovation Year:** {prop.get('renovation_year', 'N/A')}")
            st.write(f"**Energy Class:** {prop.get('energy_class', 'N/A')}")
            st.write(f"**Availability:** {prop.get('availability', 'N/A')}")
            st.write(f"**Available From:** {prop.get('available_from', 'N/A')}")
            st.write(f"**Heating Method:** {prop.get('heating_method', 'N/A')}")
            st.write(f"**Zone:** {prop.get('zone', 'N/A')}")

            # Associated Users
            users = get_users_for_similar_properties(prop["id"])
            st.write("**Associated Users:**")
            if users:
                for user in users:
                    role_icon = "👨‍💼 " if user["role"] == "agent" else "🏠 "
            else:
                st.write("No users associated with this property.")

        # Action Button
        if col[1].button(f"🗑️", key=f"delete_property_{prop['id']}"):
            st.info(f"Deleting Property is not yet implemented.")
            

    # Display properties
    if not properties:
        st.write("You have no properties listed yet.")
    else:
        if len(properties) > 1:
            additional_properties = properties[1:]
            for p in range(0, len(additional_properties), 3):
                
                cols = st.columns(3)  # Create columns for properties
                
                for col, prop in zip(cols, additional_properties[p:p+3]):
                    
                    with col:
                            
                            col = st.columns([2, 1]) 
                            col[0].markdown(f'<h3>{prop["property_type"]} - {prop["property_location"]}</h3>', unsafe_allow_html=True)
                            proper(col, prop)
                            
                        # Property Images
                        
                    

if __name__ == "__main__":
    listing()
