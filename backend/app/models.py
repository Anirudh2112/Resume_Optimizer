from pydantic import BaseModel
from typing import List, Dict, Optional

class JobDescription(BaseModel):
    text: str

class ResumeSection(BaseModel):
    title: str
    content: str

class Resume(BaseModel):
    sections: List[ResumeSection]
    raw_text: str

class Keyword(BaseModel):
    text: str
    category: str  # 'technical' or 'soft'
    relevance_score: float

class OptimizationRequest(BaseModel):
    section_title: str
    current_content: str
    selected_keywords: List[str]

class OptimizationResponse(BaseModel):
    optimized_content: str
    added_keywords: List[str]
    confidence_score: float

class AnalysisResult(BaseModel):
    ats_score: float
    missing_keywords: Dict[str, List[str]]
    matched_keywords: Dict[str, List[str]]
    section_scores: Dict[str, float]
    improvement_suggestions: Dict[str, List[str]]

class Error(BaseModel):
    code: str
    message: str