import streamlit as st

def home_button():
    if st.button("Home", key="home_button"):
        st.session_state["current_page"] = "landing"
        st.rerun()

def log_out_button():
    if st.button("Log Out", key="logout_button"):
        st.session_state.clear()
        st.session_state["current_page"] = "landing"
        st.success("You have been logged out.")
        st.rerun()

def back_button():
    if st.button("Back", key="back_button"):
        st.session_state["current_page"] = st.session_state.get("previous_page", "dashboard")
        st.rerun()
