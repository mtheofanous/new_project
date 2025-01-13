import streamlit as st
from navigation_buttons import back_button
from queries.queries_favorites import *

# display the user's favorites

def display_favorites():
    """Display the user's favorite properties."""
    st.title("Favorites")
    back_button()

    user_id = st.session_state["user_id"]
    favorites = load_favorites(user_id)

    if not favorites:
        st.write("You have no favorites yet.")
    else:
        st.write("Your favorite properties:")
        for favorite in favorites:
            with st.container(border=True):
                st.write(f"- {favorite['favorite_type']} {favorite['favorite_id']}")
                
                
if __name__ == "__main__":
    display_favorites()