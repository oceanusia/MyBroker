import streamlit as st
import time
from db import get_user, create_user

def create_account():
    st.title("Create Your Account")

    # Make sure we have an email from the verification step
    email = st.session_state.get("verified_email")
    if not email:
        st.error("No email found—please verify your email first.")
        return

    st.write(f"Your Email/Username: {email}")
    password = st.text_input("Create Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        # 1) Check passwords match
        if password != confirm_password:
            st.error("Passwords do not match.")
        # 2) Check for an existing user
        elif get_user(email) is not None:
            st.error("An account with this email already exists.")
        else:
            # 3) Create the user in Supabase
            try:
                create_user(email, password)
                st.success("Account created successfully! You can now log in.")
                time.sleep(1)
                st.session_state["current_page"] = "login"
                st.rerun()
            except Exception as e:
                st.error(f"Error creating account: {e}")
