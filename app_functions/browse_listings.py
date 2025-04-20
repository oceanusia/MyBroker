import streamlit as st
from db import get_user, get_all_listings, save_listing_for_user, unsave_listing_for_user


def browse_listings():
    st.title("Available Listings")

    # Ensure user is logged in
    email = st.session_state.get("verified_email")
    if not email:
        st.error("No user logged in.")
        return

    # Fetch all listings from Supabase
    listings = get_all_listings()
    if not listings:
        st.info("No listings yet!")
        return

    # Fetch the user's saved listing IDs
    user = get_user(email)
    saved_ids = user.get("saved_listings", [])

    # Display each listing
    for listing in listings:
        listing_id = listing.get("id")
        with st.expander(f"{listing['Address']}"):
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
            st.write(
                f"**Amenities:** {', '.join(listing['Amenities']) if listing['Amenities'] else 'None'}"
            )

            # Rent per bedroom
            if listing.get('Rent Per Bedroom'):
                st.write("**Rent Per Bedroom:**")
                for bedroom, rent in listing['Rent Per Bedroom'].items():
                    st.write(f"- {bedroom}: ${rent}")

            # Photos
            if listing.get('Photos'):
                st.write("**Photos:**")
                for photo_url in listing['Photos']:
                    st.image(photo_url, use_container_width=True)
            else:
                st.write("No photos uploaded.")

            # Save / Unsave button
            if listing_id in saved_ids:
                if st.button("💔 Unsave Listing", key=f"unsave_{listing_id}"):
                    unsave_listing_for_user(email, listing_id)
                    st.success("Listing removed from Saved!")
                    st.rerun()
            else:
                if st.button("💾 Save Listing", key=f"save_{listing_id}"):
                    save_listing_for_user(email, listing_id)
                    st.success("Listing added to Saved!")
                    st.rerun()
