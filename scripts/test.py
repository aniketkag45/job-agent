# from app.services.database import backfill_job_embeddings
# backfill_job_embeddings()

# from app.services.job_domain_filter import is_domain_relevant, EXCLUDED_DOMAINS, REQUIRED_TECH_SIGNALS

# # Test some job titles that might be getting filtered
# titles = [
#     'Junior Business Developer Bangalore F M X',
#     'Software Engineer',
#     'Product Manager',
#     'Data Analyst',
#     'Technical Support Specialist',
#     'QA Engineer',
#     'Systems Administrator',
#     'Network Engineer',
# ]

# for title in titles:
#     job = {'title': title}
#     result = is_domain_relevant(job)
#     print(f'  {"KEEP" if result else "FILTER"}  →  {title}')

# from app.services.vector_store import clear_collection
# clear_collection()
# print('ChromaDB cleared.')

# from app.services.job_domain_filter import is_domain_relevant

# test = [
#     ('Digital Advertising Campaign Manager', False),
#     ('Jamaica Interpreter', False),
#     ('Télétravail Professeur Particulier', False),
#     ('Junior Business Developer', True),    # has 'developer'
#     ('Senior Software Engineer', True),     # has 'software', 'engineer'
#     ('Python Backend Developer Intern', True),
#     ('ML Engineer', True),                  # 'ml' as standalone word
#     ('AI Research Scientist', True),       # 'ai' as standalone word
#     ('Data Analyst', True),                # 'data analyst'
#     ('Systems Administrator', True),        # now added
# ]

# all_pass = True
# for title, expected in test:
#     result = is_domain_relevant({'title': title})
#     status = 'OK' if result == expected else 'WRONG'
#     if status == 'WRONG':
#         all_pass = False
#     print(f'  {status:5s}  {"KEEP" if result else "FILTER"}  → {title}  (expected: {"KEEP" if expected else "FILTER"})')

# print()
# print('ALL PASSED!' if all_pass else 'SOME FAILED — check above')

import sqlite3
conn = sqlite3.connect('database/jobs.db')
c = conn.cursor()
c.execute('DELETE FROM jobs')
conn.commit()
conn.close()
print('SQLite database cleared.')

from app.services.vector_store import clear_collection
clear_collection()
print('ChromaDB cleared.')

# import requests
# r = requests.get('https://boards-api.greenhouse.io/v1/boards/stripe/jobs?content=true')
# data = r.json()
# job = data['jobs'][0]
# print('Available fields:', list(job.keys()))
# print()
# print('Sample job:')
# for k in job:
#     val = job[k]
#     if isinstance(val, str) and len(val) > 100:
#         val = val[:100] + '...'
#     print(f'  {k}: {val}')