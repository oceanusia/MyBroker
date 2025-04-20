import streamlit as st
import db

# Importing Page Functions
from app_functions.verify_email import verify_email
from app_functions.create_account import create_account
from app_functions.login_page import login
from app_functions.post_listing import post_listing
from app_functions.browse_listings import browse_listings
from app_functions.saved_listings import saved_listings
from app_functions.my_listings import my_listings
from app_functions.landing_page import landing_page
from app_functions.logout import logout

# Layout Configuration
st.set_page_config(layout="wide", page_title="MyBroker", page_icon="🏠")

# Site Banner
st.markdown(
    """
    <style>
    .banner {
        background: linear-gradient(90deg, #6a5acd, #483d8b); /* Gradient from purple to dark grey-purple */
        padding: 15px;
        color: white;
        font-size: 28px;
        font-weight: bold;
        border-radius: 8px; /* Rounded corners */
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3); /* Subtle shadow for depth */
        margin-bottom: 20px;
        text-align: left; /* Align text to the left */
    }
    .headline {
        font-size: 16px; /* Smaller font size for the headline */
        font-weight: normal; /* Normal font weight for the headline */
        margin-top: 5px; /* Add spacing between title and headline */
    }
    </style>
    <div class="banner">
        <div>MyBroker</div>
        <div class="headline">Connecting you with housing in your university community</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# Setting Up Initial Parameters and Simple In-Memory Database
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "landing_page"

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'users' not in st.session_state:
    st.session_state['users'] = {}

if 'listings' not in st.session_state:
    st.session_state['listings'] = []

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
    "my_listings": my_listings,
}


# Centralized Navigation Function
def navigate_to(page_name):
    st.session_state['current_page'] = page_name
    st.rerun()


# Main App Logic

# Directs to landing page if user is not logged in
if not st.session_state['logged_in']:
    current_page = st.session_state['current_page']
    if current_page in PAGE_REGISTRY:
        PAGE_REGISTRY[current_page]()
    else:
        # Default to landing page
        navigate_to("landing_page")

else:
    # Directs to Main Page if user is logged in
    # Sidebar Menu with Text Buttons for Navigation
    st.sidebar.title("My Menu")
    if st.sidebar.button("Browse Listings"):
        navigate_to("browse_listings")

    if st.sidebar.button("Post a Listing"):
        navigate_to("post_listing")

    if st.sidebar.button("My Listings"):
        navigate_to("my_listings")

    if st.sidebar.button("Saved Listings"):
        navigate_to("saved_listings")

    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        navigate_to("landing_page")

    # Render the selected page
    current_page = st.session_state['current_page']
    if current_page in PAGE_REGISTRY:
        PAGE_REGISTRY[current_page]()








