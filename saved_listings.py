import streamlit as st
import time

def saved_listings():
    st.title("Saved Listings")

    email = st.session_state['verified_email']  # Get the logged-in user's email
    user_saved_listings = st.session_state['users'][email].get('saved_listings', [])
    listings = st.session_state['listings']

    if not user_saved_listings:
        st.info("You have no saved listings yet!")
    else:
        # Filter listings based on saved identifiers
        saved_listings = [listing for listing in listings if listing['Address'] in user_saved_listings]

        if not saved_listings:
            st.info("You have no saved listings yet!")
        else:
            for i, listing in enumerate(saved_listings := [l for l in listings if l['Address'] in user_saved_listings]):
                with st.expander(f"{listing['Address']}"):
                    st.write(f"**City:** {listing['City']}")
                    st.write(f"**State:** {listing['State']}")
                    st.write(f"**Zip Code:** {listing['Zip Code']}")
                    st.write(f"**Unit:** {listing['Unit']}")
                    st.write(f"**Floor:** {listing['Floor:']}")
                    st.write(f"**Bedrooms:** {listing['Bedrooms']}")
                    st.write(f"**Bathrooms:** {listing['Bathrooms']}")
                    st.write(f"**Available From:** {listing['Available From']}")
                    st.write(f"**Lease Length:** {listing['Lease Length']} months")
                    st.write(f"**Type of Lease:** {listing['Type of Lease']}")
                    st.write(f"**Contact Email:** {listing['Contact Email']}")
                    st.write(f"**Contact Phone:** {listing['Contact Phone']}")
                    st.write(f"**Amenities:** {', '.join(listing['Amenities']) if listing['Amenities'] else 'None'}")

                    # Display rent per bedroom if available
                    if listing['Rent Per Bedroom']:
                        st.write("**Rent Per Bedroom:**")
                        for bedroom, rent in listing['Rent Per Bedroom'].items():
                            st.write(f"- {bedroom}: ${rent}")

                    # Display uploaded photos if available
                    if listing['Photos']:
                        st.write("**Photos:**")
                        for photo in listing['Photos']:
                            st.image(photo, use_container_width=True)
                    else:
                        st.write("No photos uploaded.")

                    # Unsave Button
                    if st.button("💔 Unsave Listing", key=f"unsave_saved_{i}"):
                    # Removes this listing from the user’s Saved Listings
                        user_saved_listings.remove(listing['Address'])
                        st.session_state['users'][email]['saved_listings'] = user_saved_listings
                        st.success("Listing removed from Saved!")
                        time.sleep(1)
                        st.rerun()