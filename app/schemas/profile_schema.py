from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional,List
import json

class EducationItem(BaseModel):
    degree: str = ""
    field: str = ""
    school: str = ""
    year: str = ""

class ProfileUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    headline: Optional[str] = None
    bio: Optional[str] = None
    profile_photo_url: Optional[str] = None
    mobile: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    education_degree: Optional[str] = None
    education_field: Optional[str] = None
    education_school: Optional[str] = None
    education_year: Optional[str] = None
    education: Optional[List[EducationItem]] = None
    preferred_keywords: Optional[List[str]] = None
    excluded_keywords: Optional[List[str]] = None
    preferred_locations: Optional[List[str]] = None
    remote_only: Optional[bool] = None

class ProfileResponseSchema(BaseModel):
    id: int
    user_id: int
    full_name: Optional[str] = ""
    headline: Optional[str] = ""
    bio: Optional[str] = ""
    profile_photo_url: Optional[str] = ""
    mobile: Optional[str] = ""
    location: Optional[str] = ""
    linkedin_url: Optional[str] = ""
    github_url: Optional[str] = ""
    portfolio_url: Optional[str] = ""
    education_degree: Optional[str] = ""
    education_field: Optional[str] = ""
    education_school: Optional[str] = ""
    education_year: Optional[str] = ""
    education: Optional[List[EducationItem]] = []
    preferred_keywords: Optional[List[str]] = []
    excluded_keywords: Optional[List[str]] = []
    preferred_locations: Optional[List[str]] = []
    remote_only: bool = False

    @field_validator('education', mode='before')
    @classmethod
    def parse_education(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError , TypeError):
                return []
        return v or []
    
    @field_validator('preferred_keywords', 'excluded_keywords', 'preferred_locations', mode='before')
    @classmethod
    def parse_json_list(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError , TypeError):
                return []
        return v or []