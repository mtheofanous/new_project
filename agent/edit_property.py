import streamlit as st
from database import *
def back_button():
    if st.button("Back", key="back_button"):
        st.session_state["current_page"] = st.session_state.get("previous_page", "listing")
        st.rerun()

def edit_property_with_images():
    
    back_button()
    user_id = st.session_state.get("user_id")
    
    st.title("Edit Property")

    st.write("---")
    property_id = st.session_state.get("selected_property", {}).get("id")
    if not property_id:
        st.error("No property selected for editing.")
        return
    selected_property = load_property_by_id(property_id)
        # Load current images
    existing_images = load_property_images(property_id)
        # Create labels for the images to display in the multiselect
    image_labels = [
        f"Image {idx + 1} ({'URL' if img['src'] else 'Uploaded'})"
        for idx, img in enumerate(existing_images)
    ]

    # Allow users to select images for deletion using their indices
    images_to_delete_indices = st.multiselect(
        "Select images to delete",
        options=list(range(len(existing_images))),  # Use indices as options
        format_func=lambda idx: image_labels[idx]  # Format the display label
    )

    # Filter remaining images
    remaining_images = [
        img for idx, img in enumerate(existing_images) if idx not in images_to_delete_indices
    ]
    
    # Display remaining images in rows of 4
    for i in range(0, len(remaining_images), 4):
        cols = st.columns(4)  # Create 4 columns for a row
        for col, img in zip(cols, remaining_images[i:i + 4]):
            with col:
                if img["src"]:
                    st.image(img["src"], width=150, caption="Image URL")
                elif img["blob"]:
                    st.image(img["blob"], width=150, caption="Uploaded Image")




    friendly_name = st.text_input("Friendly Name", value=selected_property.get("friendly_name", ""))
    property_type = st.text_input("Property Type", value=selected_property.get("property_type", ""))
    property_size = st.number_input("Property Size", value=selected_property.get("property_size", 0.0))
    property_location = st.text_input("Property Location", value=selected_property.get("property_location", ""))
    property_price = st.number_input("Property Price (€)", value=selected_property.get("property_price", 0.0))
    price_per_sqm = st.number_input("Price per sqm (€)", value=selected_property.get("price_per_sqm", 0.0))
    bedrooms = st.number_input("Bedrooms", value=selected_property.get("bedrooms", 0))
    bathrooms = st.number_input("Bathrooms", value=selected_property.get("bathrooms", 0))
    floor = st.number_input("Floor", value=selected_property.get("floor", 0))
    year_built = st.number_input("Year Built", value=selected_property.get("year_built", 0))
    condition = st.text_input("Condition", value=selected_property.get("condition", ""))
    energy_class = st.text_input("Energy Class", value=selected_property.get("energy_class", ""))
    availability = st.text_input("Availability", value=selected_property.get("availability", ""))
    available_from = st.text_input("Available From", value=selected_property.get("available_from", ""))
    heating_method = st.text_input("Heating Method", value=selected_property.get("heating_method", ""))
    zone = st.text_input("Zone", value=selected_property.get("zone", ""))
    
        

    # Image upload
    uploaded_files = st.file_uploader("Upload New Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    new_image_urls = st.text_area("Enter Image URLs (comma-separated)").split(",")


    # Handle Form Submission
    if st.button('Save Changes', key=f'save_changes_{property_id}'):
        if not friendly_name:
            st.error("Please enter a friendly name.")
            return
        updated_property = {
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
            "energy_class": energy_class,
            "availability": availability,
            "available_from": available_from,
            "heating_method": heating_method,
            "zone": zone,
            "creation_method": selected_property.get("creation_method", "manual")
        }
        
        normalized_new_images = []
        if uploaded_files:
            normalized_new_images += [{"src": None, "blob": file.read()} for file in uploaded_files]
        if new_image_urls:
            normalized_new_images += [{"src": url.strip(), "blob": None} for url in new_image_urls if url.strip()]
  
        images = normalized_new_images + remaining_images 
        
        # Debugging
        st.write("Remaining Images:", remaining_images)
        st.write("New Images:", normalized_new_images)
        st.write("Combined Images:", images)
        
        try:
            update_property_in_db(property_id, updated_property, user_id)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return
        try:
            if images:
                replace_property_images(property_id, user_id, images)
            else:
                st.warning("No images provided. Existing images will be deleted.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return
        # Success message
        st.success("Property updated successfully!")
        # Reset session state
        st.session_state["current_page"] = "listing"
        st.session_state["expander_open"] = False
        st.rerun()

 

if __name__ == "__main__":
    edit_property_with_images()