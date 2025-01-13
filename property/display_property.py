import streamlit as st
from queries.property import delete_property_from_db

# Display properties
def display_property(property):
    property_id = property.get('id')
    # property_images = property.get('images', [])
    columns_value = [property['friendly_name'], property['property_type'], 
                     property['property_location'], property['property_price'], 
                     property['property_size'], property['bedrooms'], property['bathrooms'], 
                     property['floor'], property['year_built'], property['condition'], 
                     property['renovation_year'], property['energy_class'], 
                     property['availability'], property['available_from'], 
                     property['heating_method'], property['zone']]
        
    with st.container(border=True):

        columnas = st.columns(len(columns_value) + 3)
        for col, value in zip(columnas, columns_value):
            col.write(value)
        if columnas[-3].button("📂", key=f"preview_{property['id']}"):
            st.session_state.current_page = "preview_property"
            st.session_state["selected_property"] = property
            st.rerun()
        if columnas[-2].button("🖊️", key=f"edit_{property['id']}"):
            st.session_state.current_page = "edit_property"
            st.session_state["selected_property"] = property
            st.rerun()
            
        # Delete Property
        # Initialize session state for delete confirmation
        delete_key = f"delete_{property['id']}"
        confirm_key = f"confirm_delete_{property['id']}"
        cancel_key = f"cancel_delete_{property['id']}"
        
        if delete_key not in st.session_state:
            st.session_state[delete_key] = False

        # Delete button
        if columnas[-1].button("🗑️", key=f"delete_button_{property['id']}"):
            st.session_state[delete_key] = True

        # Show confirmation dialog
        if st.session_state[delete_key]:
            columnas[-1].warning("Are you sure you want to delete this property?")
            col_yes, col_no = st.columns([1, 1])
            with col_yes:
                if columnas[-1].button("Yes", key=confirm_key):
                    delete_property_from_db(property['id'])
                    st.success("Property deleted successfully.")
                    # Reset the session state
                    st.session_state[delete_key] = False
                    st.rerun()
            with col_no:
                if columnas[-1].button("No", key=cancel_key):
                    st.session_state[delete_key] = False
                    st.rerun()

    
                
