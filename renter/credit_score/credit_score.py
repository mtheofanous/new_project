import streamlit as st
from database import save_credit_score
from navigation_buttons import back_button 

import streamlit as st
from database import save_credit_score, delete_credit_score, load_credit_scores

def credit_score():
    back_button()
    """Manage credit score workflow"""

    # load the current user's credit score
    credit_score = load_credit_scores(user_id=st.session_state["user_id"])
    # Initialize session state variables
    if credit_score:
        st.session_state.setdefault("authorized", credit_score["authorized"])
        st.session_state.setdefault("uploaded_file", credit_score["uploaded_file"])
        st.session_state.setdefault("status", credit_score["status"])
    else:
        st.session_state.setdefault("authorized", False)
        st.session_state.setdefault("uploaded_file", None)
        st.session_state.setdefault("status", "Not Verified")

    st.title("Credit Score Management")
    st.write("Manage your credit score effectively by following these steps:")

    st.markdown("""
        1. **Authorize Communication:** Grant us permission to communicate with [Teiresias.gr](https://www.teiresias.gr/) to retrieve your credit score.
        2. **Upload Credit Score:** Upload the retrieved credit score for verification.
        3. **Manage Your Credit Score:** Delete or update your uploaded credit score anytime.
        4. **Request New Credit Score:** Request a new credit score at any time (fees may apply).
    """)

    st.write("---")

    # Show the authorization checkbox only if no file has been uploaded
    if not st.session_state["uploaded_file"]:
        authorized_option = st.checkbox(
            "Do you authorize communication with Teiresias.gr to retrieve your credit score and share it with relevant applications?",
            value=st.session_state["authorized"],
        )

        if authorized_option:
            st.session_state["authorized"] = True
            st.success("Authorization granted. You can now upload your credit score.")
        else:
            st.session_state["authorized"] = False
            st.warning("You must authorize communication to proceed.")

    # Allow File Upload if Authorized
    if st.session_state["authorized"] and not st.session_state["uploaded_file"] and st.session_state["status"] == "Not Verified":
        st.write("### Upload Your Credit Score")
        uploaded_file = st.file_uploader("Upload your Credit Score (PDF format)", type=["pdf"])

        if uploaded_file:
            st.session_state["uploaded_file"] = uploaded_file
            st.session_state["status"] = "Pending"
            st.success("Credit score uploaded successfully.")

        st.markdown(f"**Status:** {st.session_state['status']}")

        if st.session_state["uploaded_file"]:
            with st.expander("Manage Your Uploaded Credit Score"):
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Delete Credit Score"):
                        delete_credit_score()
                        st.session_state["uploaded_file"] = None
                        st.session_state["status"] = "Not Verified"
                        st.warning("Credit score deleted successfully.")
                        st.rerun()
    else:
        st.header("Manage Your Credit Score")
        st.write(f"### Credit Status: {st.session_state['status']}")
        with st.expander("Manage Your Uploaded Credit Score"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Delete Credit Score"):
                    delete_credit_score()
                    st.session_state["uploaded_file"] = None
                    st.session_state["status"] = "Not Verified"
                    st.warning("Credit score deleted successfully.")
                    st.rerun()
 


    # Save credit score to database
    if st.button("Save"):
        if st.session_state["uploaded_file"]:
            if "user_id" in st.session_state:
                save_credit_score(
                    user_id=st.session_state["user_id"],
                    status=st.session_state["status"],
                    authorized=st.session_state["authorized"],
                    uploaded_file=bool(st.session_state["uploaded_file"])
                )
                st.success("Credit score saved successfully.")
                st.session_state["current_page"] = "dashboard"
            else:
                st.error("User ID not found. Please ensure you are logged in.")
        else:
            st.warning("No uploaded credit score file to save.")
            st.session_state["current_page"] = "dashboard"

    st.write("---")

if __name__ == "__main__":
    credit_score()

