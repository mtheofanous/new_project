import streamlit as st
from queries.user import load_user_from_db
from queries.agent import load_agent_profile_from_db

# agent_summary_profile
def agent_summary_profile():
    
    
    if "agent_profile" not in st.session_state:
        st.session_state["current_page"] = "create_agent_profile"
        st.error("Please create your agent profile.")
        st.rerun()
        
    else:
    
        user_id = st.session_state.get("user_id", None)
        
        user = load_user_from_db(user_id)
        
        agent_profile = load_agent_profile_from_db(user_id)
        
        agent_profile_pic = agent_profile["agent_profile_pic"]
        
        # Profile Summary
        col1, col2 = st.columns([1, 4])
        
        with col1:
            with st.container(border=True):
                if agent_profile_pic:
                    st.image(agent_profile_pic, width=100)
            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("👁️", key="view_full_profile_button"):
                    st.session_state["current_page"] = "agent_full_profile"
            with c2:
                if st.button("✏️", key="edit_profile_button"):
                    st.session_state["current_page"] = "edit_agent_profile"
        with col2:
            st.write(f"**First Name:** {user['first_name']}")
            st.write(f"**Last Name:** {user['last_name']}")
            st.write(f"**Agency Name:** {agent_profile['agency_name']}")
            st.write(f"**Mission:** {agent_profile['mission_statement']}")
            st.write(f"**Services Offered:** {agent_profile['services']}")

if __name__ == "__main__":
    agent_summary_profile()
    