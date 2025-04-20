import streamlit as st
from db import get_user, get_all_listings, unsave_listing_for_user


def saved_listings():
    st.title("Saved Listings")

    # Ensure a user is logged in
    email = st.session_state.get('verified_email')
    if not email:
        st.error("No user logged in.")
        return

    # Fetch user data and all listings
    user = get_user(email)
    saved_ids = user.get('saved_listings', [])
    all_listings = get_all_listings()

    # Handle no saved listings
    if not saved_ids:
        st.info("You have no saved listings yet!")
        return

    # Filter listings by saved IDs
    saved = [l for l in all_listings if l['id'] in saved_ids]
    if not saved:
        st.info("You have no saved listings yet!")
        return

    # Display each saved listing
    for listing in saved:
        with st.expander(listing['Address']):
            st.write(f"**City:** {listing['City']}")
            st.write(f"**State:** {listing['State']}")
            st.write(f"**Zip Code:** {listing['Zip Code']}")
            st.write(f"**Unit:** {listing['Unit']}")
            st.write(f"**Floor:** {listing['Floor']}")
            st.write(f"**Bedrooms:** {listing['Bedrooms']}")
            st.write(f"**Bathrooms:** {listing['Bathrooms']}")
            st.write(f"**Available From:** {listing['Available From']}")
            st.write(f"**Lease Length:** {listing['Lease Length']} months")
            st.write(f"**Type of Lease:** {listing['Type of Lease']}")
            st.write(f"**Contact Email:** {listing['Contact Email']}")
            st.write(f"**Contact Phone:** {listing['Contact Phone']}")
            st.write(f"**Amenities:** {', '.join(listing['Amenities']) if listing['Amenities'] else 'None'}")

            # Rent per bedroom
            if listing['Rent Per Bedroom']:
                st.write("**Rent Per Bedroom:**")
                for bdrm, rent in listing['Rent Per Bedroom'].items():
                    st.write(f"- {bdrm}: ${rent}")

            # Photos
            if listing['Photos']:
                st.write("**Photos:**")
                for photo_url in listing['Photos']:
                    st.image(photo_url, use_container_width=True)
            else:
                st.write("No photos uploaded.")

            # Unsave button
            if st.button("💔 Unsave Listing", key=f"unsave_{listing['id']}"):
                unsave_listing_for_user(email, listing['id'])
                st.success("Listing removed! Click to refresh.")
                st.rerun()
