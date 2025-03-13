import re
from typing import List, Dict, Set
import spacy
from collections import defaultdict

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

class TextProcessor:
    def __init__(self):
        self.common_sections = {
            'summary': {'summary', 'professional summary', 'profile', 'objective'},
            'experience': {'experience', 'work experience', 'employment history', 'work history'},
            'education': {'education', 'academic background', 'academic history'},
            'skills': {'skills', 'technical skills', 'core competencies', 'technologies'},
            'projects': {'projects', 'key projects', 'personal projects'},
            'certifications': {'certifications', 'certificates', 'professional certifications'},
        }

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        """
        # Remove special characters but keep periods and commas
        text = re.sub(r'[^\w\s.,]', ' ', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.strip()

    def identify_section(self, text: str) -> str:
        """
        Identify which section a piece of text belongs to
        """
        text_lower = text.lower()
        
        for section_type, variants in self.common_sections.items():
            if any(variant in text_lower for variant in variants):
                return section_type
        
        return 'other'

    def extract_bullet_points(self, text: str) -> List[str]:
        """
        Extract bullet points from text
        """
        # Common bullet point markers
        markers = [r'•', r'-', r'\*', r'○', r'►', r'‣', r'⁃', r'·']
        
        # Create pattern for bullet points
        pattern = f"(?:{'|'.join(markers)})\\s*(.+?)(?=(?:{'|'.join(markers)})|$)"
        
        # Find all bullet points
        points = re.findall(pattern, text, re.MULTILINE | re.DOTALL)
        
        # Clean and filter empty points
        return [self.clean_text(point) for point in points if point.strip()]

    def extract_sentences(self, text: str) -> List[str]:
        """
        Extract sentences from text using spaCy
        """
        doc = nlp(text)
        return [str(sent).strip() for sent in doc.sents]

    def has_metrics(self, text: str) -> bool:
        """
        Check if text contains metrics (numbers, percentages, etc.)
        """
        # Patterns for different types of metrics
        patterns = [
            r'\d+%',                    # Percentages
            r'\$\d+(?:,\d{3})*',       # Dollar amounts
            r'\d+(?:,\d{3})*\+?',      # Numbers with commas
            r'\d+k\+?',                # Numbers with k (thousand)
            r'\d+M\+?',                # Numbers with M (million)
            r'\d+B\+?',                # Numbers with B (billion)
        ]
        
        return any(re.search(pattern, text) for pattern in patterns)

    def extract_keywords(self, text: str) -> Dict[str, Set[str]]:
        """
        Extract potential keywords from text
        """
        doc = nlp(text)
        keywords = defaultdict(set)
        
        for token in doc:
            # Technical terms (usually nouns)
            if token.pos_ == "NOUN":
                keywords['technical'].add(token.text.lower())
            
            # Action verbs
            elif token.pos_ == "VERB":
                keywords['action'].add(token.lemma_.lower())
            
            # Skills and tools (proper nouns)
            elif token.pos_ == "PROPN":
                keywords['skill'].add(token.text)
        
        return dict(keywords)

    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts using spaCy
        """
        doc1 = nlp(text1)
        doc2 = nlp(text2)
        return doc1.similarity(doc2)

    def format_bullet_point(self, text: str) -> str:
        """
        Format text as a proper bullet point
        """
        # Remove existing bullet points
        text = re.sub(r'^[•\-\*○►‣⁃·]\s*', '', text.strip())
        
        # Ensure it starts with a capital letter
        text = text[0].upper() + text[1:] if text else text
        
        # Add period if missing
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        
        return f"• {text}"

    def estimate_bullet_point_quality(self, text: str) -> float:
        """
        Estimate the quality of a bullet point (0.0 to 1.0)
        """
        score = 0.0
        total_weights = 0.0
        
        # Check for action verb at start (weight: 0.3)
        weight = 0.3
        doc = nlp(text)
        first_word = next(doc.__iter__()).lemma_.lower()
        if first_word in nlp.vocab and nlp.vocab[first_word].is_verb:
            score += weight
        total_weights += weight
        
        # Check for metrics (weight: 0.3)
        weight = 0.3
        if self.has_metrics(text):
            score += weight
        total_weights += weight
        
        # Check length (weight: 0.2)
        weight = 0.2
        words = len(text.split())
        if 8 <= words <= 20:  # Ideal length
            score += weight
        elif 5 <= words <= 25:  # Acceptable length
            score += weight * 0.5
        total_weights += weight
        
        # Check for technical terms (weight: 0.2)
        weight = 0.2
        keywords = self.extract_keywords(text)
        if len(keywords.get('technical', set())) > 0:
            score += weight
        total_weights += weight
        
        return score / total_weights if total_weights > 0 else 0.0

# Initialize processor
text_processor = TextProcessor()