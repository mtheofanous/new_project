import streamlit as st
import uuid
from navigation_buttons import back_button


# Initialize session state for tracking landlords and statuses
if "landlords" not in st.session_state:
    st.session_state["landlords"] = []

if "form_status" not in st.session_state:
    st.session_state["form_status"] = {}

# Initialize other required session state keys
if "address" not in st.session_state:
    st.session_state["address"] = "Not provided"

if "city" not in st.session_state:
    st.session_state["city"] = "Not provided"

if "name" not in st.session_state:
    st.session_state["name"] = "Not provided"

def recommendation_form_page():
    st.title("Landlord Recommendation Form")

    # Professionalized address and tenant introduction
    st.markdown(
        f""" 
        ### Request for Tenant Recommendation

        We are reaching out regarding the property located at **{st.session_state['address']}, {st.session_state['city']}**. 
        Your former tenant, **{st.session_state['name']}**, has requested a recommendation as part of their rental application process. 
        We kindly ask that you complete the following form to provide your feedback on their tenancy. 
        Your input is invaluable in helping us make an informed decision. 
        """
    )

    # Recommendation form fields
    on_time_payment = st.radio("Did the tenant pay rent on time?", ["Yes", "No"])
    utilities_payment = st.radio("Did the tenant pay utility bills on time?", ["Yes", "No"])
    property_condition = st.radio("Did the tenant maintain the property well?", ["Yes", "No"])
    noise_complaints = st.radio("Were there noise or behavioral complaints?", ["No", "Yes"])
    would_recommend = st.radio("Would you recommend this tenant to other landlords?", ["Yes", "No"])
    additional_comments = st.text_area("Additional Comments (Optional)")

def recommendation():
    
    back_button()
    
    st.title("Send Forms to Previous Landlords")

    # Form to add landlord details
    with st.form("add_landlord_form"):
        landlord_name = st.text_input("Landlord's Full Name", placeholder="Jane Doe")
        landlord_email = st.text_input("Landlord's Email", placeholder="landlord@example.com")
        landlord_phone = st.text_input("Landlord's Phone Number", placeholder="+1234567890")
        address = st.text_input("Address", placeholder="123 Main St, Los Angeles, CA")
        city = st.text_input("City", placeholder="Los Angeles")
        submit_button = st.form_submit_button("Add Landlord")
        
        st.session_state["address"] = address
        st.session_state["city"] = city
        st.session_state["landlord_name"] = landlord_name
        st.session_state["landlord_email"] = landlord_email
        st.session_state["landlord_phone"] = landlord_phone
        

        if submit_button:
            if not landlord_name or not landlord_email or not landlord_phone:
                st.error("Please fill in all fields before adding a landlord.")
            else:
                landlord_id = str(uuid.uuid4())
                st.session_state["landlords"].append({
                    "id": landlord_id,
                    "name": landlord_name,
                    "email": landlord_email,
                    "phone": landlord_phone,
                    "address": address,
                    "city": city,
                })
                st.session_state["form_status"][landlord_id] = "Pending"
                st.success(f"Landlord {landlord_name} added successfully!")

    # Display list of landlords and their statuses
    st.markdown("### Landlords and Form Status")

    if not st.session_state["landlords"]:
        st.info("No landlords added yet.")
    else:
        for landlord in st.session_state["landlords"]:
            status = st.session_state["form_status"].get(landlord["id"], "Pending")
            st.markdown(f"**Name:** {landlord['name']}  \
**Email:** {landlord['email']}  \
**Phone:** {landlord['phone']}  \
**Address:** {landlord['address']}  \
**City:** {landlord['city']}  \
**Status:** {status}")
            if status == "Pending":
                with st.expander("Preview Form", expanded=False):
                        recommendation_form_page()
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Send Form to {landlord['name']}", key=f"send_{landlord['id']}"):
                        # Simulate sending the form (e.g., via email)
                        link = f"https://yourapp.com/recommendation_form?landlord_id={landlord['id']}"
                        st.session_state["form_status"][landlord["id"]] = "Sent"
                        st.info(f"Form sent to {landlord['email']}. **Link:** {link}")
                with col2:
                    # delete landlord
                    if st.button(f"Delete Form for {landlord['name']}", key=f"delete_{landlord['id']}"):
                        st.session_state["landlords"] = [l for l in st.session_state["landlords"] if l["id"] != landlord["id"]]
                        del st.session_state["form_status"][landlord["id"]]
                        st.success(f"Form for {landlord['name']} deleted successfully!")

if __name__ == "__main__":
    recommendation()