"use client";
import React, { useState, useCallback } from 'react';
import { AlertCircle } from 'lucide-react';
import FileUpload from './FileUpload';
import JobDescription from './JobDescription';
import KeywordDisplay from './KeywordDisplay';
import OptimizationSection from './OptimizationSection';
import { ApiService } from '../services/api';
import { Resume, AnalysisResult, Keywords } from '../types';
import { debounce } from '../utils/helpers';

const ResumeOptimizer: React.FC = () => {
  // State management
  const [resume, setResume] = useState<Resume | null>(null);
  const [jobDescription, setJobDescription] = useState('');
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [optimizedPoints, setOptimizedPoints] = useState<string[]>([]);
  const [loading, setLoading] = useState({
    upload: false,
    analysis: false,
    optimization: false
  });
  const [error, setError] = useState('');

  // Handle file upload
  const handleFileSelect = useCallback(async (file: File) => {
    setError('');
    setLoading(prev => ({ ...prev, upload: true }));

    try {
      const uploadedResume = await ApiService.uploadResume(file);
      setResume(uploadedResume);
    } catch (err) {
      setError('Error uploading resume. Please try again.');
      console.error('Upload error:', err);
    } finally {
      setLoading(prev => ({ ...prev, upload: false }));
    }
  }, []);

  // Handle job description analysis
  const handleAnalysis = useCallback(async () => {
    if (!resume || !jobDescription.trim()) return;
  
    setError('');
    setLoading(prev => ({ ...prev, analysis: true }));
  
    try {
      const result = await ApiService.analyzeResume(jobDescription, resume);
      console.log("API Response:", JSON.stringify(result, null, 2));
      setAnalysisResult(result);
    } catch (err) {
      setError('Error analyzing resume. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(prev => ({ ...prev, analysis: false }));
    }
  }, [resume, jobDescription]);

  // Handle section optimization
  const handleOptimization = async (sectionTitle: string) => {
    if (!resume) return;

    setError('');
    setLoading(prev => ({ ...prev, optimization: true }));

    try {
      const section = resume.sections.find(s => s.title === sectionTitle);
      if (!section) throw new Error('Section not found');

      const keywordsToAdd = [
        ...(analysisResult?.missing_keywords.technical || []),
        ...(analysisResult?.missing_keywords.soft || [])
      ];

      const result = await ApiService.optimizeSection(
        sectionTitle,
        section.content,
        keywordsToAdd
      );

      setOptimizedPoints(result.optimizedContent.split('\n'));
    } catch (err) {
      setError('Error optimizing section. Please try again.');
      console.error('Optimization error:', err);
    } finally {
      setLoading(prev => ({ ...prev, optimization: false }));
    }
  };

  return (
    <div className="w-full max-w-7xl mx-auto p-4 space-y-6">
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h1 className="text-2xl font-bold mb-6">Resume Optimizer</h1>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center">
            <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
            <span className="text-red-600">{error}</span>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column - Input */}
          <div className="space-y-6">
            <FileUpload 
              onFileSelect={handleFileSelect}
              isLoading={loading.upload}
            />

            <JobDescription
              value={jobDescription}
              onChange={(value) => {
                setJobDescription(value);
                handleAnalysis();
              }}
              isLoading={loading.analysis}
            />

            <button 
              className={`w-full mt-4 px-4 py-2 rounded-lg text-white font-medium
                ${!resume || !jobDescription.trim() || loading.analysis 
                  ? 'bg-gray-300 cursor-not-allowed' 
                  : 'bg-blue-500 hover:bg-blue-600'
                }`}
              onClick={() => handleAnalysis()}
              disabled={!resume || !jobDescription.trim() || loading.analysis}
            >
              {loading.analysis ? 'Analyzing...' : 'Analyze Resume'}
            </button>
          </div>

          {/* Right Column - Results */}
          <div className="space-y-6">
            {analysisResult && (
              <>
                <KeywordDisplay
                  keywords={analysisResult}  // Pass the entire analysis result
                  atsScore={analysisResult.ats_score}
                />

                <OptimizationSection
                  sections={resume?.sections || []}
                  onOptimize={handleOptimization}
                  optimizedPoints={optimizedPoints}
                  isLoading={loading.optimization}
                />
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResumeOptimizer;