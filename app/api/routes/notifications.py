from fastapi import APIRouter, Depends, Query, HTTPException
from datetime import datetime
from app.auth.dependencies import get_current_user
from app.services.database import get_session, User, UserNotification, Job, _job_to_dict
from app.schemas.response_schema import ApiResponse

router = APIRouter()

@router.get("/notifications", response_model=ApiResponse)
def get_my_notifications(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    unread_only: bool = Query(default=False),
    current_user: dict = Depends(get_current_user)
):
    email = current_user.get("sub")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        query = session.query(UserNotification).filter(UserNotification.user_id == user.id)

        if unread_only:
            query = query.filter(UserNotification.is_read == False)

        total = query.count()
        offset = (page-1)*page_size
        notifs = query.order_by(UserNotification.created_at.desc()).offset(offset).limit(page_size).all()

        result = []
        for n in notifs:
            job = session.query(Job).filter(Job.id == n.job_id).first()
            job_dict = _job_to_dict(job) if job else None
            result.append({
                "id": n.id,
                "user_id": n.user_id,
                "job_id": n.job_id,
                "notification_type": n.notification_type,
                "title": n.title,
                "message": n.message,
                "hybrid_score": n.hybrid_score,
                "is_read": n.is_read,
                "channel_status": n.channel_status,
                "created_at": n.created_at,
                "job": job_dict
            })

        return ApiResponse(success=True, data={"notifications": result, "total": total, "page": page, "page_size": page_size}, message=f"Found {len(result)} notifications")

@router.get("/notifications/unread-count", response_model=ApiResponse)
def get_unread_count(current_user: dict = Depends(get_current_user)):
    email = current_user.get("sub")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        count = session.query(UserNotification).filter(
            UserNotification.user_id == user.id,
            UserNotification.is_read == False,
            UserNotification.notification_type == "in_app"
        ).count()
        return ApiResponse(success=True, data={"unread_count": count}, message="Unread count")

@router.put("/notifications/{notif_id}/read", response_model=ApiResponse)
def mark_as_read(notif_id: int, current_user: dict = Depends(get_current_user)):
    email = current_user.get("sub")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        notif = session.query(UserNotification).filter(UserNotification.id == notif_id, UserNotification.user_id == user.id).first()
        if not notif:
            raise HTTPException(status_code=404, detail="Notification not found")
        notif.is_read = True
        return ApiResponse(success=True, message="Marked as read")

@router.put("/notifications/read-all", response_model=ApiResponse)
def mark_all_read(current_user: dict = Depends(get_current_user)):
    email = current_user.get("sub")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        session.query(UserNotification).filter(UserNotification.user_id == user.id, UserNotification.is_read == False).update({"is_read": True})
        return ApiResponse(success=True, message="All marked as read")

@router.delete("/notifications/{notif_id}", response_model=ApiResponse)
def delete_notification(notif_id: int, current_user: dict = Depends(get_current_user)):
    email = current_user.get("sub")
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        deleted = session.query(UserNotification).filter(UserNotification.id == notif_id, UserNotification.user_id == user.id).delete()
        if deleted == 0:
            raise HTTPException(status_code=404, detail="Not found")
        return ApiResponse(success=True, message="Deleted")