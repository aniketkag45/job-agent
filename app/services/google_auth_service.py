import os
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
def verify_google_id_token(id_token_str: str) -> Optional[dict]:
    """
    Verify the Google ID token and return the payload if valid.
    """
    if not GOOGLE_CLIENT_ID:
        raise ValueError("GOOGLE_CLIENT_ID is not set in the environment variables.")
    
    from google.oauth2 import id_token
    from google.auth.transport import requests as google_requests

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        id_info = id_token.verify_oauth2_token(id_token_str, google_requests.Request(), GOOGLE_CLIENT_ID)

        # ID token is valid. Return the payload.
        return id_info
    except ValueError as e:
        # Invalid token
        print(f"Invalid Google ID token: {e}")
        return None

def get_or_create_google_user_payload(id_info: dict) -> Optional[dict]:
    from app.services.database import (
        get_user_by_google_id,
        get_user_by_email,
        create_google_user,
        link_google_to_existing_user,
    )
    google_id = id_info.get("sub")
    email = id_info.get("email")
    name = id_info.get("name") or email.split("@")[0]
    avatar_url = id_info.get("picture")
    if not google_id or not email:
        print("Google ID or email is missing in the token payload.")
        return None
    existing_by_google = get_user_by_google_id(google_id)
    if existing_by_google:
        return existing_by_google
    existing_by_email = get_user_by_email(email)
    if existing_by_email:
        print(f"Found existing user by email {email}, linking Google account...")
        linked = link_google_to_existing_user(existing_by_email["id"], google_id, avatar_url)
        return linked
    print(f"Creating new Google user for email {email}...")
    new_user = create_google_user(google_id = google_id, email = email, name = name, avatar_url = avatar_url)
    return new_user
