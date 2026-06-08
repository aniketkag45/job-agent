import json
import os
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException,UploadFile, File
from app.services.resume_parser import extract_resume_text_from_bytes
from app.services.candidate_profile_builder import build_candidate_profile
from app.services.candidate_semantic_representation import build_candidate_semantic_text
from app.services.embedding_service import generate_embedding
from app.schemas.response_schema import ApiResponse
from app.auth.dependencies import get_current_user

router = APIRouter()

STORAGE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "storage")

PROFILE_PATH = os.path.join(STORAGE_DIR, "candidate_profiles.json")

def load_profile() -> Optional[dict]:
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    return None

def save_profile(profile: dict) -> None:
    os.makedirs(STORAGE_DIR, exist_ok=True)
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)

@router.post("/resume/upload", response_model=ApiResponse)
async def upload_resume(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")
    try:
        file_bytes = await file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Error reading file. Please try again.")
    try:
        resume_text = extract_resume_text_from_bytes(file_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Error extracting text from PDF. Ensure it's a valid PDF file. Details: {str(e)}"

        )
    if not resume_text or not resume_text.strip():
        raise HTTPException(status_code=422, detail="No text could be extracted from the PDF. Please upload a valid resume.")
    
    profile = build_candidate_profile(resume_text)
    semantic_text = build_candidate_semantic_text(profile)
    embedding = generate_embedding(semantic_text)
    full_data = {
        "profile": profile,
        "semantic_text": semantic_text,
        "embedding": embedding,
        "resume_length": len(resume_text),
        "file_name": file.filename,
    }
    save_profile(full_data)
    return ApiResponse(
        success = True,
        data = {
            "profile": profile,
            "semantic_text_preview": semantic_text[:200] + "..." if len(semantic_text) > 200 else semantic_text,
            "embedding_dimension": len(embedding),
            "resume_length": len(resume_text),
        },
        message = "Resume processed! Your agent now knows your skills and can find matching jobs."
    )

@router.get("/resume/profile", response_model=ApiResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    stored = load_profile()
    if not stored:
        return ApiResponse(
            success = False,
            data = None,
            message = "No resume uploaded yet. Please upload your resume first."
        )
    return ApiResponse(
        success = True,
        data = {
            "profile": stored.get("profile"),
            "semantic_text_preview": stored.get("semantic_text", "")[:200] + "...",
            "resume_length": stored.get("resume_length", 0),
            "file_name": stored.get("file_name", "unknown"),
        },
        message = "Candidate profile retrieved successfully."
    )

@router.delete("/resume/profile", response_model=ApiResponse)
async def delete_profile(current_user: dict = Depends(get_current_user)):
    if os.path.exists(PROFILE_PATH):
        os.remove(PROFILE_PATH)
        return ApiResponse(
            success = True,
            data = None,
            message = "Candidate profile deleted successfully."
        )
    return ApiResponse(
            success = False,
            data = None,
            message = "No candidate profile found to delete."
    )
        

