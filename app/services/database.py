import os
import logging
from datetime import datetime
from typing import List, Optional,Dict, Any
from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text,ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from app.auth.security import hash_password
from app.services.pipeline_metrics import increment_metric
from app.services.semantic_representation import (
    build_semantic_representation
)

load_dotenv()
logger = logging.getLogger(__name__)


DATABASE_URl = os.getenv("DATABASE_URL", "postgresql://jobagent:jobagent123@localhost:5432/jobagent")

engine = create_engine(DATABASE_URl,pool_size = 10, pool_pre_ping = True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        session.close()

class User(Base):
     """
    Users table — login, registration, verification.
    
    Columns:
        id: Auto-incrementing primary key
        username: Display name
        email: Unique — used for login
        hashed_password: bcrypt hash, never store plain text
        is_verified: Has the user verified their email?
        created_at: ISO format timestamp
    """
     __tablename__ = "users"
     id = Column(Integer, primary_key=True, autoincrement=True)
     username = Column(String(100), nullable=False)
     email = Column(String(255), unique=True, nullable=False)
     hashed_password = Column(String(255), nullable=True)
     is_verified = Column(Boolean, default=False)
     google_id = Column(String(255), unique=True, nullable=True)  # NEW
     auth_provider = Column(String(50), default="local")  # NEW: local or google
     avatar_url = Column(String(500), nullable=True)  # NEW
     created_at = Column(String(50), default=lambda: datetime.now().isoformat())

class VerificationToken(Base):
    """
    Stores email verification tokens.
    
    When a user signs up, we generate a random token and store it here.
    When they click the verification link, we look up the token,
    mark the user as verified, and delete the token.
    
    A user can have only one active token at a time because
    new signups create new tokens.
    """
    __tablename__ = "verification_tokens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    created_at = Column(String(50), default=lambda: datetime.now().isoformat())

class Job(Base):
    """
    Scraped jobs table — the core data.
    
    Columns:
        id: Auto-increment
        title, company, location: Self-explanatory
        apply_link: UNIQUE — how we deduplicate
        source: Where it came from (RemoteOK, Greenhouse)
        score: Keyword-based relevance score
        is_notified: Has a Telegram alert been sent?
        semantic_text: Natural language description for embedding
    """
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    company = Column(String(300), nullable=False)
    location = Column(String(500))
    apply_link = Column(String(1000), unique=True, nullable=False)
    source = Column(String(100))
    score = Column(Integer,default=0)
    is_notified = Column(Boolean, default=False)
    scraped_at = Column(String(50)) 
    applied_at = Column(String(50)) 
    semantic_text = Column(Text)

class PipelineRun(Base):
     """
    Pipeline execution history — for the agent overview dashboard.
    
    Every time the scraper pipeline runs, we record what happened:
    how many jobs fetched, inserted, filtered, etc.
    This powers the stats cards on the dashboard.
    """
     __tablename__ = "pipeline_runs"
     id = Column(Integer, primary_key=True, autoincrement=True)
     run_started_at = Column(String(50))
     run_completed_at = Column(String(50))
     jobs_fetched = Column(Integer,default=0)
     jobs_inserted = Column(Integer,default=0)
     jobs_filtered = Column(Integer,default=0)
     duplicates_skipped = Column(Integer,default=0)
     scraper_failures = Column(Integer,default=0)
     alerts_sent = Column(Integer,default=0)
     status = Column(String(50))  # SUCCESS, PARTIAL_FAILURE, FAILURE
     error_message = Column(Text)
     execution_time_seconds = Column(Integer)

class UserProfile(Base):
     """
    User profile — NEW table for the profile page.
    
    Stores personal information, preferences, education.
    One profile per user (user_id is UNIQUE).
    
    JSON fields: education, preferred_keywords, excluded_keywords,
    preferred_locations are stored as JSON strings in PostgreSQL.
    """
     __tablename__ = "user_profiles"
     id = Column(Integer, primary_key=True, autoincrement=True)
     user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
     full_name = Column(String(200))
     headline = Column(String(300))
     bio = Column(Text)
     education_degree = Column(String(200))
     education_field = Column(String(200))
     education_school = Column(String(300))
     education_year = Column(String(10))
     profile_photo_url = Column(String(500))
     mobile = Column(String(30))
     location = Column(String(200))
     education = Column(Text)           # JSON string
     linkedin_url = Column(String(500))
     github_url = Column(String(500))
     portfolio_url = Column(String(500))
     preferred_keywords = Column(Text)  # JSON string: ["python", "backend"]
     excluded_keywords = Column(Text)   # JSON string: ["senior", "manager"]
     preferred_locations = Column(Text) # JSON string: ["India", "Remote"]
     remote_only = Column(Boolean, default=False)
     updated_at = Column(String(50))

class UserResume(Base):
    """
    User resumes — NEW table for multiple resume support.
    
    Each user can upload multiple resumes. One is marked as
    'is_active' — that's the one used for job matching.
    
    We store:
        - filename: original file name
        - skills, domains: extracted by the AI parser
        - semantic_text: for embedding
        - The actual embedding is in ChromaDB (not here — too large)
    """
    __tablename__ = "user_resumes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(500))
    skills = Column(Text)          # JSON string: ["python", "sql"]
    domains = Column(Text)         # JSON string: ["finance", "healthcare"]
    experience_level = Column(String(50))
    semantic_text = Column(Text)   # For embedding
    is_active = Column(Boolean, default=True)
    uploaded_at = Column(String(50),default=lambda: datetime.now().isoformat())

class UserApplication(Base):
    """
    Tracks which jobs a user has applied to.

    One row per application. Linked to user and job.
    """
    __tablename__ = "user_applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    applied_at = Column(String(50), default=lambda: datetime.now().isoformat())
    source = Column(String(50), default="manual")  # manual or auto


def init_db():
     """
    Create all tables if they don't exist.
    
    Call this once at application startup.
    Safe to call multiple times — uses CREATE TABLE IF NOT EXISTS.
    
    Usage:
        from app.services.database import init_db
        init_db()
    """
     Base.metadata.create_all(bind=engine)
     logger.info("All database tables verified/created.")

        
def insert_job(job):
    from sqlalchemy.exc import IntegrityError
    from app.services.embedding_service import generate_embedding

    semantic_text = build_semantic_representation(job)

    session = SessionLocal()
    try:
        new_job = Job(
            title = job.get('title'),
            company = job.get('company'),
            location = job.get('location'),
            apply_link = job.get('apply_link'),
            source = job.get('source'),
            score = job.get('score'),
            semantic_text = semantic_text,
            scraped_at=datetime.now().isoformat(),
        )
        session.add(new_job)
        session.flush()
        job_id = new_job.id
        session.commit()
        print(f"Inserted job: {job.get('title')} (ID: {job_id})")
        try:
            from app.services.vector_store import store_job_embedding
            embedding = generate_embedding(semantic_text)
            store_job_embedding(
                job_id = job_id,
                embedding = embedding,
                metadata = {
                    "title": job.get("title"),
                    "company": job.get("company"),
                    "location": job.get("location"),
                    "apply_link": job.get("apply_link"),
                    "source": job.get("source"),
                    "score": job.get("score"),
                    "searchable_text": " ".join([
                        job.get("title", ""),
                        job.get("description", ""),
                        " ".join(job.get("tech_stack", []))
                    ])
                }
            )
        except Exception as e:
            print(f"Error storing embedding for job ID {job_id}: {e}")
        session.commit()
        return job_id
    except IntegrityError:
        session.rollback()
        increment_metric("duplicates_skipped")
        return None
    except Exception:
        session.rollback()
    finally:
        session.close()


# def fetch_jobs(limit = 10):
#     connection = get_connection()
#     cursor = connection.cursor()
#     cursor.execute('''
#         SELECT title, company, location, apply_link, source, score
#         FROM jobs
#         ORDER BY score DESC
#         LIMIT ?
#     ''', (limit,))
#     rows = cursor.fetchall()
#     connection.close()
#     jobs = []
#     for row in rows:
#         jobs.append({
#             "title": row[0],
#             "company": row[1],
#             "location": row[2],
#             "apply_link": row[3],
#             "source": row[4],
#             "score": row[5]
#         })

#     return jobs
            

def fetch_unnotified_jobs():
    with get_session() as session:
        jobs = session.query(Job).filter(Job.is_notified == False).all()
        return [
            {
                "id":j.id,
                "title": j.title,
                "company": j.company,
                "location": j.location,
                "apply_link": j.apply_link,
                "source": j.source,
                "score": j.score,
                "is_notified": j.is_notified
            }
            for j in jobs
        ]

def mark_job_as_notified(job_id):
    with get_session()as session:
        session.query(Job).filter(Job.id==job_id).update({"is_notified":True})


def fetch_all_jobs_from_db(page = 1, page_size = 10,sort_by = "score", sort_order = "DESC"):
    ALLOWED_SORT = ["score","title","company","source","id"]
    if sort_by not in ALLOWED_SORT:
        sort_by = "score"
    if sort_order.upper() not in ["ASC","DESC"]:
        sort_order = "DESC"
    offset = (page - 1) * page_size
    with get_session() as session:
        sort_col = getattr(Job, sort_by)
        if sort_order.upper() == "DESC":
            sort_col = sort_col.desc()
        else:
            sort_col = sort_col.asc()
        
        jobs = (
            session.query(Job)
            .order_by(sort_col)
            .offset(offset)
            .limit(page_size)
            .all()
        )
        return [_job_to_dict(j) for j in jobs]
    
def search_jobs(keyword,limit = 20):
    search_pattern = f"%{keyword}%"
    with get_session() as session:
        jobs = (
            session.query(Job)
            .filter((Job.title.ilike(search_pattern)) | (Job.company.ilike(search_pattern)))
            .order_by(Job.score.desc())
            .limit(limit)
            .all()
        )
        return [_job_to_dict(j) for j in jobs]
    


def filter_jobs_by_source(source, page = 1, page_size = 10):
    offset = (page - 1) * page_size
    with get_session() as session:
        jobs = (
            session.query(Job)
            .filter(Job.source == source)
            .order_by(Job.score.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )
        return [_job_to_dict(j) for j in jobs]


def _job_to_dict(job: Job) -> dict:
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "apply_link": job.apply_link,
        "source": job.source,
        "score": job.score,
        "is_notified": job.is_notified,
        "scraped_at": job.scraped_at,
        "applied_at": job.applied_at,
    }

def query_jobs(keyword = None, source = None,min_score = None, page = 1, page_size = 10,sort_by = "score", sort_order = "DESC",location = None):
    offset = (page - 1) * page_size
    ALLOWED_SORT = ["score","title","company","source","id"]
    if sort_by not in ALLOWED_SORT:
        sort_by = "score"
    if sort_order.upper() not in ["ASC","DESC"]:
        sort_order = "DESC"
    with get_session() as session:
        query = session.query(Job)
        if keyword:
            search_pattern = f"%{keyword}%"
            query = query.filter((Job.title.ilike(search_pattern)) | (Job.company.ilike(search_pattern)))
        if source:
            query = query.filter(Job.source == source)
        if location:
            query = query.filter(Job.location.ilike(f"%{location}%"))
        if min_score is not None:
            query = query.filter(Job.score >= min_score)
        sort_col = getattr(Job, sort_by)
        if sort_order.upper() == "DESC":
            sort_col = sort_col.desc()
        else:
            sort_col = sort_col.asc()
        jobs = (
            query.order_by(sort_col)
            .offset(offset)
            .limit(page_size)
            .all()
        )
        return [_job_to_dict(j) for j in jobs]


def create_job(job_data):
    with get_session() as session:
        job = Job(
            title = job_data.title,
            company=job_data.company,
            location=job_data.location,
            apply_link=job_data.apply_link,
            source=job_data.source,
            score=job_data.score,
        )
        session.add(job)
        session.flush()
        result = _job_to_dict(job)
        return result


def update_job(job_id,job_data):
    with get_session() as session:
        job = session.query(Job).filter(Job.id == job_id).first()
        if not job:
            return None
        job.title = job_data.title
        job.company = job_data.company
        job.location = job_data.location
        job.apply_link = job_data.apply_link
        job.source = job_data.source
        job.score = job_data.score
        return _job_to_dict(job)


def delete_job(job_id):
    with get_session() as session:
        deleted = session.query(Job).filter(Job.id == job_id).delete()
        if deleted == 0:
         return 0

    try:
        from app.services.vector_store import delete_job_embedding
        delete_job_embedding(job_id)
    except Exception as e:
        print(f"Warning: Failed to delete embedding for job {job_id}: {e}")

    return deleted


def create_user(user_data):
    from sqlalchemy.exc import IntegrityError
    with get_session() as session:
        try:
            user = User(
                username = user_data.username,
                email = user_data.email,
                hashed_password = hash_password(user_data.password),
            )
            session.add(user)
            session.flush()
            result =  {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_verified": user.is_verified
            }
            session.commit()
            return result
        except IntegrityError:
            session.rollback()
            return None
        finally:
            session.close()


def get_user_by_email(email : str):
    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            return None
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "is_verified": user.is_verified,
            "google_id": user.google_id,
            "auth_provider": user.auth_provider,
            "avatar_url": user.avatar_url
            
        }

def get_user_by_google_id(google_id : str):
    with get_session() as session:
        user = session.query(User).filter(User.google_id == google_id).first()
        if not user:
            return None
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "is_verified": user.is_verified,
            "google_id": user.google_id,
            "auth_provider": user.auth_provider,
            "avatar_url": user.avatar_url
            
        }
    
def create_google_user(email: str, username: str, google_id: str, avatar_url: str = None):
    from sqlalchemy.exc import IntegrityError
    with get_session() as session:
        try:
            user = User(
                username = username,
                email = email,
                hashed_password = None,
                is_verified = True,
                google_id = google_id,
                auth_provider = "google",
                avatar_url = avatar_url
            )
            session.add(user)
            session.flush()
            result =  {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_verified": user.is_verified,
                "google_id": user.google_id,
                "auth_provider": user.auth_provider,
                "avatar_url": user.avatar_url
            }
            session.commit()
            print(f"Created Google user: {email} (ID: {user.id})")
            return result
        except IntegrityError:
            session.rollback()
            print(f"Google user {email} already exists, fetching...")
            return get_user_by_email(email)
        finally:
            session.close()
    
def link_google_to_existing_user(user_id: int, google_id: str, avatar_url: str = None):
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        user.google_id = google_id
        user.avatar_url = avatar_url or user.avatar_url
        user.is_verified = True
        if not user.auth_provider or user.auth_provider == "local":
            pass
        session.flush()
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_verified": user.is_verified,
            "google_id": user.google_id,
            "auth_provider": user.auth_provider,
            "avatar_url": user.avatar_url
        }

def save_verification_token(user_id: int, token: str):
    with get_session() as session:
        verification_token = VerificationToken(
            user_id = user_id,
            token = token
        )
        session.add(verification_token)

def get_verification_token(token: str):
    with get_session() as session:
        token_record = session.query(VerificationToken).filter(VerificationToken.token == token).first()
        if not token_record:
            return None
        return {
            "id": token_record.id,
            "user_id": token_record.user_id,
            "token": token_record.token,
            "created_at": token_record.created_at
        }


def verify_user(user_id: int):
    with get_session() as session:
         session.query(User).filter(User.id == user_id).update({"is_verified": True})

        
def delete_verification_token(token: str):
    with get_session() as session:
        session.query(VerificationToken).filter(VerificationToken.token == token).delete()

def get_agent_overview():
    """
    Get pipeline stats for the dashboard.
    
    IMPORTANT: Extract ALL data from ORM objects INSIDE the session block.
    SQLAlchemy objects become 'detached' (unreadable) after the session closes.
    """
    with get_session() as session:
        total_jobs = session.query(Job).count()
        
        latest_run = (
            session.query(PipelineRun)
            .order_by(PipelineRun.id.desc())
            .first()
        )
        
        successful_runs = (
            session.query(PipelineRun)
            .filter(PipelineRun.status == "SUCCESS")
            .count()
        )
        
        # Extract data INSIDE the session — before it closes
        if latest_run:
            latest_data = {
                "run_started_at": latest_run.run_started_at,
                "run_completed_at": latest_run.run_completed_at,
                "jobs_fetched": latest_run.jobs_fetched,
                "jobs_inserted": latest_run.jobs_inserted,
                "jobs_filtered": latest_run.jobs_filtered,
                "duplicates_skipped": latest_run.duplicates_skipped,
                "scraper_failures": latest_run.scraper_failures,
                "alerts_sent": latest_run.alerts_sent,
                "status": latest_run.status,
                "execution_time_seconds": latest_run.execution_time_seconds,
            }
        else:
            latest_data = {}
    
    # Now it's safe to return — all data was extracted inside the block
    return {
        "total_jobs": total_jobs,
        "successful_runs": successful_runs,
        "latest_run": latest_data,
    }

def fetch_diverse_recommended_jobs(limit=3):
     with get_session() as session:
        jobs = (
            session.query(Job)
            .order_by(Job.score.desc())
            .limit(50)
            .all()
        )
     results = []
     seen = set()
     for j in jobs:
        key = j.title.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        results.append(_job_to_dict(j))
        if len(results) >= limit:
            break
     return results
   



def job_exists(apply_link):
    with get_session() as session:
        existing_job = session.query(Job).filter(Job.apply_link == apply_link).first()
        return existing_job is not None
    
def backfill_job_embeddings(batch_size = 50):
    from app.services.embedding_service import generate_embedding, generate_embeddings_batch
    from app.services.vector_store import store_job_embedding
    with get_session() as session:
        jobs = session.query(Job).filter( Job.semantic_text.isnot(None),
            Job.semantic_text != "").all()
        rows = [
            {
                "id": j.id,
                "title": j.title,
                "company": j.company,
                "location": j.location,
                "apply_link": j.apply_link,
                "source": j.source,
                "score": j.score,
                "semantic_text": j.semantic_text
            }
            for j in jobs
        ]
    total = len(jobs)
    if total == 0:
        print("No jobs found for backfilling embeddings.")
        return
    print(f"Backfilling embeddings for {total} jobs...")
    embedded = 0
    for i in range(0, total, batch_size):
        batch = rows[i:i+batch_size]
        entries = []
        for row in batch:
            entries.append({
            "job_id": row["id"],
            "metadata": {
                "title": row["title"] or "",
                "company": row["company"] or "",
                "location": row["location"] or "",
                "apply_link": row["apply_link"] or "",
                "source": row["source"] or "",
                "score": row["score"] or 0
            },
            })
        texts = [row["semantic_text"] for row in batch]
        embeddings = generate_embeddings_batch(texts)
        for entry, embedding in zip(entries, embeddings):
            entry["embedding"] = embedding
        for entry in entries:
            store_job_embedding(
                job_id=entry["job_id"],
                embedding=entry["embedding"],
                metadata=entry["metadata"]
            )
        embedded += len(batch)
        print(f"  Embedded {min(i + batch_size, total)}/{total} jobs")
    print(f"Backfilling complete! Total jobs embedded: {embedded}")

def cleanup_old_jobs():
    """
    Delete jobs older than 5 days (or 15 days if applied).
    Run after each scraper pipeline run.
    """
    from datetime import datetime, timedelta

    five_days_ago = (datetime.now() - timedelta(days=5)).isoformat()
    fifteen_days_ago = (datetime.now() - timedelta(days=15)).isoformat()

    with get_session() as session:
        # Delete unapplied jobs older than 5 days
        unapplied = session.query(Job).filter(
            Job.scraped_at < five_days_ago,
            Job.applied_at == None
        ).delete()

        # Delete applied jobs older than 15 days
        applied = session.query(Job).filter(
            Job.applied_at < fifteen_days_ago,
            Job.applied_at != None
        ).delete()

        logger.info(f"Cleanup: deleted {unapplied} old jobs + {applied} old applied jobs.")
        return unapplied + applied

# Profile Functions
def get_or_create_user_profile(user_id:int) -> dict:
    with get_session() as session:
        profile = session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            profile = UserProfile(
                user_id=user_id,
                education = "[]",
                preferred_keywords = "[]",
                excluded_keywords = "[]",
                preferred_locations = "[]"
                                  )
            session.add(profile)
            session.flush()
            
        
        return _profile_to_dict(profile)

def update_profile(user_id:int,update_data:dict) -> Optional[dict]:
    import json
    db_data = {}
    for key,value in update_data.items():
        if value is None:
            continue  # Skip None — don't overwrite existing data
        if isinstance(value, list):
            db_data[key] = json.dumps(value)
        else:
            db_data[key] = value
    db_data["updated_at"] = datetime.now().isoformat()
    with get_session() as session:
        profile = session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            return None
        for key, value in db_data.items():
            setattr(profile, key, value)
        session.flush()
        return _profile_to_dict(profile)
    
def _profile_to_dict(profile: UserProfile) -> dict:
    """Convert a UserProfile ORM object to a dict for API responses."""
    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "full_name": profile.full_name or "",
        "headline": profile.headline or "",
        "bio": profile.bio or "",
        "profile_photo_url": profile.profile_photo_url or "",
        "mobile": profile.mobile or "",
        "location": profile.location or "",
        "linkedin_url": profile.linkedin_url or "",
        "github_url": profile.github_url or "",
        "portfolio_url": profile.portfolio_url or "",
        "education_degree": profile.education_degree or "",
        "education_field": profile.education_field or "",
        "education_school": profile.education_school or "",
        "education_year": profile.education_year or "",
        "education": profile.education or "[]",
        "preferred_keywords": profile.preferred_keywords or "[]",
        "excluded_keywords": profile.excluded_keywords or "[]",
        "preferred_locations": profile.preferred_locations or "[]",
        "remote_only": profile.remote_only or False,
        "updated_at": profile.updated_at or "",
    }

         
    
 


