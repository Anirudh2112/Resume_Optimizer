from ..models import Resume, Keyword, AnalysisResult
import spacy
import re
from typing import List, Dict
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define common technical and soft skills
TECHNICAL_SKILLS = {
    'languages': [
        'python', 'java', 'javascript', 'c++', 'ruby', 'php', 'swift', 'kotlin',
        'golang', 'rust', 'typescript', 'sql', 'html', 'css'
    ],
    'frameworks': [
        'react', 'angular', 'vue', 'django', 'flask', 'spring', 'node.js',
        'express', 'fastapi', 'pytorch', 'tensorflow', 'keras'
    ],
    'tools': [
        'docker', 'kubernetes', 'aws', 'gcp', 'azure', 'git', 'jenkins',
        'jira', 'postgresql', 'mongodb', 'mysql', 'redis', 'elasticsearch'
    ],
    'concepts': [
        'machine learning', 'deep learning', 'nlp', 'computer vision',
        'data science', 'agile', 'ci/cd', 'devops', 'microservices',
        'rest api', 'graphql', 'oauth', 'jwt'
    ]
}

SOFT_SKILLS = [
    'leadership', 'communication', 'teamwork', 'problem solving',
    'analytical', 'project management', 'time management', 'adaptability',
    'collaboration', 'creativity', 'critical thinking', 'decision making',
    'mentoring', 'presentation', 'negotiation'
]

def extract_keywords(text: str) -> List[Keyword]:
    """
    Extract and categorize keywords from text - combining predefined lists and dynamic extraction
    """
    keywords = []
    doc = nlp(text.lower())
    
    # Extract from predefined lists
    from_predefined = extract_from_predefined_lists(text, doc)
    keywords.extend(from_predefined)
    
    # Extract additional keywords dynamically
    dynamic_keywords = extract_dynamic_keywords(text, doc)
    
    # Add dynamic keywords that aren't already in the list
    existing_texts = {kw.text for kw in keywords}
    for kw in dynamic_keywords:
        if kw.text not in existing_texts:
            keywords.append(kw)
            existing_texts.add(kw.text)
    
    return keywords

def extract_from_predefined_lists(text: str, doc: spacy.tokens.Doc) -> List[Keyword]:
    """
    Extract keywords from predefined lists
    """
    keywords = []
    
    # Extract technical skills
    for category, skills in TECHNICAL_SKILLS.items():
        for skill in skills:
            if re.search(rf'\b{re.escape(skill)}\b', text.lower()):
                # Calculate relevance score based on frequency and context
                score = calculate_relevance_score(doc, skill)
                keywords.append(Keyword(
                    text=skill,
                    category='technical',
                    relevance_score=score
                ))
    
    # Extract soft skills
    for skill in SOFT_SKILLS:
        if re.search(rf'\b{re.escape(skill)}\b', text.lower()):
            score = calculate_relevance_score(doc, skill)
            keywords.append(Keyword(
                text=skill,
                category='soft',
                relevance_score=score
            ))
    
    return keywords

def extract_dynamic_keywords(text: str, doc: spacy.tokens.Doc) -> List[Keyword]:
    """
    Extract keywords dynamically from text using NLP techniques
    """
    keywords = []
    
    # Skill-related terms often found in job descriptions
    skill_indicators = ['experience with', 'knowledge of', 'proficiency in', 'skilled in', 
                       'familiarity with', 'background in', 'expertise in', 'working knowledge']
    
    # Extract noun phrases following skill indicators
    for indicator in skill_indicators:
        pattern = rf'{indicator}\s+([\w\s\-\/]+)'
        matches = re.finditer(pattern, text.lower())
        for match in matches:
            if match.group(1):
                skill = match.group(1).strip()
                if len(skill.split()) < 4:  # Avoid very long phrases
                    keywords.append(Keyword(
                        text=skill,
                        category='technical' if is_technical_skill(skill) else 'soft',
                        relevance_score=0.8
                    ))
    
    # Extract named entities that might be technologies or tools
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"]:
            text = ent.text.lower()
            if len(text.split()) < 3:  # Avoid long entity names
                keywords.append(Keyword(
                    text=text,
                    category='technical',
                    relevance_score=0.7
                ))
    
    # Extract other potentially important terms
    important_pos = ["NOUN", "PROPN"]
    for token in doc:
        if token.pos_ in important_pos and not token.is_stop and len(token.text) > 3:
            if is_likely_skill(token.text.lower(), doc):
                keywords.append(Keyword(
                    text=token.text.lower(),
                    category='technical',
                    relevance_score=0.6
                ))
    
    return keywords

def is_technical_skill(text: str) -> bool:
    """
    Determine if a term is likely a technical skill
    """
    technical_indicators = ['software', 'hardware', 'programming', 'development', 
                          'technology', 'system', 'framework', 'language', 'database',
                          'platform', 'tool', 'api', 'code', 'design', 'algorithm',
                          'application', 'architecture', 'cloud', 'data', 'server']
    
    return any(indicator in text for indicator in technical_indicators)

def is_likely_skill(text: str, doc: spacy.tokens.Doc) -> bool:
    """
    Determine if a term is likely a skill based on context
    """
    # Check if it appears in contexts that suggest it's a skill
    for token in doc:
        if token.text.lower() == text:
            # Check left context
            left_context = doc[max(0, token.i-3):token.i]
            for left_token in left_context:
                if left_token.text.lower() in ['skilled', 'experience', 'knowledge', 'proficient']:
                    return True
            
            # Check right context
            right_context = doc[token.i+1:min(len(doc), token.i+4)]
            for right_token in right_context:
                if right_token.text.lower() in ['experience', 'skills', 'knowledge']:
                    return True
    
    return False

def calculate_relevance_score(doc: spacy.tokens.Doc, keyword: str) -> float:
    """
    Calculate relevance score for a keyword based on:
    - Frequency
    - Context (proximity to important words)
    - Position in document
    """
    frequency = len(re.findall(rf'\b{re.escape(keyword)}\b', doc.text.lower()))
    
    # Find keyword mentions and their contexts
    importance_words = ['required', 'essential', 'must', 'key', 'primary', 'core', 
                       'preferred', 'desired', 'important', 'necessary']
    context_score = 0
    
    for token in doc:
        if token.text.lower() in keyword:
            # Check surrounding words
            surrounding = doc[max(0, token.i-5):min(len(doc), token.i+6)]
            for word in surrounding:
                if word.text.lower() in importance_words:
                    context_score += 1
    
    # Normalize scores
    freq_score = min(frequency / 3, 1.0)  # Cap at 1.0
    context_score = min(context_score / 2, 1.0)
    
    # Combine scores (weighted average)
    return (freq_score * 0.7) + (context_score * 0.3)

def calculate_ats_score(resume: Resume, keywords: List[Keyword]) -> AnalysisResult:
    """
    Calculate ATS score and analyze keyword matches
    """
    missing_keywords = defaultdict(list)
    matched_keywords = defaultdict(list)
    section_scores = {}
    improvement_suggestions = defaultdict(list)
    
    # Check each keyword against resume content
    for keyword in keywords:
        keyword_pattern = rf'\b{re.escape(keyword.text)}\b'
        
        # Check in full resume text first
        if re.search(keyword_pattern, resume.raw_text, re.IGNORECASE):
            matched_keywords[keyword.category].append(keyword.text)
        else:
            missing_keywords[keyword.category].append(keyword.text)
            
            # Generate improvement suggestions for sections
            for section in resume.sections:
                if keyword.relevance_score > 0.7:  # High relevance keywords
                    suggestion = f"Consider adding '{keyword.text}' to this section"
                    if suggestion not in improvement_suggestions[section.title]:
                        improvement_suggestions[section.title].append(suggestion)
    
    # Calculate section-specific scores
    for section in resume.sections:
        section_matches = sum(
            1 for kw in keywords 
            if re.search(rf'\b{re.escape(kw.text)}\b', section.content, re.IGNORECASE)
        )
        section_scores[section.title] = (section_matches / len(keywords) * 100) if len(keywords) > 0 else 0
    
    # Calculate overall ATS score
    total_keywords = len(keywords)
    total_matched = len(matched_keywords['technical']) + len(matched_keywords['soft'])
    ats_score = (total_matched / total_keywords * 100) if total_keywords > 0 else 0
    
    return AnalysisResult(
        ats_score=round(ats_score, 2),
        missing_keywords=dict(missing_keywords),
        matched_keywords=dict(matched_keywords),
        section_scores=section_scores,
        improvement_suggestions=dict(improvement_suggestions)
    )