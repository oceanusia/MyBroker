import json
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    Text,
    exc,
    text
)
from sqlalchemy.sql import select

# --- Engine & Metadata ---
import streamlit as st
engine = create_engine(st.secrets["DATABASE_URL"])
meta = MetaData()

# --- Users Table ---
users = Table(
    "users", meta,
    Column("email", String, primary_key=True),
    Column("password", String, nullable=False),
    Column("saved_listings", Text, nullable=False, server_default=text('[]')),
)

# --- Listings Table ---
listings = Table(
    "listings", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("Address", String, nullable=False),
    Column("City", String),
    Column("State", String),
    Column("Zip Code", String),
    Column("Unit", String),
    Column("Floor", Integer),
    Column("Bedrooms", Integer),
    Column("Bathrooms", Float),
    Column("Rent Per Bedroom", Text),  # stored as JSON string
    Column("Available From", String),
    Column("Lease Length", Integer),
    Column("Type of Lease", String),
    Column("Contact Email", String),
    Column("Contact Phone", String),
    Column("Amenities", Text),         # stored as JSON list
    Column("Additional Notes", Text),  
    Column("Photos", Text),            # stored as JSON list
)

# Create tables if they don't exist
meta.create_all(engine)

# --- User Helper Functions ---
def create_user(email, password):
    """Insert a new user with an empty saved_listings list."""
    ins = users.insert().values(
        email=email,
        password=password,
        saved_listings=json.dumps([])
    )
    try:
        with engine.begin() as conn:
            conn.execute(ins)
    except exc.IntegrityError:
        raise ValueError(f"User with email '{email}' already exists.")


def get_user(email):
    """Fetch a user row as a dict, or None if not found."""
    sel = select(users).where(users.c.email == email)
    with engine.begin() as conn:
        row = conn.execute(sel).fetchone()
    if row:
        data = dict(row)
        data["saved_listings"] = json.loads(data.get("saved_listings") or "[]")
        return data
    return None


def authenticate_user(email, password):
    """Return True if the password matches for the given email."""
    user = get_user(email)
    return bool(user and user["password"] == password)


def save_listing_for_user(email, listing_id):
    """Append a listing ID to the user’s saved_listings."""
    user = get_user(email)
    if not user:
        return
    saved = user["saved_listings"]
    if listing_id not in saved:
        saved.append(listing_id)
        upd = users.update().where(users.c.email == email).values(
            saved_listings=json.dumps(saved)
        )
        with engine.begin() as conn:
            conn.execute(upd)


def unsave_listing_for_user(email, listing_id):
    """Remove a listing ID from the user’s saved_listings."""
    user = get_user(email)
    if not user:
        return
    saved = user["saved_listings"]
    if listing_id in saved:
        saved.remove(listing_id)
        upd = users.update().where(users.c.email == email).values(
            saved_listings=json.dumps(saved)
        )
        with engine.begin() as conn:
            conn.execute(upd)

# --- Listing Helper Functions ---
def create_listing(
    address, city, state, zip_code, floor, unit,
    bedrooms, bathrooms, rent_per_bedroom,
    available_from, lease_length, type_of_lease,
    contact_email, contact_phone,
    amenities, photos, additional_notes
):
    """Insert a new listing and return its new ID."""
    rent_json = json.dumps(rent_per_bedroom)
    amenities_json = json.dumps(amenities)
    photos_json = json.dumps(photos)

    values = {
        "Address": address,
        "City": city,
        "State": state,
        "Zip Code": zip_code,
        "Unit": unit,
        "Floor": floor,
        "Bedrooms": bedrooms,
        "Bathrooms": bathrooms,
        "Rent Per Bedroom": rent_json,
        "Available From": available_from,
        "Lease Length": lease_length,
        "Type of Lease": type_of_lease,
        "Contact Email": contact_email,
        "Contact Phone": contact_phone,
        "Amenities": amenities_json,
        "Additional Notes": additional_notes,
        "Photos": photos_json,
    }

    ins = listings.insert().values(**values)
    with engine.begin() as conn:
        result = conn.execute(ins)
        return result.inserted_primary_key[0]


def get_all_listings():
    """Fetch all listings as a list of dicts, parsing JSON fields."""
    sel = select(listings)
    with engine.begin() as conn:
        rows = conn.execute(sel).fetchall()
    results = []
    for row in rows:
        record = dict(row)
        record["Rent Per Bedroom"] = json.loads(record.get("Rent Per Bedroom") or "{}")
        record["Amenities"] = json.loads(record.get("Amenities") or "[]")
        record["Photos"] = json.loads(record.get("Photos") or "[]")
        results.append(record)
    return results


def remove_listing(listing_id):
    """Delete a listing by its ID."""
    deletion = listings.delete().where(listings.c.id == listing_id)
    with engine.begin() as conn:
        conn.execute(deletion)
