import streamlit as st
from database import load_user_from_db, load_agent_profile_from_db
# agent_summary_profile
def agent_summary_profile():
    
    if "agent_profile" not in st.session_state:
        st.session_state["current_page"] = "create_agent_profile"
        
    else:
    
        agent_profile = st.session_state.get("agent_profile")
        
        agent_profile_pic = agent_profile["agent_profile_pic"]
        
        # Profile Summary
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if agent_profile_pic:
                st.image(agent_profile_pic, width=200)
            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("👁️", key="view_full_profile_button"):
                    st.session_state["current_page"] = "agent_full_profile"
            with c2:
                if st.button("✏️", key="edit_profile_button"):
                    st.session_state["current_page"] = "edit_agent_profile"
        with col2:
            st.write(f"**Name:** {agent_profile['name']}")
            st.write(f"**Agency Name:** {agent_profile['agency_name']}")
            st.write(f"**Mission:** {agent_profile['mission_statement']}")
            st.write(f"**Services Offered:** {agent_profile['services']}")

    