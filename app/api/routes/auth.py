import os
import httpx
from fastapi import APIRouter, HTTPException, Query, Depends
from starlette.responses import RedirectResponse
from pydantic import BaseModel

from app.schemas.user_schema import UserCreateSchema, UserResponseSchema
from app.services.database import (
    create_user,
    get_user_by_email,
    save_verification_token,
    get_verification_token,
    verify_user,
    delete_verification_token,
)
from app.auth.security import create_access_token, verify_password, generate_verification_token
from app.auth.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from app.services.email_service import send_verification_email
from app.services.google_auth_service import verify_google_id_token, get_or_create_google_user_payload


router = APIRouter()

@router.post("/signup", response_model=UserResponseSchema)
def signup(user_data: UserCreateSchema):
    created_user = create_user(user_data)
    if not created_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    verification_token = generate_verification_token()
    save_verification_token(created_user["id"], verification_token)
    base_url = os.getenv("APP_BASE_URL", "http://127.0.0.1:8000")
    verification_link = f"{base_url}/verify-email?token={verification_token}"
    email_sent = send_verification_email(created_user["email"], verification_link)
    if email_sent:
        print(f"Verification email sent to {created_user['email']}")
    else:
        print(f"Failed to send verification email to {created_user['email']}")
    return created_user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    # Google-only users have no password
    if not user.get("hashed_password"):
        raise HTTPException(status_code=401, detail="This account uses Google login. Please continue with Google.")
    password_valid = verify_password(form_data.password, user["hashed_password"])
    if not password_valid:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user["is_verified"]:
        raise HTTPException(status_code=403, detail="Email not verified. Please verify your email first.")
    access_token = create_access_token({"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify-email")
def verify_email(token: str = Query(...)):
    token_data = get_verification_token(token)
    if not token_data:
        frontend_url = os.getenv("FRONTEND_URL", "http://127.0.0.1:5173")
        return RedirectResponse(
            url=f"{frontend_url}/verify-email?status=error&message=invalid_token"
        )
    verify_user(token_data["user_id"])
    delete_verification_token(token)
    frontend_url = os.getenv("FRONTEND_URL", "http://127.0.0.1:5173")
    return RedirectResponse(
        url=f"{frontend_url}/verify-email?status=success"
    )

@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    return {"message": "protected route accessed", "user": current_user}


# ===== GOOGLE OAUTH =====

class GoogleAuthRequest(BaseModel):
    id_token: str

@router.post("/auth/google")
def google_auth(payload: GoogleAuthRequest):
    """Production flow: Frontend sends Google id_token, we verify and return our JWT."""
    id_info = verify_google_id_token(payload.id_token)
    if not id_info:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    # Optional: ensure email_verified
    # if not id_info.get("email_verified"):
    #     raise HTTPException(status_code=401, detail="Google email not verified")

    user = get_or_create_google_user_payload(id_info)
    if not user:
        raise HTTPException(status_code=400, detail="Failed to create or fetch user")

    access_token = create_access_token({"sub": user["email"]})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }

@router.get("/auth/google/login")
def google_login():
    """Redirect flow entry — redirects user to Google consent screen."""
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://127.0.0.1:8000/auth/google/callback")
    
    if not client_id or "your-google" in client_id:
        raise HTTPException(status_code=500, detail="GOOGLE_CLIENT_ID not configured in .env")

    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return RedirectResponse(url=google_auth_url)

@router.get("/auth/google/callback")
def google_callback(code: str = Query(...)):
    """Google redirects here with ?code=... We exchange code for tokens."""
    frontend_url = os.getenv("FRONTEND_URL", "http://127.0.0.1:5173")
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://127.0.0.1:8000/auth/google/callback")

    if not client_id or not client_secret:
        return RedirectResponse(url=f"{frontend_url}/login?error=google_not_configured")

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    }

    try:
        resp = httpx.post(token_url, data=data, timeout=15)
        resp.raise_for_status()
        token_data = resp.json()
        id_token_str = token_data.get("id_token")

        if not id_token_str:
            print(f"Google token response missing id_token: {token_data}")
            return RedirectResponse(url=f"{frontend_url}/login?error=google_no_id_token")

        id_info = verify_google_id_token(id_token_str)
        if not id_info:
            return RedirectResponse(url=f"{frontend_url}/login?error=google_invalid_token")

        user = get_or_create_google_user_payload(id_info)
        if not user:
            return RedirectResponse(url=f"{frontend_url}/login?error=google_user_failed")

        access_token = create_access_token({"sub": user["email"]})
        # Redirect to frontend callback page with our JWT
        return RedirectResponse(url=f"{frontend_url}/auth/google/callback?token={access_token}")

    except Exception as e:
        print(f"Google callback error: {e}")
        return RedirectResponse(url=f"{frontend_url}/login?error=google_callback_failed")