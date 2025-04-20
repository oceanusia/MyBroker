import streamlit as st

def landing_page():
    # Landing Page with separate buttons for Verify Email and Login
    st.title("Welcome to MyBroker!")
    st.write("Please choose an option to proceed:")

    if st.button("Create an Account (New Users)"):
        st.session_state['current_page'] = "verify_email"
        st.rerun()

    if st.button("Login (Returning Users)"):
        st.session_state['current_page'] = "login"
        st.rerun()
