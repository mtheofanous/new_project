import streamlit as st
from database import get_users_for_similar_properties

def back_button():
    if st.button("Back", key="back_button"):
        st.session_state["current_page"] = st.session_state.get("previous_page", "listing")
        st.rerun()

def display_images(property):
    property_images = property.get('images', [])
    
    if not property_images:
        st.write("No images available.")
        return
    for i in range(0, len(property_images), 3):
        columns = st.columns(3)
        for col, img in zip(columns, property_images[i:i+3]):
            with col:
                if img["src"]:
                    st.image(img["src"], width=300)
                elif img["blob"]:
                    st.image(img["blob"], width=300)
                        
def preview_property(property):
    
    back_button()
    
    if not property:
        st.error("No property data available.")
        return
    
    st.header(f"Previewing: {property['friendly_name']}")
    
    columns = st.columns([1, 2, 5])
    
    with columns[0]:
        st.write(f"**Friendly Name:** {property['friendly_name']}")
        st.write(f"**Property Type:** {property['property_type']}")
        st.write(f"**Location:** {property['property_location']}")
        st.write(f"**Price:** €{property['property_price']} per month")
        st.write(f"**Size:** {property['property_size']} sqm")
        st.write(f"**Bedrooms:** {property['bedrooms']}")
        st.write(f"**Bathrooms:** {property['bathrooms']}")
        st.write(f"**Floor:** {property['floor']}")
    with columns[1]:
        st.write(f"**Year Built:** {property['year_built']}")
        st.write(f"**Condition:** {property['condition']}")
        st.write(f"**Renovation Year:** {property['renovation_year']}")
        st.write(f"**Energy Class:** {property['energy_class']}")
        st.write(f"**Availability:** {property['availability']}")
        st.write(f"**Available From:** {property['available_from']}")
        st.write(f"**Heating Method:** {property['heating_method']}")
        st.write(f"**Zone:** {property['zone']}")
    
    # Associated Users
    users = get_users_for_similar_properties(property["id"])
    st.write("**Associated Users:**")
    if users:
        for user in users:
            role_icon = "👤 Agent" if user['role'] == "renter" else "🏠 Landlord"
            st.write(f"- {user['username']} - {role_icon}")
    else:
        st.write("No associated users.")
        
    st.write("---")
    with columns[2]:
        display_images(property)
    
if __name__ == "__main__":
    preview_property(property)
    



    