import streamlit as st
import time

def post_listing():
    st.title("Post Your Lease")
    st.markdown("*Note: All fields marked with an asterisk (\*) are required.*")

    # Essential Information
    address = st.text_input("Street Address*")
    city = st.text_input("City*")
    state = st.selectbox("State*", options=["PA", "MA"])
    zip_code = st.text_input("Zip Code*")
    floor = st.number_input("Floor Number", min_value=0, max_value=100)
    unit = st.text_input("Unit Number or Letter*")
    beds = st.number_input("Number of Bedrooms*", min_value=0, max_value=10)
    baths = st.number_input("Number of Bathrooms*", min_value=0.0, max_value=10.0, step=0.5)

    # Specify rent per bedroom if there are multiple bedrooms
    rent_per_bedroom = {}
    if beds > 1:
        st.markdown("**Specify Rent Per Bedroom**")
        for i in range(1, int(beds) + 1):
            rent_per_bedroom[f"Bedroom {i}"] = st.number_input(
                f"Rent for Bedroom {i} ($)", min_value=0, step=1
            )

    available_from = st.date_input("Available From*")
    lease_length = st.number_input("Lease Length (Months)", min_value=1, max_value=24)
    type_of_lease = st.selectbox("Type of Lease*", options=["Sublet", "Full Lease"])
    contact_email = st.text_input("Your Email*", value=st.session_state.get('verified_email', ''))
    contact_phone = st.text_input("Your Phone Number (Optional)")

    # Amenities Information
    amenities = st.multiselect(
        "Select Amenities*",
        options=[
            "Air Conditioning",
            "Heat",
            "In-Unit Laundry",
            "Kitchen",
            "Dishwasher",
            "Furnished",
            "Parking",
            "Pet Friendly",
            "Gym Access",
        ],
    )

    # Photo Upload
    photos = st.file_uploader(
        "You can upload multiple photos (Optional, JPEG/PNG only).",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )

    additional_notes = st.text_area("Additional Notes (Optional)", height = 100)


    # Form Submission
    if st.button("Submit Listing"):
        if not address:
            st.error("Street Address is required.")
        elif not city:
            st.error("City is required.")
        elif not state:
            st.error("State is required.")
        elif not zip_code:
            st.error("Zip Code is required.")
        elif not unit:
            st.error("Unit Number or Letter is required.")
        elif beds == 0:
            st.error("Number of Bedrooms must be greater than 0.")
        elif baths == 0.0:
            st.error("Number of Bathrooms must be greater than 0.")
        elif not type_of_lease:
            st.error("Type of Lease is required.")
        elif not contact_email:
            st.error("Contact Email is required.")
        else:
            listing = {
                "Address": address,
                "City": city,
                "State": state,
                "Unit": unit,
                "Floor:": floor,
                "Zip Code": zip_code,
                "Bedrooms": beds,
                "Bathrooms": baths,
                "Rent Per Bedroom": rent_per_bedroom,
                "Available From": str(available_from),
                "Lease Length": lease_length,
                "Type of Lease": type_of_lease,
                "Contact Email": contact_email,
                "Contact Phone": contact_phone,
                "Amenities": amenities,
                "Photos": photos if photos else [],
                "Additional Notes": additional_notes,
            }
            if 'listings' not in st.session_state:
                st.session_state['listings'] = []
            st.session_state['listings'].append(listing)

            st.success("Listing posted successfully! Redirecting to My Listings...")
            st.session_state['current_page'] = "my_listings"
            time.sleep(2)
            st.rerun()