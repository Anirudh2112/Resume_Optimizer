from fastapi import UploadFile
from ..models import Resume, ResumeSection
import docx2txt
from pdf2image import convert_from_bytes
import pytesseract
import io
import re
import logging
import fitz

logger = logging.getLogger(__name__)

async def process_resume_file(file: UploadFile) -> Resume:
    """
    Process uploaded resume file and extract text content with section parsing
    """
    content = await file.read()
    
    if file.filename.endswith('.pdf'):
        raw_text = extract_from_pdf(content)
    elif file.filename.endswith('.docx'):
        raw_text = extract_from_docx(content)
    else:
        raise ValueError("Unsupported file format")

    # Parse sections from raw text
    sections = parse_resume_sections(raw_text)
    
    return Resume(
        sections=sections,
        raw_text=raw_text
    )

def extract_from_pdf(content: bytes) -> str:
    """
    Extract text from PDF file using PyMuPDF
    """
    try:
        # Open PDF from memory buffer
        with fitz.open(stream=content, filetype="pdf") as pdf:
            text = ""
            # Extract text from each page
            for page in pdf:
                text += page.get_text()
            return text
    
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise

def extract_from_docx(content: bytes) -> str:
    """
    Extract text from DOCX file
    """
    try:
        return docx2txt.process(io.BytesIO(content))
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {str(e)}")
        raise

def parse_resume_sections(text: str) -> list[ResumeSection]:
    """
    Parse resume into sections based on common section headers
    """
    # Common section headers in resumes
    section_headers = [
        "EDUCATION",
        "EXPERIENCE",
        "WORK EXPERIENCE",
        "SKILLS",
        "TECHNICAL SKILLS",
        "PROJECTS",
        "CERTIFICATIONS",
        "AWARDS",
        "PROFESSIONAL SUMMARY",
        "OBJECTIVE"
    ]
    
    # Create regex pattern for finding sections
    pattern = f"({'|'.join(section_headers)})[:\\s]*"
    
    # Split text into sections
    sections = []
    current_section = ""
    current_content = []
    
    for line in text.split('\n'):
        # Check if line is a section header
        if re.match(pattern, line.strip().upper()):
            # Save previous section if it exists
            if current_section and current_content:
                sections.append(ResumeSection(
                    title=current_section,
                    content='\n'.join(current_content).strip()
                ))
            
            # Start new section
            current_section = line.strip()
            current_content = []
        else:
            current_content.append(line)
    
    # Add final section
    if current_section and current_content:
        sections.append(ResumeSection(
            title=current_section,
            content='\n'.join(current_content).strip()
        ))
    
    return sections