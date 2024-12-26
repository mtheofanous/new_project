import streamlit as st
from database import save_credit_score
from navigation_buttons import back_button 

def credit_score():
    
    back_button()
    # Initialize session state variables if they are not present
    if "authorized" not in st.session_state:
        st.session_state["authorized"] = None
    if "uploaded_file" not in st.session_state:
        st.session_state["uploaded_file"] = None
    if "status" not in st.session_state:
        st.session_state["status"] = "Not Verified"

    st.title("Credit Score Management")
    st.write("Manage your credit score effectively by following these steps:")

    st.markdown("""
        1. **Authorize Communication:** Grant us permission to communicate with [Teiresias.gr](https://www.teiresias.gr/) to retrieve your credit score.
        2. **Upload Credit Score:** Upload the retrieved credit score for verification.
        3. **Manage Your Credit Score:** Delete or update your uploaded credit score anytime.
        4. **Request New Credit Score:** Request a new credit score at any time (fees may apply).
    """)

    st.write("---")

    # Authorization Step
    if not st.session_state["authorized"] is None:
        authorized = st.checkbox("Do you authorize communication with Teiresias.gr to retrieve your credit score, and to share your credit score with relevant applications?",
                                  st.session_state.get('authorized', True), key="credit_score_authorization")

        if authorized == True:
            st.session_state["authorized"] = True
            st.success("Authorization granted. You can now upload your credit score.")
            
            st.write("### Upload Your Credit Score")
            uploaded_file = st.file_uploader("Upload your Credit Score (PDF format)", type=["pdf"])

            if uploaded_file:
                st.session_state["uploaded_file"] = uploaded_file
                st.session_state["status"] = "Pending"
                st.success("Credit score uploaded successfully.")

            st.markdown(f"**Status:** {st.session_state['status']}")

        else:
            st.warning("You must authorize communication to proceed.")


        st.write("### Manage Your Uploaded Credit Score")
        
        if st.session_state["status"] == "Verified" or "Pending":
            with st.expander("Delete Credit Score"):
                st.button("Delete Credit Score")
                if "Request New Credit Score":
                    st.warning("This action will request a new credit score. Are you sure? Please note that requesting a new credit score will incur a fee.")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Yes, Delete Credit Score"):
                            st.session_state["authorized"] = False
                            st.session_state["status"] = "Not Verified"
                            st.success("Credit score is deleted.")
                    with col2:
                        if st.button("No, Cancel Request"):
                            st.warning("Request cancelled.")
                            
    # Save credit score to database
    if st.button("Save"):
        if st.session_state["uploaded_file"]:
            # Assuming `st.session_state["user_id"]` is set elsewhere in your app
            if "user_id" in st.session_state:
                save_credit_score(st.session_state["user_id"], st.session_state["status"])
                st.success("Credit score saved successfully.")
                st.session_state["current_page"] = "dashboard"
            else:
                st.error("User ID not found. Please ensure you are logged in.")
        else:
            st.warning("No uploaded credit score file to save.")
   
    st.write("---")
    

    
if __name__ == "__main__":
    credit_score()