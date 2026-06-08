import os
import logging
from typing import Dict, Any,Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

client = None
def get_client():
    global client
    if client is None:
        if not LLM_API_KEY:
            logger.warning("LLM_API_KEY is not set. LLM functionalities will be disabled.")
            return None
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=LLM_API_KEY,
                base_url=LLM_BASE_URL
            )
            logger.info("LLM client initialized successfully.")
        except ImportError as e:
            logger.error(f"OpenAI library is not installed: {e}")
            return None
        except Exception as e:
            logger.error(f"Error initializing LLM client: {e}")
            return None
    return client

def call_llm(
        system_prompt: str,
        user_message: str,
        temperature: float = 0.3,
        max_tokens: int = 500,
) -> Optional[str]:
    client = get_client()
    if client is None:
        logger.error("LLM client is not available. Cannot call LLM.")
        return None
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error calling LLM: {e}")
        return None
    
def explain_match(job: Dict[str,Any],
                  candidate_profile: Dict[str,Any],
                  )-> Optional[str]:
    skills = ", ".join(candidate_profile.get("skills", []))
    domains = ", ".join(candidate_profile.get("domains", []))
    experience = ", ".join(candidate_profile.get("experience_level", []))
    job_title = job.get("title", "Unknown Role")
    job_company = job.get("company", "Unknown Company")
    job_location = job.get("location", "Unknown Location")
    job_description = job.get("description", "")[:500]  # Truncate for prompt
    job_tech = ", ".join(job.get("tech_stack", []))
    system_prompt = (
        "You are a career match analyst. Given a job and a candidate profile, "
        "explain in 2-4 sentences why this job is a good match (or not). "
        "Be honest — if the job doesn't match, say so. "
        "Focus on: skill overlap, experience level alignment, "
        "domain match, and location fit."
    )
    user_message = (
          f"JOB:\n"
        f"  Title: {job_title}\n"
        f"  Company: {job_company}\n"
        f"  Location: {job_location}\n"
        f"  Tech Stack: {job_tech}\n"
        f"  Description: {job_description}\n\n"
        f"CANDIDATE:\n"
        f"  Skills: {skills}\n"
        f"  Domains: {domains}\n"
        f"  Experience Level: {experience}\n\n"
        f"Explain the match (or mismatch) in 2-4 sentences."
    )
    return call_llm(system_prompt, user_message, temperature=0.3, max_tokens=250)

def generate_cover_letter(job: Dict[str,Any], candidate_profile: Dict[str,Any], candidate_name: str = "Candidate") -> Optional[str]:
    skills = ", ".join(candidate_profile.get("skills", []))
    experience = ", ".join(candidate_profile.get("experience_level","unknown"))
    job_title = job.get("title", "Unknown Role")
    job_company = job.get("company", "Unknown Company")
    job_description = job.get("description", "")[:800]  # Truncate for prompt
    job_tech = ", ".join(job.get("tech_stack", []))
    system_prompt = (
        "You are a professional cover letter writer. Write a compelling, "
        "concise cover letter. 3 short paragraphs: opening, skills match, "
        "closing. Use [Hiring Manager] as greeting since we don't know the name. "
        "Be professional but enthusiastic. Do NOT make up experience — only "
        "reference skills that are actually listed."
    )
    user_message = (
          f"JOB:\n"
        f"  Title: {job_title}\n"
        f"  Company: {job_company}\n"
        f"  Tech Stack: {job_tech}\n"
        f"  Description: {job_description}\n\n"
        f"CANDIDATE:\n"
        f"  Name: {candidate_name}\n"
        f"  Skills: {skills}\n"
        f"  Experience Level: {experience}\n\n"
        f"Write a personalized cover letter."
    )
    return call_llm(system_prompt, user_message, temperature=0.7, max_tokens=500)

def summarize_job_description(
    job_title: str,
    job_description: str,
) -> Optional[str]:
    if not job_description or len(job_description) < 50:
        return job_description  # Return as-is if too short to summarize
    system_prompt = (
         "You are a job description summarizer. Extract key information "
        "in 3-5 bullet points. Focus on: tech stack, main responsibilities, "
        "required experience, standout perks. Be concise."
    )
    user_message = (
        f"JOB TITLE: {job_title}\n\n"
        f"DESCRIPTION:\n{job_description}\n\n"
        f"Summarize the key points in 3-5 bullets."
    )
    return call_llm(system_prompt, user_message, temperature=0.3, max_tokens=300)
