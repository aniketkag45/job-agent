import sqlite3
from app.auth.security import hash_password
from app.services.pipeline_metrics import increment_metric
from app.services.semantic_representation import (
    build_semantic_representation
)

DATABASE_PATH = 'database/jobs.db'

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def insert_job(job):

    connection = get_connection()

    cursor = connection.cursor()

    try:
        semantic_text = build_semantic_representation(job)

        cursor.execute(
            '''
            INSERT INTO jobs (
                title,
                company,
                location,
                apply_link,
                source,
                score,
                semantic_text
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                job.get('title'),
                job.get('company'),
                job.get('location'),
                job.get('apply_link'),
                job.get('source'),
                job.get('score'),
                semantic_text
            )
        )

        connection.commit()

        print(
            f"Inserted job: {job.get('title')}"
        )

        return True


    except sqlite3.IntegrityError:

        increment_metric(
            "duplicates_skipped"
        )

        

        return False


    finally:

        connection.close()
        
def fetch_jobs(limit = 10):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT title, company, location, apply_link, source, score
        FROM jobs
        ORDER BY score DESC
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    connection.close()
    jobs = []
    for row in rows:
        jobs.append({
            "title": row[0],
            "company": row[1],
            "location": row[2],
            "apply_link": row[3],
            "source": row[4],
            "score": row[5]
        })

    return jobs
            
def fetch_unnotified_jobs():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT

        id,
        title,
        company,
        location,
        apply_link,
        source,
        score

    FROM jobs

    WHERE is_notified = 0

    ORDER BY score DESC
    """)
                   
    rows = cursor.fetchall()
    connection.close()
    jobs = []
    for row in rows:
        jobs.append({
            "id": row[0],
            "title": row[1],
            "company": row[2],
            "location": row[3],
            "apply_link": row[4],
            "source": row[5],
            "score": row[6]
        })

    return jobs

def mark_job_as_notified(job_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE jobs
    SET is_notified = 1
    WHERE id = ?
    """, (job_id,))
    connection.commit()
    connection.close()
    print(f"Marked job ID {job_id} as notified.")

def fetch_all_jobs_from_db(page = 1, page_size = 10,sort_by = "score", sort_order = "DESC"):
    offset = (page - 1) * page_size
    allowed_sort_fields = ["score", "title", "company", "source"]
    if sort_by not in allowed_sort_fields:
        sort_by = "score"
    if sort_order.lower() not in ["ASC", "DESC"]:
        sort_order = "DESC"
    connection = get_connection()
    cursor = connection.cursor()
    query = f"""
    SELECT
        id,
        title,
        company,
        location,
        apply_link,
        source,
        score,
        is_notified

    FROM jobs
    ORDER BY {sort_by} {sort_order}
    LIMIT ? OFFSET ?
    """

  
    cursor.execute(query, (page_size, offset))

    rows = cursor.fetchall()
    connection.close()
    jobs = []
    
    for row in rows:
        jobs.append({
            "id": row[0],
            "title": row[1],
            "company": row[2],
            "location": row[3],
            "apply_link": row[4],
            "source": row[5],
            "score": row[6],
            "is_notified": row[7]
        })
    return jobs

def search_jobs(keyword,limit = 20):
    connection = get_connection()
    cursor = connection.cursor()
    search_pattern = f"%{keyword}%"
    cursor.execute("""
    SELECT

        id,
        title,
        company,
        location,
        apply_link,
        source,
        score,
        is_notified

    FROM jobs

    WHERE title LIKE ? OR company LIKE ? 

    ORDER BY score DESC
    LIMIT ?
    """, (search_pattern, search_pattern, limit))

    rows = cursor.fetchall()
    connection.close()
    jobs = []
    for row in rows:
        jobs.append({
            "id": row[0],
            "title": row[1],
            "company": row[2],
            "location": row[3],
            "apply_link": row[4],
            "source": row[5],
            "score": row[6],
            "is_notified": row[7]
        })
    return jobs

def filter_jobs_by_source(source, page = 1, page_size = 10):
    offset = (page - 1) * page_size
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT

        id,
        title,
        company,
        location,
        apply_link,
        source,
        score,
        is_notified

    FROM jobs

    WHERE source = ?

    ORDER BY score DESC
    LIMIT ? OFFSET ?
    """, (source, page_size, offset))

    rows = cursor.fetchall()
    connection.close()
    jobs = []
    for row in rows:
        jobs.append({
            "id": row[0],
            "title": row[1],
            "company": row[2],
            "location": row[3],
            "apply_link": row[4],
            "source": row[5],
            "score": row[6],
            "is_notified": row[7]
        })
    return jobs

def query_jobs(keyword = None, source = None,min_score = None, page = 1, page_size = 10,sort_by = "score", sort_order = "DESC",location = None):
    offset = (page - 1) * page_size
    allowed_sort_fields = ["score", "title", "company", "source"]
    if sort_by not in allowed_sort_fields:
        sort_by = "score"
    if sort_order.lower() not in ["asc", "desc"]:
        sort_order = "DESC"

    connection = get_connection()
    cursor = connection.cursor()
    query = """
    SELECT

        id,
        title,
        company,
        location,
        apply_link,
        source,
        score,
        is_notified

        FROM jobs
        WHERE 1=1
    """
    params = []
    if keyword:
        query += " AND (title LIKE ? OR company LIKE ?)"
        search_pattern = f"%{keyword}%"
        params.extend([search_pattern, search_pattern])
    if source:
        query += " AND source = ?"
        params.append(source)
    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")
    if min_score is not None:
        query += " AND score >= ?"
        params.append(min_score)    
    query += f" ORDER BY {sort_by} {sort_order}"
    query += " LIMIT ? OFFSET ?"
    params.extend([page_size, offset])
    cursor.execute(query, params)
    rows = cursor.fetchall()
    connection.close()
    jobs = []
    for row in rows:
        jobs.append({
            "id": row[0],
            "title": row[1],
            "company": row[2],
            "location": row[3],
            "apply_link": row[4],
            "source": row[5],
            "score": row[6],
            "is_notified": row[7]
        })
    return jobs

def create_job(job_data):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO jobs (

        title,
        company,
        location,
        apply_link,
        source,
        score,
        is_notified

    ) VALUES (?, ?, ?, ?, ?, ?, 0)
    """, (

        job_data.title,

        job_data.company,

        job_data.location,

        job_data.apply_link,

        job_data.source,

        job_data.score
    ))

    connection.commit()

    job_id = cursor.lastrowid

    connection.close()

    return {

        "id": job_id,

        **job_data.dict(),

        "is_notified": 0
    }


def update_job(job_id, job_data):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
    UPDATE jobs
    SET title = ?, company = ?, location = ?, apply_link = ?, source = ?, score = ?
    WHERE id = ?
    """, (
        job_data.title,
        job_data.company,
        job_data.location,
        job_data.apply_link,
        job_data.source,
        job_data.score,
        job_id
    ))

    connection.commit()

    connection.close()

    return {

        "id": job_id,

        **job_data.dict(),

        "is_notified": 0
    }


def delete_job(job_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM jobs

    WHERE id = ?
    """, (job_id,))

    connection.commit()

    affected_rows = cursor.rowcount

    connection.close()

    return affected_rows

def create_user(user_data):
    connection = get_connection()
    cursor = connection.cursor()
    hashed_password = hash_password(user_data.password)
    try:
        cursor.execute("""
        INSERT INTO users (
            username,
            email,
            hashed_password
        ) VALUES (?, ?, ?)
        """, (
            user_data.username,
            user_data.email,
            hashed_password
        ))
        connection.commit()
        user_id = cursor.lastrowid
        return {
            "id": user_id,
            "username": user_data.username,
            "email": user_data.email,
            "is_verified": 0
        }
    except sqlite3.IntegrityError:
        return None
    finally:
        connection.close()
    
def get_user_by_email(email : str):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT *
    FROM users
    WHERE email = ?
    """, (email,))
    user = cursor.fetchone()
    connection.close()
    
    return user

def save_verification_token(user_id: int, token: str):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO verification_tokens (user_id, token)
    VALUES (?, ?)
    """, (user_id, token))
    connection.commit()
    connection.close()

def get_verification_token(token: str):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT *
    FROM verification_tokens
    WHERE token = ?
    """, (token,))
    token_record = cursor.fetchone()
    connection.close()
    
    return token_record

def verify_user(user_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE users
    SET is_verified = 1
    WHERE id = ?
    """, (user_id,))
    connection.commit()
    connection.close()

def delete_verification_token(token: str):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    DELETE FROM verification_tokens
    WHERE token = ?
    """, (token,))
    connection.commit()
    connection.close()

def get_agent_overview():

    connection = get_connection()

    cursor = connection.cursor()


    # Total jobs count

    cursor.execute("""

    SELECT COUNT(*) AS total_jobs

    FROM jobs

    """)

    total_jobs = cursor.fetchone()["total_jobs"]


    # Latest pipeline run

    cursor.execute("""

    SELECT *

    FROM pipeline_runs

    ORDER BY id DESC

    LIMIT 1

    """)

    latest_run = cursor.fetchone()


    # Total successful runs

    cursor.execute("""

    SELECT COUNT(*) AS successful_runs

    FROM pipeline_runs

    WHERE status = 'SUCCESS'

    """)

    successful_runs = cursor.fetchone()["successful_runs"]


    connection.close()


    return {

        "total_jobs": total_jobs,

        "successful_runs": successful_runs,

        "latest_run": {

            "run_started_at": latest_run["run_started_at"],

            "run_completed_at": latest_run["run_completed_at"],

            "jobs_fetched": latest_run["jobs_fetched"],

            "jobs_inserted": latest_run["jobs_inserted"],

            "jobs_filtered": latest_run["jobs_filtered"],

            "duplicates_skipped": latest_run["duplicates_skipped"],

            "scraper_failures": latest_run["scraper_failures"],

            "alerts_sent": latest_run["alerts_sent"],

            "status": latest_run["status"],

            "execution_time_seconds": latest_run["execution_time_seconds"]

        }
    }

def fetch_diverse_recommended_jobs(limit=3):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
    SELECT

        id,
        title,
        company,
        location,
        apply_link,
        source,
        score,
        is_notified

    FROM jobs

    ORDER BY score DESC
    LIMIT 50
    """)

    rows = cursor.fetchall()

    connection.close()

    jobs = []

    seen_titles = set()

    for row in rows:

        normalized_title = (
            row[1]
            .strip()
            .lower()
        )

        if normalized_title in seen_titles:

            continue

        seen_titles.add(
            normalized_title
        )

        jobs.append({

            "id": row[0],

            "title": row[1],

            "company": row[2],

            "location": row[3],

            "apply_link": row[4],

            "source": row[5],

            "score": row[6],

            "is_notified": row[7]
        })

        if len(jobs) >= limit:

            break

    return jobs

def job_exists(apply_link):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

    SELECT id

    FROM jobs

    WHERE apply_link = ?

    LIMIT 1

    """, (apply_link,))

    existing_job = cursor.fetchone()

    connection.close()

    return existing_job is not None