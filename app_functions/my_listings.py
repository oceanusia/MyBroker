import streamlit as st
from db import get_all_listings, remove_listing

def my_listings():
    st.title("My Listings")
    st.markdown("Here are all the listings you have posted:")

    # Display a “removed” message if we just deleted one
    if 'removed_listing' in st.session_state:
        removed = st.session_state.pop('removed_listing')  # Remove it after displaying
        st.success(f"Listing for **{removed['Address']}** removed successfully!")

    # Pull your listings straight from the database
    all_listings = get_all_listings()
    if not all_listings:
        st.info("You have not posted any listings yet.")
        return

    for listing in all_listings:
        # Use the unique listing['id'] as your key
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(listing['Address'])
                # … all your st.write(...) calls, just swap from listing['Field'] …
            with col2:
                if st.button(
                    f"❌ Remove Listing",
                    key=f"remove_{listing['id']}"
                ):
                    # delete in DB
                    remove_listing(listing['id'])
                    # store the address so we can show the success toast
                    st.session_state['removed_listing'] = listing
                    st.success("Removing listing…")
                    st.rerun()
        st.markdown("---")
