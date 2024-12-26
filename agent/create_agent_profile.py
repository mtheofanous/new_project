import streamlit as st
from navigation_buttons import home_button 

def create_agent_profile():
    
    home_button()
    
    st.title("Create Rental Agent Profile")

    # Collect agent's profile information
    with st.expander("Add Profile Information"):
        # Personal details
        name = st.text_input("Enter agent's full name:")
        phone = st.text_input("Enter agent's phone number:")
        profile_pic = st.text_input("Enter path or URL to agent's profile photo:")
        license_number = st.text_input("Enter agent's license number:")
        agency_name = st.text_input("Enter agency name:")
        agency_website = st.text_input("Enter agency website:")
        working_days = st.multiselect("Select working days:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        working_hours = st.slider("Select working hours:", 0, 24, (9, 17), format="%d:00")
        preferred_communication = st.multiselect("Select preferred communication methods:", ["Phone", "Email", "Text", "In-person"])

    with st.expander("Portfolio Information"):
        # Portfolio details
        service_area = st.text_area("Enter service areas (comma-separated):").split(',')
        neighborhood_specialties = st.text_area("Enter neighborhood specialties (comma-separated):").split(',')
        current_listings = st.text_area("Enter URLs for current rental listings (comma-separated):").split(',')

    with st.expander("Add Professional Information"):
        # Professional details
        experience_years = st.number_input("Enter years of experience in rental properties:", min_value=0, step=1)
        services_offered = {
            "tenant_matching": st.checkbox("Offer tenant matching?"),
            "landlord_support": st.checkbox("Offer landlord support?"),
            "lease_management": st.checkbox("Offer lease management?"),
            "market_analysis": st.checkbox("Offer market analysis?")
        }
        languages = st.text_area("Enter languages spoken (comma-separated):").split(',')
        specializations = st.text_area("Enter specializations (comma-separated):").split(',')
        certifications = st.text_area("Enter certifications (comma-separated):").split(',')
        negotiation_skills = st.text_input("Enter negotiation skills level (e.g., Expert, Intermediate):")
        advertising_strategies = st.text_area("Enter advertising strategies (comma-separated):").split(',')
        professional_network = st.text_area("Enter professional network connections (comma-separated):").split(',')
        tech_skills = st.text_area("Enter tech skills (comma-separated):").split(',')
        
    with st.expander("Additional Information"):

        # Additional information
        achievements = st.text_area("Enter achievements (comma-separated):").split(',')
        mission_statement = st.text_area("Enter mission statement:")
        hobbies = st.text_area("Enter hobbies/interests (comma-separated):").split(',')

    if st.button("Save Profile"):
        # Build the profile dictionary
        agent_profile = {
            "name": name,
            "phone": phone,
            "profile_pic": profile_pic,
            "license_number": license_number,
            "agency_name": agency_name,
            "agency_website": agency_website,
            "working_days": working_days,
            "working_hours": working_hours,
            "preferred_communication": preferred_communication
            
            }
        agent_skills = {
            "experience_years": experience_years,
            "services_offered": services_offered,
            "specializations": specializations,
            "certifications": certifications,
            "languages": languages,
            "advertising_strategies": advertising_strategies,
            "professional_network": professional_network,
            "negotiation_skills": negotiation_skills,
            "tech_skills": tech_skills
            },
        agent_portfolio = {
                "service_area": service_area,
                "neighborhood_specialties": neighborhood_specialties,
                "current_listings": current_listings,
            },

        additional_info = {
                "achievements": achievements,
                "mission_statement": mission_statement,
                "hobbies": hobbies
            }
        # Save agent profile to database
        # save_agent_profile_to_db(agent_profile, agent_skills, agent_portfolio, additional_info)
        


if __name__ == "__main__":
    create_agent_profile()
