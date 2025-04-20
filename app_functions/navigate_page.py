import streamlit as st

# Page Registry
PAGE_REGISTRY = {
    "landing_page": landing_page,
    "verify_email": verify_email,
    "create_account": create_account,
    "login": login,
    "post_listing": post_listing,
    "browse_listings": browse_listings,
    "saved_listings": saved_listings,
    "logout": logout,
}


# Centralized Navigation Function
def navigate_to(page_name):
    st.session_state['current_page'] = page_name
    st.rerun()
