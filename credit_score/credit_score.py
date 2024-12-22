import streamlit as st

# Income and Credit Score

def income_credit_score():
    # Check if the credit score is already verified
    if st.session_state.get("credit_score_verified", False):
        edit_confirmation = st.radio(
            "Your credit score is already verified. Are you sure you want to edit it?",
            options=["No", "Yes"],
            index=0,
            key="edit_credit_score_confirmation"
        )
        if edit_confirmation == "No":
            st.info("Credit score verification remains unchanged.")
            return

    # Credit score verification and upload process
    credit_score_verified = st.checkbox(
        "I authorize credit score verification.",
        value=st.session_state.get("credit_score_verified", False),
        key="new_profile_credit_score_auth"
    )

    uploaded_credit_score = None
    if credit_score_verified:
        st.info("Please upload a credit score document.")
        uploaded_credit_score = st.file_uploader(
            "Upload your credit score (PDF/Image)", 
            type=["pdf", "jpg", "png"], 
            key="new_profile_credit_score_file"
        )
        if uploaded_credit_score:
            st.success("Credit score uploaded successfully!")
            st.markdown("✅ Credit score verified")
        else:
            st.markdown("❌ Credit score not uploaded")
    
    # Update session state
    st.session_state["credit_score_verified"] = credit_score_verified
    st.session_state["uploaded_credit_score"] = uploaded_credit_score
