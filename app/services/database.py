import sqlite3

DATABASE_PATH = 'database/jobs.db'

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

def insert_job(job):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO jobs (
                       title, 
                       company, 
                       location,
                        apply_link, 
                       source,
                        score
                       )VALUES (?, ?, ?, ?, ?, ?)
        ''', (
             job.get('title'),
             job.get('company'),
             job.get('location'),
             job.get('apply_link'), 
             job.get('source'),
             job.get('score')))
        connection.commit()
        print(f"Inserted job: "
              f"{job.get('title')}"
              )
    except sqlite3.IntegrityError:
        print(f"Duplicate job skipped: "
              f"{job.get('title')}"
              )
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
