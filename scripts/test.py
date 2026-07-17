from app.services.database import get_session, User, Job
from app.services.notification_service import process_new_jobs_notifications

user_id = None
with get_session() as session:
    user = session.query(User).filter(User.email == "aniketkagsirvi@gmail.com").first()
    user_id = user.id

with get_session() as session:
    jobs = session.query(Job).order_by(Job.id.desc()).limit(20).all()
    new_ids = [j.id for j in jobs]

stats = process_new_jobs_notifications(new_ids)
print(f"Stats: {stats}")