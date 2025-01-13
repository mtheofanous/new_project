import streamlit as st
from navigation_buttons import home_button, back_button, log_out_button
from queries.user import save_user_to_db, load_user_from_db, update_email, update_username, update_user_password
from roles import assign_role_to_user, get_user_roles, remove_role_from_user
from app.components.utils import verify_password, hash_password, authenticate_user, update_user_password, delete_user_account

# Profile settings (roles, username, email, password)

def profile_settings():
    """User profile settings."""
    # Back to Home Button
    back_button()

    st.title("Profile Settings")

    # Load user data
    user_id = st.session_state["user_id"]
    user = load_user_from_db(user_id=user_id)

    # Display user profile settings
    st.markdown(f"**Username:** {user['username']}")
    st.markdown(f"**Email:** {user['email']}")

    # Display user roles
    roles = get_user_roles(user_id)
    st.markdown(f"**Roles:** {', '.join(roles)}")
    
    if "expander_open" not in st.session_state:
        st.session_state["expander_open"] = True

    # Change Username
    with st.expander("Change Username", expanded=st.session_state["expander_open"]):
        st.subheader("Change Username")
        new_username = st.text_input("New Username", key="new_username")

        if st.button("Change Username", key="change_username"):
            if not new_username.strip():
                st.error("Please enter a valid username.")
            else:
                try:
                    # Update username in the database
                    update_username(user_id, new_username)
                    st.session_state["username"] = new_username
                    st.success("Username updated successfully!")
                    
                    # close the expander
                    st.session_state["expander_open"] = False
                except ValueError as e:
                    st.error(f"Error: {e}")

                    

    # Change Email
    with st.expander("Change Email", expanded=st.session_state["expander_open"]):
        st.subheader("Change Email")
        new_email = st.text_input("New Email", key="new_email")

        if st.button("Change Email", key="change_email"):
            if not new_email.strip():
                st.error("Please enter a valid email.")
            else:
                try:
                    # Update email in the database
                    update_email(user_id, new_email)
                    st.session_state["email"] = new_email
                    st.success("Email updated successfully!")
                    
                    # close the expander
                    st.session_state["expander_open"] = False
                    
                except ValueError as e:
                    st.error(f"Error: {e}")

    # Change Password
    with st.expander("Change Password", expanded=st.session_state["expander_open"]):
        st.subheader("Change Password")
        current_password = st.text_input("Current Password", type="password", key="current_password")
        new_password = st.text_input("New Password", type="password", key="new_password")
        confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_password")

        if st.button("Change Password", key="change_password"):
            if not current_password or not new_password or not confirm_password:
                st.error("Please fill in all password fields.")
            elif not verify_password(current_password, user["password_hash"]):
                st.error("Incorrect current password!")
            elif new_password != confirm_password:
                st.error("New password and confirm password do not match!")
            else:
                try:
                    new_password_hash = update_user_password(user_id, new_password)
                    
                    user["password_hash"] = new_password_hash
                    
                    st.success("Password updated successfully!")
                    
                    # close the expander
                    st.session_state["expander_open"] = False
                    
                except ValueError as e:
                    st.error(f"Error: {e}")

    # Add Role
    with st.expander("Add Role", expanded=st.session_state["expander_open"]):
        st.subheader("Add Role")
        # new role options are based on the current roles of the user (to avoid duplicates) 
        new_role_options = ["Renter", "Landlord", "Agent"]
        # new_role_options = [role for role in new_role_options if role not in roles]
        new_role = st.selectbox("Select New Role", new_role_options, key="new_role")

        if st.button("Add Role", key="add_role"):
            if not new_role:
                st.error("Please select a valid role.")
            elif new_role in roles:
                st.error(f"Role {new_role} already assigned to your account.")
            else:
                assign_role_to_user(user_id, new_role)
                st.session_state["role"] = new_role
                st.success(f"Role {new_role} added successfully!")
                
                # close the expander
                st.session_state["expander_open"] = False
                
                # st.rerun()
        
        # Remove Role
    with st.expander("Remove Role", expanded=st.session_state["expander_open"]):
        # load the session state roles
        st.subheader("Remove Role")
        
        # if the user has multiple roles, they can remove one of them, otherwise, the remove role option is disabled
        if len(roles) > 1:
            role_to_remove = st.selectbox("Select a role to remove", roles)
            if st.button("Remove Role"):
                if not role_to_remove:
                    st.error("Please select a valid role.")
                else:
                    remove_role_from_user(user_id, role_to_remove)
                    st.session_state["role"] = role_to_remove
                    st.success(f"Role {role_to_remove} removed successfully!")
                    
                    # close the expander
                    st.session_state["expander_open"] = False
                    # st.rerun()
        else:
            st.info("You must have at least one role assigned to your account.")
            
        
    with st.expander("Delete Account"):
    # Delete Account
        st.subheader("Delete Account")
        delete_account = st.checkbox("I want to delete my account", key="delete_account")

        if delete_account:
            if st.button("Delete Account", key="confirm_delete_account"):
                delete_user_account(user_id)
                st.success("Account deleted successfully!")
                st.session_state["logged_in"] = False
                st.session_state["user_id"] = None
                st.session_state["user"] = None
                st.session_state["role"] = None
                st.session_state["email"] = None
                st.session_state["current_page"] = "landing"
            
if __name__ == "__main__":
    profile_settings()