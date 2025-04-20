import streamlit as st

def browse_listings():
    st.title("Available Listings")

    listings = st.session_state['listings']
    email = st.session_state['verified_email']  # Get the logged-in user's email
    
    # Initalize user's Saved Listings list
    user_data = st.session_state['users'][email]
    if 'saved_listings' not in user_data:
        user_data['saved_listings'] = []
    user_saved_listings = user_data['saved_listings']

    if not listings:
        st.info("No listings yet!")
    else:
        # Display each listing as a panel
        for i, listing in enumerate(listings):
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
                        st.image(photo, use_container_width = True)
                else:
                    st.write("No photos uploaded.")

            # Add a Save / Unsave button by Address instead of index
                addr = listing['Address']
                if addr in user_saved_listings:
                    if st.button("💔 Unsave Listing", key=f"unsave_{i}"):
                        user_saved_listings.remove(addr)
                        st.success("Listing removed from Saved!")
                else:
                    if st.button("💾 Save Listing", key=f"save_{i}"):
                        user_saved_listings.append(addr)
                        st.success("Listing added to Saved!")

                # Persist back to session_state
                st.session_state['users'][email]['saved_listings'] = user_saved_listings