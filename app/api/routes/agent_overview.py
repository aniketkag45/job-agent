from fastapi import APIRouter, Depends
from app.services.database import get_agent_overview
from app.schemas.response_schema import ApiResponse

router = APIRouter()

@router.get("/agent/overview", response_model=ApiResponse)
def agent_overview():
    
    overview = get_agent_overview()

    return ApiResponse(
        success=True,
        data=overview,
        message="Agent overview fetched successfully"
    )