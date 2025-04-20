import json
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    Text
)
from sqlalchemy.sql import select

# --- Engine & Metadata ---
engine = create_engine(
    "sqlite:///mybroker.db",
    connect_args={"check_same_thread": False}
)
meta = MetaData()

# --- Users Table ---
users = Table(
    "users", meta,
    Column("email", String, primary_key=True),
    Column("password", String, nullable=False),
    Column("saved_listings", Text, nullable=False, default="[]"),
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
    with engine.begin() as conn:
        conn.execute(ins)


def get_user(email):
    """Fetch a user row as a dict, or None if not found."""
    sel = select(users).where(users.c.email == email)
    with engine.begin() as conn:
        row = conn.execute(sel).fetchone()
    if row:
        data = dict(row)
        data["saved_listings"] = json.loads(data["saved_listings"])
        return data
    return None


def authenticate_user(email, password):
    """Return True if the password matches for the given email."""
    user = get_user(email)
    return user is not None and user["password"] == password


def save_listing_for_user(email, listing_id):
    """Append a listing ID to the user’s saved_listings."""
    user = get_user(email)
    if user is None:
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
    if user is None:
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
def get_all_listings():
    """Fetch all listings as a list of dicts, parsing JSON fields."""
    sel = select(listings)
    with engine.begin() as conn:
        rows = conn.execute(sel).fetchall()
    results = []
    for row in rows:
        record = dict(row)
        # Parse JSON fields
        record["Rent Per Bedroom"] = json.loads(record.get("Rent Per Bedroom") or "{}")
        record["Amenities"] = json.loads(record.get("Amenities") or "[]")
        record["Photos"]    = json.loads(record.get("Photos") or "[]")
        # Additional Notes is plain text
        results.append(record)
    return results


def remove_listing(listing_id):
    """Delete a listing by its ID."""
    deletion = listings.delete().where(listings.c.id == listing_id)
    with engine.begin() as conn:
        conn.execute(deletion)
