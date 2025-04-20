import streamlit as st
import time

# Login Function
def login():
    st.title("Login")
    email = st.text_input("University Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = st.session_state['users'].get(email)
        if user and user["password"] == password:
            st.session_state['logged_in'] = True
            
            # Show a loading spinner and pause for 2 seconds
            with st.spinner("Logging In..."):
                time.sleep(2)

            st.session_state['current_page'] = "browse_listings"
            st.rerun()

        else:
            st.error("Invalid email or password.")