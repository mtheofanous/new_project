import streamlit as st
from queries.property import save_property_interest, delete_property_interest, has_expressed_interest
from queries.queries_favorites import *
# Display properties
def renter_display_property(property):
    property_id = property.get('id')
    property_images = property.get('images', [])
    columnas_value = [ property['property_type'], 
                     property['property_location'], property['property_price'], 
                     property['property_size'], property['bedrooms'], property['bathrooms'], 
                     property['floor'], property['year_built'], property['condition'], 
                     property['renovation_year'], 
                     property['availability'], property['available_from']
                    ]
       

    with st.container(border=True):

        columnas = st.columns(len(columnas_value) + 3)
        columnas[0].image(property_images[0]["src"], width=150)
        for col, value in zip(columnas[1:], columnas_value):
            col.write(value)
        if columnas[-3].button("📂", key=f"renter_preview_{property['id']}"):
            st.session_state.current_page = "renter_preview_property"
            st.session_state["renter_selected_property"] = property
            st.rerun()
            
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
            if columnas[-2].button("Send request", key=f"save_interest_{property_id}"):
                if save_property_interest(property_id, user_id):
                    st.session_state.show_interest[property_id] = True
                    st.success("Interest saved successfully!")
                    st.rerun()
        else:
            if columnas[-2].button("Request sended", key=f"remove_interest_{property_id}"):
                if delete_property_interest(property_id, user_id):  # Ensure this function is implemented
                    st.session_state.show_interest[property_id] = False
                    st.success("Interest removed successfully!")
                    st.rerun()
                    
        # add button to add to favorites
        # ensure that the session state for "show_favorite" is a dictionary
        if "show_favorite" not in st.session_state or not isinstance(st.session_state.show_favorite, dict):
            st.session_state.show_favorite = {}
            
        # check if the user has already added the property to favorites
        user_id = st.session_state.get("user_id")
        property_id = property["id"] # Assume `property` is the current property object
        
        if property_id not in st.session_state.show_favorite:
            st.session_state.show_favorite[property_id] = is_favorited(user_id, "property", property_id)
            
        # display the appropriate button based on favorite status
        
        if not st.session_state.show_favorite[property_id]:
            if columnas[-1].button("❤️", key=f"save_favorite_{property_id}"):
                if save_to_favorites(user_id, "property", property_id):
                    st.session_state.show_favorite[property_id] = True
                    st.success("Property added to favorites successfully!")
                    st.rerun()
        else:
            if columnas[-1].button("🤍", key=f"remove_favorite_{property_id}"):
                if remove_from_favorites(user_id, "property", property_id):
                    st.session_state.show_favorite[property_id] = False
                    st.success("Property removed from favorites successfully!")
                    st.rerun()
        