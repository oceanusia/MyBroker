import streamlit as st

# Import all your page functions
from app_functions.landing_page    import landing_page
from app_functions.verify_email    import verify_email
from app_functions.create_account  import create_account
from app_functions.login_page      import login
from app_functions.post_listing    import post_listing
from app_functions.browse_listings import browse_listings
from app_functions.saved_listings  import saved_listings
from app_functions.my_listings     import my_listings
from app_functions.logout          import logout

# Page Registry
PAGE_REGISTRY = {
    "landing_page":    landing_page,
    "verify_email":    verify_email,
    "create_account":  create_account,
    "login":           login,
    "post_listing":    post_listing,
    "browse_listings": browse_listings,
    "saved_listings":  saved_listings,
    "my_listings":     my_listings,
    "logout":          logout,
}

def navigate_to(page_name):
    """Set the current page and force a rerun."""
    st.session_state['current_page'] = page_name
    st.rerun()
