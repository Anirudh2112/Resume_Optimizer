"use client";
import React, { useCallback, useState } from 'react';
import { Upload, FileText, AlertCircle } from 'lucide-react';
import { FileUploadProps } from '../types';
import { isValidFileType, formatFileSize } from '../utils/helpers';

const FileUpload: React.FC<FileUploadProps> = ({ onFileSelect, isLoading }) => {
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState<string>('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFile = useCallback((file: File | null) => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    if (!isValidFileType(file)) {
      setError('Invalid file type. Please upload a PDF or DOCX file');
      return;
    }

    if (file.size > 10 * 1024 * 1024) { // 10MB limit
      setError('File size too large. Please upload a file smaller than 10MB');
      return;
    }

    setError('');
    setSelectedFile(file);
    onFileSelect(file);
  }, [onFileSelect]);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragActive(false);
    const file = e.dataTransfer.files[0];
    handleFile(file);
  }, [handleFile]);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragActive(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragActive(false);
  }, []);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    handleFile(file);
  }, [handleFile]);

  return (
    <div className="w-full">
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors
          ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-500'}
          ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => !isLoading && document.getElementById('fileInput')?.click()}
      >
        <input
          id="fileInput"
          type="file"
          className="hidden"
          accept=".pdf,.docx"
          onChange={handleChange}
          disabled={isLoading}
        />
        
        <Upload className="mx-auto h-12 w-12 text-gray-400" />
        <p className="mt-2">Drop your resume here or click to upload</p>
        <p className="text-sm text-gray-500">Supports PDF and DOCX</p>

        {selectedFile && (
          <div className="mt-4 flex items-center justify-center text-green-500">
            <FileText className="h-5 w-5 mr-2" />
            <span>{selectedFile.name} ({formatFileSize(selectedFile.size)})</span>
          </div>
        )}

        {error && (
          <div className="mt-4 flex items-center justify-center text-red-500">
            <AlertCircle className="h-5 w-5 mr-2" />
            <span>{error}</span>
          </div>
        )}

        {isLoading && (
          <div className="mt-4 text-blue-500">
            Processing your resume...
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;