from ..models import OptimizationResponse
from typing import List, Dict
import spacy
from transformers import pipeline
import re
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize text generation model
generator = pipeline("text2text-generation", model="google/flan-t5-base")

class ResumeOptimizer:
    def __init__(self):
        self.action_verbs = [
            "achieved", "improved", "developed", "led", "managed", "created",
            "implemented", "designed", "analyzed", "collaborated", "initiated",
            "launched", "optimized", "reduced", "increased", "streamlined"
        ]
        
    def optimize_resume_section(self, current_content: str, selected_keywords: List[str]) -> OptimizationResponse:
        """
        Optimize resume section content by incorporating selected keywords
        """
        try:
            # Split content into bullet points
            bullet_points = [p.strip() for p in current_content.split('\n') if p.strip()]
            
            optimized_points = []
            added_keywords = set()
            total_confidence = 0
            
            for point in bullet_points:
                # Check which keywords are missing from this point
                missing_kw = [kw for kw in selected_keywords 
                             if not re.search(rf'\b{re.escape(kw)}\b', point, re.IGNORECASE)]
                
                if missing_kw:
                    # Generate optimized version of the point
                    new_point = self._optimize_bullet_point(point, missing_kw)
                    optimized_points.append(new_point)
                    
                    # Track which keywords were successfully added
                    for kw in missing_kw:
                        if re.search(rf'\b{re.escape(kw)}\b', new_point, re.IGNORECASE):
                            added_keywords.add(kw)
                else:
                    optimized_points.append(point)
                
                # Calculate confidence score for this point
                total_confidence += self._calculate_confidence_score(point, selected_keywords)
            
            # Calculate overall confidence score
            avg_confidence = total_confidence / len(bullet_points) if bullet_points else 0
            
            return OptimizationResponse(
                optimized_content='\n'.join(optimized_points),
                added_keywords=list(added_keywords),
                confidence_score=avg_confidence
            )
        
        except Exception as e:
            logger.error(f"Error optimizing resume section: {str(e)}")
            raise

    def _optimize_bullet_point(self, point: str, keywords: List[str]) -> str:
        """
        Optimize a single bullet point by incorporating keywords
        """
        try:
            # Extract key components
            doc = nlp(point)
            achievement = self._extract_achievement(doc)
            metrics = self._extract_metrics(point)
            
            # Prepare prompt for the model
            prompt = f"""
            Rewrite this resume bullet point to include these keywords ({', '.join(keywords)}):
            Original: {point}
            Requirements:
            - Start with a strong action verb
            - Include quantifiable metrics if present: {metrics}
            - Incorporate achievement: {achievement}
            - Naturally include these keywords
            - Keep under 20 words
            - Use active voice
            """
            
            # Generate optimized version
            response = generator(prompt, max_length=100, num_return_sequences=1)
            optimized = response[0]['generated_text'].strip()
            
            # Ensure it starts with an action verb
            if not self._starts_with_action_verb(optimized):
                optimized = self._add_action_verb(optimized)
            
            # Ensure it's not too long
            if len(optimized.split()) > 20:
                optimized = ' '.join(optimized.split()[:20])
            
            return optimized
        
        except Exception as e:
            logger.error(f"Error optimizing bullet point: {str(e)}")
            return point  # Return original if optimization fails

    def _calculate_confidence_score(self, point: str, keywords: List[str]) -> float:
        """
        Calculate confidence score for optimized bullet point
        """
        doc = nlp(point)
        
        scores = {
            'keyword_usage': self._calculate_keyword_score(point, keywords),
            'action_verb': self._calculate_action_verb_score(point),
            'metrics': self._calculate_metrics_score(point),
            'length': self._calculate_length_score(point),
            'grammar': self._calculate_grammar_score(doc)
        }
        
        # Weights for different factors
        weights = {
            'keyword_usage': 0.35,
            'action_verb': 0.20,
            'metrics': 0.20,
            'length': 0.15,
            'grammar': 0.10
        }
        
        # Calculate weighted score
        final_score = sum(score * weights[factor] for factor, score in scores.items())
        
        return min(final_score, 1.0)  # Cap at 1.0

    def _extract_achievement(self, doc: spacy.tokens.Doc) -> str:
        """
        Extract the main achievement or responsibility from the bullet point
        """
        # Look for result clauses (often after "resulting in", "leading to", etc.)
        achievement = ""
        for token in doc:
            if token.text.lower() in ["achieved", "resulting", "led", "improved"]:
                achievement = ' '.join(t.text for t in token.rights)
                break
        
        return achievement if achievement else str(doc)

    def _extract_metrics(self, text: str) -> List[str]:
        """
        Extract quantifiable metrics from the text
        """
        # Look for numbers followed by % or other metrics
        metric_pattern = r'\d+(?:\.\d+)?%|\d+(?:\.\d+)?\s*(?:x|times|hrs?|hours?|days?|months?|years?|k|M|B|million|billion)'
        return re.findall(metric_pattern, text)

    def _starts_with_action_verb(self, text: str) -> bool:
        """
        Check if text starts with an action verb
        """
        first_word = text.strip().split()[0].lower()
        return first_word in self.action_verbs

    def _add_action_verb(self, text: str) -> str:
        """
        Add an appropriate action verb to the beginning of the text
        """
        import random
        verb = random.choice(self.action_verbs)
        return f"{verb.capitalize()} {text}"

    def _calculate_keyword_score(self, text: str, keywords: List[str]) -> float:
        """
        Calculate score based on keyword usage
        """
        if not keywords:
            return 1.0
        
        matches = sum(1 for kw in keywords 
                     if re.search(rf'\b{re.escape(kw)}\b', text, re.IGNORECASE))
        return matches / len(keywords)

    def _calculate_action_verb_score(self, text: str) -> float:
        """
        Calculate score based on action verb usage
        """
        return 1.0 if self._starts_with_action_verb(text) else 0.0

    def _calculate_metrics_score(self, text: str) -> float:
        """
        Calculate score based on presence of metrics
        """
        metrics = self._extract_metrics(text)
        return min(len(metrics) / 2, 1.0)  # Cap at 1.0

    def _calculate_length_score(self, text: str) -> float:
        """
        Calculate score based on text length
        """
        words = len(text.split())
        if 10 <= words <= 20:
            return 1.0
        elif words < 10:
            return words / 10
        else:
            return max(0, 1 - (words - 20) / 10)

    def _calculate_grammar_score(self, doc: spacy.tokens.Doc) -> float:
        """
        Calculate score based on grammar and structure
        """
        # Basic checks for sentence structure
        has_verb = any(token.pos_ == "VERB" for token in doc)
        has_subject = any(token.dep_ == "nsubj" for token in doc)
        
        if has_verb and has_subject:
            return 1.0
        elif has_verb or has_subject:
            return 0.5
        return 0.0

# Initialize the optimizer
optimizer = ResumeOptimizer()