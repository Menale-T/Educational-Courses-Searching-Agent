from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os
import sys

class InstitutionAnalysis(BaseModel):

    pricing: str
    is_online: Optional[bool] = None
    duration: str = ""
    certificate_available: Optional[bool] = None

class InstitutionInfo(BaseModel):
    
    name: str
    description: str
    website: str
    pricing: str = ""
    is_online: Optional[bool] = None
    duration: str = ""
    ##certificate_available = Optional[bool] = None
    learning_experience_rating: Optional[str] = None

class ResearchState(BaseModel):
    query: str
    extracted_courses: List[str] = []
    institutions: List[InstitutionInfo] = []
    search_results: List[Dict[str, Any]] = []
    analysis: Optional[str] = None



