import streamlit as st

def my_listings():
    st.title("My Listings")
    st.markdown("Here are all the listings you have posted:")

    # Display the removed listing message if available
    if 'removed_listing' in st.session_state:
        removed = st.session_state.pop('removed_listing')  # Remove it after displaying
        st.success(f"Listing for **{removed['Address']}** removed successfully!")

    # Check if there are any listings
    if 'listings' in st.session_state and st.session_state['listings']:
        for i, listing in enumerate(st.session_state['listings'], start=1):
            # Create a container for each listing
            with st.container():
                # Use columns for layout
                col1, col2 = st.columns([3, 1])

                # Left column: Listing details
                with col1:
                    st.subheader(listing['Address'])
                    st.write(f"**City:** {listing['City']}")
                    st.write(f"**State:** {listing['State']}")
                    st.write(f"**Zip Code:** {listing['Zip Code']}")
                    st.write(f"**Bedrooms:** {listing['Bedrooms']}")
                    st.write(f"**Bathrooms:** {listing['Bathrooms']}")
                    st.write(f"**Type of Lease:** {listing['Type of Lease']}")
                    st.write(f"**Available From:** {listing['Available From']}")
                    st.write(f"**Lease Length:** {listing['Lease Length']} months")
                    st.write(f"**Type of Lease:** {listing['Type of Lease']}")
                    st.write(f"**Contact Email:** {listing['Contact Email']}")
                    st.write(f"**Amenities:** {', '.join(listing['Amenities']) if listing['Amenities'] else 'None'}")
                    st.write(f"**Additional Notes:** {listing['Additional Notes'] if listing['Additional Notes'] else 'None'}")

                # Right column: Remove button
                with col2:
                    if st.button(f"❌ Remove Listing for {listing['Address']}", key=f"remove_{i}"):
                        # Remove the listing from the user's listings
                        removed_listing = st.session_state['listings'].pop(i - 1)

                        # Remove the listing from the general Browse Listings
                        if 'browse_listings' in st.session_state:
                            st.session_state['browse_listings'] = [
                                l for l in st.session_state['browse_listings'] if l != removed_listing
                            ]

                        # Remove the listing from any user's Saved Listings
                        if 'saved_listings' in st.session_state:
                            st.session_state['saved_listings'] = [
                                l for l in st.session_state['saved_listings'] if l != removed_listing
                            ]

                        # Store the removed listing temporarily in session state
                        st.session_state['removed_listing'] = removed_listing

                        # Trigger a rerun to refresh the page
                        st.rerun()

                st.markdown("---")
    else:
        st.info("You have not posted any listings yet.")
