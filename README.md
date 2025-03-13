# Resume Optimizer - ATS-Optimized

## Overview
This project implements a system to help job seekers optimize their resumes for Applicant Tracking Systems (ATS). It analyzes job descriptions, calculates ATS compatibility scores, and identifies keyword matches and gaps to improve application success rates.

⚠️ **Note:** This is a work in progress. Section optimization features are under active development.

## Current Features
- Resume upload and processing (PDF/DOCX)
- Job description keyword extraction and analysis
- ATS compatibility scoring system
- Matched and missing keyword identification
- Technical skills and soft skills categorization
- Modern, responsive web interface

## Tech Stack
- **Frontend:** Next.js, React 18, TypeScript, Tailwind CSS
- **Backend:** FastAPI, spaCy, Hugging Face Transformers
- **Document Processing:** PyMuPDF, NLP libraries
- **API Communication:** Axios, RESTful endpoints

## Running the Application

## Backend
### Activate virtual environment (Windows PowerShell)
.\env\Scripts\Activate.ps1

### Run the FastAPI server
uvicorn app.main:app --reload --port 8000

## Frontend
### Run the Next.js development server
npm run dev

## Usage Flow
- Upload your resume (PDF/DOCX format)
- Enter a job description
- Click "Analyze Resume"
- Review your ATS score and keyword analysis

## Future Updates
- Section-specific optimization suggestions
- LangChain and LangGraph integration
- Dynamic keyword extraction enhancements
- Industry-specific keyword databases
- Optimized resume export functionality
- Resume version management

## Contributions
- Contributions are welcome! Please feel free to submit issues or pull requests.


