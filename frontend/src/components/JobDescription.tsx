"use client";
import React from 'react';
import { JobDescriptionProps } from '../types';

const JobDescription: React.FC<JobDescriptionProps> = ({ 
  value, 
  onChange, 
  isLoading 
}) => {
  return (
    <div className="w-full space-y-2">
      <label 
        htmlFor="jobDescription" 
        className="block text-sm font-medium text-gray-700"
      >
        Job Description
      </label>
      
      <textarea
        id="jobDescription"
        className={`w-full h-48 p-3 border rounded-lg resize-none
          focus:ring-2 focus:ring-blue-500 focus:border-blue-500
          ${isLoading ? 'bg-gray-50 cursor-not-allowed' : 'bg-white'}
          ${value ? '' : 'placeholder-gray-400'}`}
        placeholder="Paste the job description here..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={isLoading}
      />
      
      {isLoading && (
        <p className="text-sm text-blue-500">
          Analyzing job description...
        </p>
      )}
      
      {!isLoading && value && (
        <p className="text-sm text-gray-500">
          Characters: {value.length}
        </p>
      )}
    </div>
  );
};

export default JobDescription;