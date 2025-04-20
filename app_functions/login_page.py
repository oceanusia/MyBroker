import streamlit as st
import time
from db import authenticate_user

# Login Function
def login():
    st.title("Login")
    
    # Input fields
    email = st.text_input("University Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    # Login button
    if st.button("Login"):
        # Authenticate against Supabase
        if authenticate_user(email, password):
            # Set logged-in state and store email
            st.session_state['logged_in'] = True
            st.session_state['verified_email'] = email

            # Loading spinner for UX
            with st.spinner("Logging In..."):
                time.sleep(2)

            # Navigate to the main listings page
            st.session_state['current_page'] = "browse_listings"
            st.rerun()
        else:
            st.error("Invalid email or password.")
