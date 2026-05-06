import json
import os

def save_jobs_to_json(jobs, file_path = "scripts/jobs.json"):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path,"w",encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=4)
    
    print(f"\nSaved {len(jobs)} jobs to {file_path}")