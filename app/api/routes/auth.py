import os

from fastapi import APIRouter, HTTPException,Query,Depends
from starlette.responses import RedirectResponse
from app.schemas.user_schema import UserCreateSchema, UserLoginSchema,UserResponseSchema

from app.services.database import create_user,get_user_by_email,save_verification_token,get_verification_token,verify_user,delete_verification_token
from app.auth.security import  create_access_token, verify_password,generate_verification_token
from app.auth.dependencies import get_current_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.services.email_service import send_verification_email



router = APIRouter()

@router.post("/signup", response_model=UserResponseSchema)
def signup(user_data: UserCreateSchema):
    created_user = create_user(user_data)
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
    password_valid = verify_password(form_data.password, user["hashed_password"])
    if not password_valid:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user["is_verified"]:
        raise HTTPException(status_code=403, detail="Email not verified.Please verify your email first.")
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
    
    # Redirect to frontend with success
    frontend_url = os.getenv("FRONTEND_URL", "http://127.0.0.1:5173")
    return RedirectResponse(
        url=f"{frontend_url}/verify-email?status=success"
    )

@router.get("/me")
def get_me( current_user = Depends(
        get_current_user
    )):
    return {"message": "protected route accessed", "user": current_user}


