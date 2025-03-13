  export interface Keywords {
    technical: string[];
    soft: string[];
  }
  
  export interface AnalysisResult {
    ats_score: number;
    missing_keywords: {
      technical: string[];
      soft: string[];
    };
    matched_keywords: {
      technical: string[];
      soft: string[];
    };
    section_scores: Record<string, number>;
    improvement_suggestions: Record<string, string[]>;
  }
  
  export interface OptimizationResponse {
    optimizedContent: string;
    addedKeywords: string[];
    confidenceScore: number;
  }
  
  export interface ResumeSection {
    title: string;
    content: string;
  }
  
  export interface Resume {
    sections: ResumeSection[];
    rawText: string;
  }
  
  export interface FileUploadProps {
    onFileSelect: (file: File) => void;
    isLoading: boolean;
  }
  
  export interface JobDescriptionProps {
    value: string;
    onChange: (value: string) => void;
    isLoading: boolean;
  }
  
  export interface KeywordDisplayProps {
    keywords: AnalysisResult;  // Pass the entire analysis result
    atsScore: number | null;
  }
  
  export interface OptimizationSectionProps {
    sections: ResumeSection[];
    onOptimize: (sectionTitle: string) => void;
    optimizedPoints: string[];
    isLoading: boolean;
  }