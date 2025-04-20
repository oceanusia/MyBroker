import streamlit as st
from db import get_user, get_all_listings, unsave_listing_for_user


def saved_listings():
    st.title("Saved Listings")

    # Ensure a user is logged in
    email = st.session_state.get("verified_email")
    if not email:
        st.error("No user logged in.")
        return

    # Fetch user data and saved listing IDs
    user = get_user(email)
    saved_ids = user.get("saved_listings", [])

    # Fetch all listings and filter by saved IDs
    all_listings = get_all_listings()
    saved = [l for l in all_listings if l.get("id") in saved_ids]

    # Handle no saved listings
    if not saved:
        st.info("You have no saved listings yet!")
        return

    # Display each saved listing
    for listing in saved:
        listing_id = listing.get("id")
        with st.expander(listing.get("Address", "")):
            st.write(f"**City:** {listing.get('City', '')}")
            st.write(f"**State:** {listing.get('State', '')}")
            st.write(f"**Zip Code:** {listing.get('Zip Code', '')}")
            st.write(f"**Unit:** {listing.get('Unit', '')}")
            st.write(f"**Floor:** {listing.get('Floor', '')}")
            st.write(f"**Bedrooms:** {listing.get('Bedrooms', '')}")
            st.write(f"**Bathrooms:** {listing.get('Bathrooms', '')}")
            st.write(f"**Available From:** {listing.get('Available From', '')}")
            st.write(f"**Lease Length:** {listing.get('Lease Length', '')} months")
            st.write(f"**Type of Lease:** {listing.get('Type of Lease', '')}")
            st.write(f"**Contact Email:** {listing.get('Contact Email', '')}")
            st.write(f"**Contact Phone:** {listing.get('Contact Phone', '')}")
            amenities = listing.get('Amenities', []) or []
            st.write(f"**Amenities:** {', '.join(amenities) if amenities else 'None'}")

            # Rent per bedroom
            rent_info = listing.get('Rent Per Bedroom', {}) or {}
            if rent_info:
                st.write("**Rent Per Bedroom:**")
                for bdrm, rent in rent_info.items():
                    st.write(f"- {bdrm}: ${rent}")

            # Additional notes
            notes = listing.get('Additional Notes')
            if notes:
                st.write(f"**Additional Notes:** {notes}")

            # Photos
            photos = listing.get('Photos', []) or []
            if photos:
                st.write("**Photos:**")
                for photo_url in photos:
                    st.image(photo_url, use_container_width=True)
            else:
                st.write("No photos uploaded.")

            # Unsave button
            if st.button("💔 Unsave Listing", key=f"unsave_{listing_id}"):
                unsave_listing_for_user(email, listing_id)
                st.success("Listing removed! Refresh to see changes.")
