"""
Notification Service — Broad Engineering Feed: Every new engineering job
notified, resume matches on top priority (your ask)
"""

import logging
from datetime import datetime
from typing import List, Dict, Any
from app.services.database import get_session, UserProfile, UserNotification
from app.services.candidate_retrieval_service import get_all_new_jobs_scored
from app.notifier.telegram_notifier import send_job_alert, send_telegram_message

logger = logging.getLogger(__name__)

def _exists(user_id: int, job_id: int, notif_type: str) -> bool:
    with get_session() as session:
        return session.query(UserNotification).filter(
            UserNotification.user_id == user_id,
            UserNotification.job_id == job_id,
            UserNotification.notification_type == notif_type
        ).first() is not None

def create_notification(user_id: int, job_id: int, notif_type: str = "in_app", title: str = "", message: str = "", hybrid_score: float = 0.0, channel_status: str = "pending") -> bool:
    if _exists(user_id, job_id, notif_type):
        return False
    try:
        hybrid_score = float(hybrid_score) if hybrid_score is not None else 0.0
    except Exception:
        hybrid_score = 0.0
    try:
        with get_session() as session:
            notif = UserNotification(
                user_id=user_id,
                job_id=job_id,
                notification_type=notif_type,
                title=title[:500] if title else "",
                message=message,
                hybrid_score=hybrid_score,
                is_read=False,
                channel_status=channel_status,
                created_at=datetime.now().isoformat(),
                sent_at=datetime.now().isoformat() if channel_status == "sent" else None
            )
            session.add(notif)
        return True
    except Exception as e:
        logger.error(f"Create notif failed {user_id} {job_id}: {e}")
        return False

def mark_sent(user_id: int, job_id: int):
    try:
        with get_session() as session:
            notif = session.query(UserNotification).filter(
                UserNotification.user_id == user_id,
                UserNotification.job_id == job_id,
                UserNotification.notification_type == "telegram"
            ).first()
            if notif:
                notif.channel_status = "sent"
                notif.sent_at = datetime.now().isoformat()
    except Exception:
        pass

def process_new_jobs_notifications(new_job_ids: List[int]) -> Dict[str, Any]:
    """
    Broad: For every new engineering job batch, notify each user about ALL new jobs,
    but highlight resume matches on top.
    """
    stats = {"users_processed": 0, "in_app_created": 0, "telegram_sent": 0, "new_job_count": len(new_job_ids)}
    if not new_job_ids:
        return stats

    with get_session() as session:
        profiles = session.query(UserProfile).all()
        cache = {p.user_id: {"chat_id": p.telegram_chat_id, "enabled": bool(p.telegram_enabled), "threshold": float(p.notification_threshold or 0.6)} for p in profiles}

    if not cache:
        return stats

    for user_id, prof in cache.items():
        try:
            all_scored = get_all_new_jobs_scored(user_id, new_job_ids)
            if not all_scored:
                continue

            high_priority = [j for j in all_scored if float(j["hybrid_score"]) >= float(prof["threshold"])]
            stats["users_processed"] += 1

            for job in all_scored:
                if create_notification(user_id, job["id"], "in_app", job["title"], f"New engineering job: {job['title']} at {job['company']} - match {float(job['hybrid_score'])*100:.0f}%", float(job["hybrid_score"]), "sent"):
                    stats["in_app_created"] += 1
                if prof["enabled"] and prof["chat_id"]:
                    create_notification(user_id, job["id"], "telegram", job["title"], f"Telegram: {job['title']}", float(job["hybrid_score"]), "pending")

            if prof["enabled"] and prof["chat_id"]:
                chat_id = prof["chat_id"]
                total_new = len(all_scored)
                high_count = len(high_priority)

                if high_count > 0:
                    summary = f"<b>{total_new} New Engineering Jobs</b>\n\n"
                    summary += f"<b>{high_count} highly match your resume</b> (priority on top)\n"
                    summary += f"Total to explore: {total_new}\n\nTop matches:\n"
                    for i, job in enumerate(high_priority[:3], 1):
                        summary += f"{i}. <b>{job['title']}</b> at {job['company']} - {float(job['hybrid_score'])*100:.0f}%\n"
                    summary += f"\n<i>All {total_new} jobs are engineering background. Check dashboard.</i>"
                    if send_telegram_message(summary, chat_id=chat_id):
                        stats["telegram_sent"] += 1
                    for job in high_priority[:2]:
                        if send_job_alert(job, chat_id=chat_id):
                            stats["telegram_sent"] += 1
                            mark_sent(user_id, job["id"])
                else:
                    summary = f"<b>{total_new} New Engineering Jobs</b>\n\nNo high resume match this batch, but all are engineering to explore.\n\nCheck Jobs page - all sorted with your resume priority.\n"
                    if send_telegram_message(summary, chat_id=chat_id):
                        stats["telegram_sent"] += 1

        except Exception as e:
            logger.error(f"Notify failed user {user_id}: {e}")
            continue

    logger.info(f"Broad notification stats: {stats}")
    return stats