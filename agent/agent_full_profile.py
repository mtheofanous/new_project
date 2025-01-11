import streamlit as st
from navigation_buttons import back_button

def agent_full_profile():
    
    back_button()
    
    agent_profile = st.session_state["agent_profile"]
    
    st.title("Agent Profile")
    
    st.markdown("---")
    
    # Profile Columns
    col1, col2 = st.columns(2)
    
    with col1:
        if agent_profile["agent_profile_pic"]:
            st.image(agent_profile["agent_profile_pic"], width=200)
        st.markdown(f"##### **First Name:** {agent_profile['first_name']}")
        st.markdown(f"##### **Last Name:** {agent_profile['last_name']}")
        st.markdown(f"##### **Phone:** {agent_profile['phone']}")
        st.markdown(f"##### **Agency Name:** {agent_profile['agency_name']}")
        st.markdown(f"##### **Agency Address:** {agent_profile['agency_address']}")
        st.markdown(f"##### **Agency Website:** {agent_profile['agency_website']}")
        st.markdown(f"##### **Social Media:** {agent_profile['social_media']}")
        
    with col2:
        # Work Details
        st.subheader("Work Details")
        st.markdown(f"##### **Working Days:** {agent_profile['working_days']}")
        st.markdown(f"##### **Working Hours:** {agent_profile['working_hours']}")
        st.markdown(f"##### **Preferred Communication:** {agent_profile['preferred_communication']}")
        
        # Professional Background
        st.subheader("Professional Background")
        st.markdown(f"##### **Services Offered:** {agent_profile['services']}")
        st.markdown(f"##### **Languages Spoken:** {agent_profile['languages']}")
        
        # Additional Information
        st.subheader("Additional Information")
        st.markdown(f"##### **Mission Statement:** {agent_profile['mission_statement']}")
        
    st.markdown("---")
    
    # Edit Profile Button
    if st.button("Edit Profile"):
        st.session_state["current_page"] = "edit_agent_profile"
        
if __name__ == "__main__":
    agent_full_profile()