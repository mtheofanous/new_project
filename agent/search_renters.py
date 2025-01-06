import streamlit as st
import sqlite3
from navigation_buttons import back_button
from db_setup import get_db_connection

import streamlit as st
import sqlite3

import streamlit as st
import sqlite3

def get_db_connection():
    """Create and return a connection to the SQLite database."""
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Enable accessing columns by name
    return conn

def search_renters():
    st.title("Search Renters")

    # Search filters
    st.sidebar.header("Filter Renters")

    # Filters for Renter Profiles Table
    st.sidebar.subheader("Renter Profiles")
    min_age = st.sidebar.number_input("Minimum Age", min_value=18, step=1)
    max_age = st.sidebar.number_input("Maximum Age", min_value=18, step=1)
    nationality = st.sidebar.text_input("Nationality")
    contract_type = st.sidebar.text_input("Contract Type")
    min_income = st.sidebar.number_input("Minimum Income", min_value=0.0, step=1000.0)
    max_income = st.sidebar.number_input("Maximum Income", min_value=0.0, step=1000.0)
    work_mode = st.sidebar.text_input("Work Mode")

    # Filters for Rental Preferences Table
    st.sidebar.subheader("Rental Preferences")
    preferred_city = st.sidebar.text_input("Preferred City")
    preferred_area = st.sidebar.text_input("Preferred Area")
    budget_min = st.sidebar.number_input("Minimum Budget (€)", min_value=0.0, step=50.0)
    budget_max = st.sidebar.number_input("Maximum Budget (€)", min_value=0.0, step=50.0)
    property_type = st.sidebar.selectbox("Property Type", ["Any", "Apartment", "House", "Studio", "Shared Room"])
    rooms_needed = st.sidebar.number_input("Rooms Needed", min_value=0, step=1)
    number_of_people = st.sidebar.number_input("Number of People", min_value=1, step=1)
    move_in_date = st.sidebar.date_input("Move-in Date")
    pets = st.sidebar.selectbox("Pets", ["Any", "Yes", "No"])
    lease_duration = st.sidebar.selectbox("Lease Duration", ["Any", "Short-Term", "Long-Term"])

    # Filters for Credit Score
    st.sidebar.subheader("Additional Filters")
    credit_score_status = st.sidebar.selectbox("Credit Score Status", ["Any", "Verified", "Not Verified", "Pending"])

    # Submit button
    if st.sidebar.button("Search"):
        query = """
        SELECT rp.*, rpfs.*, rcs.status AS credit_score_status
        FROM renter_profiles rp
        JOIN rental_preferences rpfs ON rp.id = rpfs.profile_id
        LEFT JOIN renter_credit_scores rcs ON rp.user_id = rcs.user_id
        WHERE 1=1
        """
        params = []

        # Filters for Renter Profiles
        if min_age:
            query += " AND rp.age >= ?"
            params.append(min_age)
        if max_age:
            query += " AND rp.age <= ?"
            params.append(max_age)
        if nationality:
            query += " AND rp.nationality LIKE ?"
            params.append(f"%{nationality}%")
        if contract_type:
            query += " AND rp.contract_type LIKE ?"
            params.append(f"%{contract_type}%")
        if min_income:
            query += " AND rp.income >= ?"
            params.append(min_income)
        if max_income:
            query += " AND rp.income <= ?"
            params.append(max_income)
        if work_mode:
            query += " AND rp.work_mode LIKE ?"
            params.append(f"%{work_mode}%")

        # Filters for Rental Preferences
        if preferred_city:
            query += " AND rpfs.preferred_city LIKE ?"
            params.append(f"%{preferred_city}%")
        if preferred_area:
            query += " AND rpfs.preferred_area LIKE ?"
            params.append(f"%{preferred_area}%")
        if budget_min:
            query += " AND rpfs.budget_min >= ?"
            params.append(budget_min)
        if budget_max:
            query += " AND rpfs.budget_max <= ?"
            params.append(budget_max)
        if property_type and property_type != "Any":
            query += " AND rpfs.property_type = ?"
            params.append(property_type)
        if rooms_needed:
            query += " AND rpfs.rooms_needed >= ?"
            params.append(rooms_needed)
        if number_of_people:
            query += " AND rpfs.number_of_people >= ?"
            params.append(number_of_people)
        if move_in_date:
            query += " AND rpfs.move_in_date >= ?"
            params.append(move_in_date)
        if pets and pets != "Any":
            query += " AND rpfs.pets = ?"
            params.append(1 if pets == "Yes" else 0)
        if lease_duration and lease_duration != "Any":
            query += " AND rpfs.lease_duration = ?"
            params.append(lease_duration)

        # Filters for Credit Score
        if credit_score_status and credit_score_status != "Any":
            query += " AND rcs.status = ?"
            params.append(credit_score_status)

        # Execute the query
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        renters = cursor.fetchall()
        conn.close()

        # Display results
        # Display results
        if renters:
            st.write(f"Found {len(renters)} renter(s):")
            for renter in renters:
                st.write(f"Name: {renter['first_name']} {renter['surname']}")
                st.write(f"Credit Score Status: {renter['credit_score_status']}")
                
                with st.expander(f"View Profile: {renter['first_name']} {renter['surname']}"):
                    st.image(renter["profile_pic"], caption="Profile Picture", width=150)
                    st.markdown(
                        f"""
                        <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                            <h3 style="color: #2C3E50; margin-bottom: 15px;">{renter['first_name']} {renter['surname']}</h3>
                            <p><strong>Age:</strong> {renter['age']} years</p>
                            <p><strong>Nationality:</strong> {renter['nationality']}</p>
                            <p><strong>Contract Type:</strong> {renter['contract_type']}</p>
                            <p><strong>Income:</strong> €{renter['income']}</p>
                            <p><strong>Work Mode:</strong> {renter['work_mode']}</p>
                            <p><strong>Preferred City:</strong> {renter['preferred_city']}</p>
                            <p><strong>Preferred Area:</strong> {renter['preferred_area']}</p>
                            <p><strong>Budget Range:</strong> €{renter['budget_min']} - €{renter['budget_max']}</p>
                            <p><strong>Property Type:</strong> {renter['property_type']}</p>
                            <p><strong>Rooms Needed:</strong> {renter['rooms_needed']}</p>
                            <p><strong>Number of People:</strong> {renter['number_of_people']}</p>
                            <p><strong>Move-in Date:</strong> {renter['move_in_date']}</p>
                            <p><strong>Pets Allowed:</strong> {renter['pets']}</p>
                            <p><strong>Lease Duration:</strong> {renter['lease_duration']}</p>
                            <p><strong>Credit Score Status:</strong> {renter['credit_score_status']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                st.write("---")
        # if renters:
        #     st.write(f"Found {len(renters)} renter(s):")
        #     for renter in renters:
        #         st.write(f"Name: {renter['first_name']} {renter['surname']}")
        #         st.write(f"Age: {renter['age']}")
        #         st.write(f"Nationality: {renter['nationality']}")
        #         st.write(f"Credit Score Status: {renter['credit_score_status']}")
        #         st.write("---")
                
        #         with st.expander(f"View Profile: {renter['first_name']} {renter['surname']}"):
        #             st.markdown(
        #                 f"""
        #                 <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
        #                     <div style="text-align: center;">
        #                         <img src="{renter['profile_pic']}" alt="Profile Picture" style="border-radius: 50%; width: 150px; height: 150px; object-fit: cover; margin-bottom: 15px;">
        #                     </div>
        #                     <h3 style="text-align: center; margin-bottom: 20px;">{renter['first_name']} {renter['surname']}</h3>
        #                     <p><strong>Age:</strong> {renter['age']} years</p>
        #                     <p><strong>Nationality:</strong> {renter['nationality']}</p>
        #                     <p><strong>Contract Type:</strong> {renter['contract_type']}</p>
        #                     <p><strong>Income:</strong> €{renter['income']}</p>
        #                     <p><strong>Work Mode:</strong> {renter['work_mode']}</p>
        #                     <p><strong>Preferred City:</strong> {renter['preferred_city']}</p>
        #                     <p><strong>Preferred Area:</strong> {renter['preferred_area']}</p>
        #                     <p><strong>Budget Range:</strong> €{renter['budget_min']} - €{renter['budget_max']}</p>
        #                     <p><strong>Property Type:</strong> {renter['property_type']}</p>
        #                     <p><strong>Rooms Needed:</strong> {renter['rooms_needed']}</p>
        #                     <p><strong>Number of People:</strong> {renter['number_of_people']}</p>
        #                     <p><strong>Move-in Date:</strong> {renter['move_in_date']}</p>
        #                     <p><strong>Pets Allowed:</strong> {'Yes' if renter['pets'] else 'No'}</p>
        #                     <p><strong>Lease Duration:</strong> {renter['lease_duration']}</p>
        #                     <p><strong>Credit Score Status:</strong> {renter['credit_score_status']}</p>
        #                 </div>
        #                 """,
        #                 unsafe_allow_html=True
        #             )

                            
        else:
            st.warning("No renters found with the specified filters.")

if __name__ == "__main__":
    search_renters()



    #     # Display results
    #     if renters:
    #         st.write(f"Found {len(renters)} renter(s):")
    #         for renter in renters:
    #             st.write(f"Name: {renter['first_name']} {renter['surname']}")
    #             st.write(f"Age: {renter['age']}")
    #             st.write(f"Nationality: {renter['nationality']}")
    #             # Add button for full profile
    #             if st.button(f"View Full Profile ({renter['first_name']} {renter['surname']})", key=f"profile_{renter['id']}"):
    #                 st.session_state["renter_profile"] = dict(renter)  # Save renter's profile
    #                 st.session_state["current_page"] = "renters_profiles"  # Navigate to full profile page
    #                 st.rerun()  # Trigger navigation
    #             st.write("---")
    #     else:
    #         st.warning("No renters found with the specified filters.")

            
# if __name__ == "__main__":
#     search_renters()