from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import *
from .services.file_processor import process_resume_file
from .services.keyword_extractor import extract_keywords, calculate_ats_score
from .services.resume_optimizer import optimizer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Resume Optimizer API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-resume", response_model=Resume)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and process a resume file (PDF or DOCX)
    """
    try:
        if not file.filename.endswith(('.pdf', '.docx')):
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Only PDF and DOCX are supported."
            )
        
        resume = await process_resume_file(file)
        return resume
    
    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze", response_model=AnalysisResult)
async def analyze_resume(job_desc: JobDescription, resume: Resume):
    """
    Analyze resume against job description
    """
    try:
        # Log what we're receiving for debugging
        logger.info(f"Received job_desc: {job_desc}")
        logger.info(f"Received resume: {resume}")
        
        # Extract keywords from job description
        keywords = extract_keywords(job_desc.text)
        
        # Calculate ATS score and analyze matches
        analysis = calculate_ats_score(resume, keywords)
        return analysis
    
    except Exception as e:
        logger.error(f"Error analyzing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize-section", response_model=OptimizationResponse)
async def optimize_section(request: OptimizationRequest):
    """
    Optimize a specific resume section with selected keywords
    """
    try:
        optimization_result = optimize_resume_section(
            request.current_content,
            request.selected_keywords
        )
        return optimization_result
    
    except Exception as e:
        logger.error(f"Error optimizing section: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)