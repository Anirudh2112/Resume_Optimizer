import axios from 'axios';
import { Resume, AnalysisResult, OptimizationResponse } from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadResume = async (file: File): Promise<Resume> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post<Resume>('/upload-resume', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

// In your services/api.ts file
export const analyzeResume = async (
  jobDescription: string,
  resume: Resume
): Promise<AnalysisResult> => {
  const response = await api.post('/analyze', {
    job_desc: { text: jobDescription },
    resume: resume
  });

  // Make sure to include matched_keywords in the transformed response
  return {
    ats_score: response.data.ats_score,
    missing_keywords: response.data.missing_keywords,
    matched_keywords: response.data.matched_keywords, // Add this line
    section_scores: response.data.section_scores,
    improvement_suggestions: response.data.improvement_suggestions
  };
};

export const optimizeSection = async (
  sectionTitle: string,
  currentContent: string,
  selectedKeywords: string[]
): Promise<OptimizationResponse> => {
  const response = await api.post<OptimizationResponse>('/optimize-section', {
    sectionTitle,
    currentContent,
    selectedKeywords,
  });

  return response.data;
};

export const ApiService = {
  uploadResume,
  analyzeResume,
  optimizeSection,
};

export default ApiService;