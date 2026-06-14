import json
from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.services.database import get_or_create_user_profile,update_profile
from app.schemas.profile_schema import ProfileUpdateSchema, ProfileResponseSchema
from app.schemas.response_schema import ApiResponse

router = APIRouter()

@router.get("/profile", response_model=ApiResponse)
def get_profile(current_user :dict = Depends(get_current_user)):
    from app.services.database import get_session,User
    email = current_user.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user.id
    profile = get_or_create_user_profile(user_id)
    return ApiResponse(success=True, data=profile, message="Profile retrieved successfully")

@router.put("/profile", response_model=ApiResponse)
def update_my_profile(profile_data: ProfileUpdateSchema, current_user :dict = Depends(get_current_user)):
    from app.services.database import get_session,User
    email = current_user.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user.id
    update_dict = profile_data.model_dump(exclude_unset=True)
    if not update_dict:
        raise HTTPException(status_code=400, detail="No data provided for update")
    updated_profile = update_profile(user_id, update_dict)
    if not updated_profile:
        raise HTTPException(status_code=500, detail="Profile update failed")
    return ApiResponse(success=True, data=updated_profile, message="Profile updated successfully")