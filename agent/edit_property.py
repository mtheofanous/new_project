import streamlit as st
from database import load_properties_by_user, load_property_images, update_property_in_db, replace_property_images
from navigation_buttons import home_button, back_button, log_out_button
def edit_property_with_images():
    
    back_button()
    user_id = st.session_state.get("user_id")
    
    st.title("Edit Property")

    # Fetch all properties for the current user
    properties = load_properties_by_user(user_id)
    if not properties:
        st.error("No properties found for this user.")
        return

    selected_property = st.selectbox(
        "Select a property to edit:",
        options=properties,
        format_func=lambda p: f"{p['property_type']} at {p['property_location']}"
    )

    if not selected_property:
        st.warning("Please select a property to proceed.")
        return

    property_id = selected_property["id"]
    st.write("---")
    
    if "expander_open" not in st.session_state:
        st.session_state["expander_open"] = False
    
    with st.expander("Property Details", expanded=st.session_state["expander_open"]):
        st.subheader(f"Editing: {selected_property['property_type']} at {selected_property['property_location']}")

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



        # Editable form
        with st.form("edit_property_form"):
            property_type = st.text_input("Property Type", value=selected_property.get("property_type", ""))
            property_size = st.text_input("Property Size", value=round(selected_property.get("property_size", "")))
            property_location = st.text_input("Property Location", value=selected_property.get("property_location", ""))
            property_price = st.number_input("Property Price (€)", value=round(selected_property.get("property_price", 0)))
            bedrooms = st.text_input("Bedrooms", value=selected_property.get("bedrooms", 0))
            bathrooms = st.text_input("Bathrooms", value=selected_property.get("bathrooms", 0))
            floor = st.text_input("Floor", value=selected_property.get("floor", ""))
            year_built = st.text_input("Year Built", value=selected_property.get("year_built", ""))
            condition = st.text_input("Condition", value=selected_property.get("condition", ""))
            energy_class = st.text_input("Energy Class", value=selected_property.get("energy_class", ""))
            availability = st.text_input("Availability", value=selected_property.get("availability", ""))
            # available_from is saved as a string in the database
            available_from = st.text_input("Available From", value=selected_property.get("available_from", ""))
            heating_method = st.text_input("Heating Method", value=selected_property.get("heating_method", ""))
            zone = st.text_input("Zone", value=selected_property.get("zone", ""))

            # Image upload
            uploaded_files = st.file_uploader("Upload New Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
            new_image_urls = st.text_area("Enter Image URLs (comma-separated)").split(",")

            # Submit Button
            submit_button = st.form_submit_button("Save Changes")

        # Handle Form Submission
        if submit_button:
            updated_property = {
                "property_type": property_type,
                "property_size": property_size,
                "property_location": property_location,
                "property_price": property_price,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "floor": floor,
                "year_built": year_built,
                "condition": condition,
                "energy_class": energy_class,
                "availability": availability,
                "available_from": available_from,
                "heating_method": heating_method,
                "zone": zone
            }

            # Prepare new images
            new_images = [{"src": url.strip(), "blob": None} for url in new_image_urls if url.strip()]
            for uploaded_file in uploaded_files:
                new_images.append({"src": None, "blob": uploaded_file.read()})

            try:
                update_property_in_db(property_id, updated_property, user_id)
                # new images and remaining_images
                images = new_images + remaining_images
                replace_property_images(property_id, user_id, images)
                st.success("Property updated successfully!")
                                
                st.session_state["expander_open"] = False
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    edit_property_with_images()