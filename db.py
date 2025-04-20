# db.py
import json
from sqlalchemy import (
    create_engine, MetaData,
    Table, Column, Integer, String, Text
)
from sqlalchemy.sql import select

# 1) Engine & metadata
#    This will create a file called mybroker.db next to this script.
engine = create_engine(
    "sqlite:///mybroker.db",
    connect_args={"check_same_thread": False}
)
meta = MetaData()

# 2) Users table
users = Table(
    "users", meta,
    Column("email", String, primary_key=True),
    Column("password", String, nullable=False),
    # we’ll store the list of saved listing IDs as a JSON string
    Column("saved_listings", Text, nullable=False, default="[]"),
)

# 3) (Later) you can add a listings table here in the same pattern…

# 4) Create the file & tables on first import
meta.create_all(engine)

# — Helper functions —

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
    """Fetch a user row, or None if not found."""
    sel = select(users).where(users.c.email == email)
    with engine.begin() as conn:
        row = conn.execute(sel).fetchone()
    if row:
        data = dict(row)
        data["saved_listings"] = json.loads(data["saved_listings"])
        return data
    return None

def authenticate_user(email, password):
    """Return True if the password matches."""
    user = get_user(email)
    return user is not None and user["password"] == password

def save_listing_for_user(email, listing_id):
    """Append a listing ID to that user’s saved_listings."""
    user = get_user(email)
    saved = user["saved_listings"]
    if listing_id not in saved:
        saved.append(listing_id)
        upd = (
            users.update()
                 .where(users.c.email == email)
                 .values(saved_listings=json.dumps(saved))
        )
        with engine.begin() as conn:
            conn.execute(upd)

def unsave_listing_for_user(email, listing_id):
    user = get_user(email)
    saved = user["saved_listings"]
    if listing_id in saved:
        saved.remove(listing_id)
        upd = (
            users.update()
                 .where(users.c.email == email)
                 .values(saved_listings=json.dumps(saved))
        )
        with engine.begin() as conn:
            conn.execute(upd)
