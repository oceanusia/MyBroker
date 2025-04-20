import streamlit as st
from db import get_all_listings, remove_listing


def my_listings():
    st.title("My Listings")
    st.markdown("Here are all the listings you have posted:")

    # Show a success message if a listing was just removed
    if 'removed_listing' in st.session_state:
        removed = st.session_state.pop('removed_listing')
        st.success(f"Listing for **{removed['Address']}** removed successfully!")

    # Fetch all listings from Supabase
    all_listings = get_all_listings()
    if not all_listings:
        st.info("You have not posted any listings yet.")
        return

    # Display each listing with a Remove button
    for listing in all_listings:
        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader(listing['Address'])
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

                # Display rent per bedroom if available
                if listing.get('Rent Per Bedroom'):
                    st.write("**Rent Per Bedroom:**")
                    for br, rent in listing['Rent Per Bedroom'].items():
                        st.write(f"- {br}: ${rent}")

                # Additional notes
                if listing.get('Additional Notes'):
                    st.write(f"**Additional Notes:** {listing['Additional Notes']}")

                # Photos
                if listing.get('Photos'):
                    st.write("**Photos:**")
                    for photo_url in listing['Photos']:
                        st.image(photo_url, use_container_width=True)
                else:
                    st.write("No photos uploaded.")

            with col2:
                if st.button(
                    "❌ Remove Listing",
                    key=f"remove_{listing['id']}"
                ):
                    remove_listing(listing['id'])
                    st.session_state['removed_listing'] = listing
                    st.success("Removing listing…")
                    st.rerun()

        st.markdown("---")
