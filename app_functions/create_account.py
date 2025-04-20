import streamlit as st
import time

# Create Account Function
def create_account():
    st.title("Create Your Account")
    email = st.session_state.get('verified_email')
    st.write(f"Your Email/Username: {email}")
    password = st.text_input("Create Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if password != confirm_password:
            st.error("Passwords do not match.")
        elif email in st.session_state['users']:
            st.error("An account with this email already exists.")
        else:
            # Save the user (password should be hashed in a real implementation)
            st.session_state['users'][email] = {"password": password, "saved_listings": []}
            st.success("Account created successfully! You can now log in.")
            time.sleep(1)
            st.session_state['current_page'] = "login"  # Navigate to login page
            st.rerun()
