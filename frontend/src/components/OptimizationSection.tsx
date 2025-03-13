"use client";
import React, { useState } from 'react';
import { Check, Loader } from 'lucide-react';
import { OptimizationSectionProps } from '../types';

const OptimizationSection: React.FC<OptimizationSectionProps> = ({
  sections,
  onOptimize,
  optimizedPoints,
  isLoading
}) => {
  const [selectedSection, setSelectedSection] = useState('');

  const handleOptimize = () => {
    if (selectedSection) {
      onOptimize(selectedSection);
    }
  };

  return (
    <div className="space-y-4">
      <div className="p-4 border rounded-lg bg-white">
        <h3 className="font-bold text-lg mb-4">Optimize Section</h3>
        
        {/* Section Selection */}
        <div className="space-y-2">
          <label 
            htmlFor="section-select" 
            className="block text-sm font-medium text-gray-700"
          >
            Select section to optimize
          </label>
          <select
            id="section-select"
            className="w-full p-2 border rounded-lg bg-white"
            value={selectedSection}
            onChange={(e) => setSelectedSection(e.target.value)}
            disabled={isLoading}
          >
            <option value="">Choose a section...</option>
            {sections.map((section, index) => (
              <option key={index} value={section.title}>
                {section.title}
              </option>
            ))}
          </select>
        </div>

        {/* Optimize Button */}
        <button
          className={`mt-4 w-full px-4 py-2 rounded-lg text-white font-medium
            ${isLoading 
              ? 'bg-blue-400 cursor-not-allowed' 
              : selectedSection 
                ? 'bg-blue-500 hover:bg-blue-600' 
                : 'bg-gray-300 cursor-not-allowed'
            }`}
          onClick={handleOptimize}
          disabled={isLoading || !selectedSection}
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <Loader className="w-5 h-5 mr-2 animate-spin" />
              Optimizing...
            </span>
          ) : (
            'Optimize Section'
          )}
        </button>
      </div>

      {/* Optimized Content */}
      {optimizedPoints.length > 0 && (
        <div className="p-4 border rounded-lg bg-white">
          <h4 className="font-bold text-lg mb-3">Optimized Points:</h4>
          <div className="space-y-3">
            {optimizedPoints.map((point, index) => (
              <div key={index} className="flex items-start">
                <Check className="w-5 h-5 text-green-500 mr-2 mt-1 flex-shrink-0" />
                <p className="text-gray-700">{point}</p>
              </div>
            ))}
          </div>
          
          <div className="mt-4 text-sm text-gray-500">
            Review these optimized points and copy them to your resume as needed.
          </div>
        </div>
      )}
    </div>
  );
};

export default OptimizationSection;