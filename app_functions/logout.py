import streamlit as st

def logout():
    """Logout the user and return to the landing page."""
    st.session_state['logged_in'] = False
    st.session_state['current_page'] = "landing_page"
    st.rerun()
