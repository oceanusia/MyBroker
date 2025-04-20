import streamlit as st
from supabase import create_client, Client

# Initialize the Supabase client
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# — User helpers —
def create_user(email: str, password: str):
    supabase.table("users").insert({
        "email": email,
        "password": password,
        "saved_listings": []
    }).execute()

def get_user(email: str):
    """
    Fetch a user row as a dict, or None if not found.
    Works with both ApiResponse.data and dict['data'] return types.
    """
    resp = (
        supabase
        .table("users")
        .select("*")
        .eq("email", email)
        .maybe_single()    # avoids error when 0 rows
        .execute()
    )
    # If resp is a dict (supabase-py v2+), pull 'data' key
    if isinstance(resp, dict):
        return resp.get("data")
    # Otherwise, assume it's an ApiResponse with a .data attribute
    return getattr(resp, "data", None)



def authenticate_user(email: str, password: str) -> bool:
    user = get_user(email)
    return bool(user and user["password"] == password)

def save_listing_for_user(email: str, listing_id: int):
    user = get_user(email)
    if user:
        lst = user["saved_listings"] or []
        if listing_id not in lst:
            lst.append(listing_id)
            supabase.table("users").update({"saved_listings": lst}).eq("email", email).execute()

def unsave_listing_for_user(email: str, listing_id: int):
    user = get_user(email)
    if user:
        lst = user["saved_listings"] or []
        if listing_id in lst:
            lst.remove(listing_id)
            supabase.table("users").update({"saved_listings": lst}).eq("email", email).execute()

# — Listing helpers —
def create_listing(**fields) -> int:
    resp = supabase.table("listings").insert(fields).execute()
    return resp.data[0]["id"]

def get_all_listings():
    resp = supabase.table("listings").select("*").execute()
    return resp.data  # list of dicts

def remove_listing(listing_id: int):
    supabase.table("listings").delete().eq("id", listing_id).execute()
