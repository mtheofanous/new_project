import streamlit as st
from database import save_property_interest, delete_property_interest, has_expressed_interest

# Display properties
def renter_display_property(property):
    property_id = property.get('id')
    property_images = property.get('images', [])
    columnas_value = [ property['property_type'], 
                     property['property_location'], property['property_price'], 
                     property['property_size'], property['bedrooms'], property['bathrooms'], 
                     property['floor'], property['year_built'], property['condition'], 
                     property['renovation_year'], property['energy_class'], 
                     property['availability'], property['available_from'], 
                     property['heating_method'], property['zone']]

        
    with st.container(border=True):

        columnas = st.columns(len(columnas_value) + 3)
        columnas[0].image(property_images[0]["src"], width=150)
        for col, value in zip(columnas[1:], columnas_value):
            col.write(value)
        if columnas[-2].button("📂", key=f"renter_preview_{property['id']}"):
            st.session_state.current_page = "renter_preview_property"
            st.session_state["renter_selected_property"] = property
            st.rerun()
            
        # i want if the user has already saved the property to show the heart filled in red and if not to show the heart empty
        # Ensure the session state for "show_interest" is a dictionary
        if "show_interest" not in st.session_state or not isinstance(st.session_state.show_interest, dict):
            st.session_state.show_interest = {}
    

        # Check if the user has already expressed interest in the property
        user_id = st.session_state.get("user_id")  # Assume user_id is stored in session state
        property_id = property["id"]  # Assume `property` is the current property object

        if property_id not in st.session_state.show_interest:
            st.session_state.show_interest[property_id] = has_expressed_interest(property_id, user_id)

        # Display the appropriate button based on interest status
        if not st.session_state.show_interest[property_id]:
            if columnas[-1].button("🤍", key=f"save_interest_{property_id}"):
                if save_property_interest(property_id, user_id):
                    st.session_state.show_interest[property_id] = True
                    st.success("Interest saved successfully!")
                    st.experimental_rerun()
        else:
            if columnas[-1].button("❤️", key=f"remove_interest_{property_id}"):
                if delete_property_interest(property_id, user_id):  # Ensure this function is implemented
                    st.session_state.show_interest[property_id] = False
                    st.success("Interest removed successfully!")
                    st.experimental_rerun()
                    