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
    from db import create_listing
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
            # → INSERT into the database instead of session_state
            listing_id = create_listing(
                address=address,
                city=city,
                state=state,
                zip_code=zip_code,
                floor=floor,
                unit=unit,
                bedrooms=beds,
                bathrooms=baths,
                rent_per_bedroom=rent_per_bedroom,
                available_from=str(available_from),
                lease_length=lease_length,
                type_of_lease=type_of_lease,
                contact_email=contact_email,
                contact_phone=contact_phone,
                amenities=amenities,
                photos=[file.name for file in photos] if photos else [],
                additional_notes=additional_notes
            )
            st.success("Listing posted successfully! Redirecting to My Listings…")
            st.session_state['current_page'] = "my_listings"
            time.sleep(2)
            st.rerun()
