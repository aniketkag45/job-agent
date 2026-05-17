from pydantic import BaseModel

class JobSchema(BaseModel):
    id: int
    title: str
    company: str
    location: str
    apply_link: str
    source: str
    score: int
    is_notified: int

class JobCreateSchema(BaseModel):
    title: str
    company: str
    location: str
    apply_link: str
    source: str
    score: int=0