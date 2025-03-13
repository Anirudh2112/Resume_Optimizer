"use client";

import React from 'react';
import { KeywordDisplayProps } from '../types';
import { calculateATSColor } from '../utils/helpers';

const KeywordDisplay: React.FC<KeywordDisplayProps> = ({ keywords, atsScore }) => {
  const missingTechnical = keywords?.missing_keywords?.technical || [];
  const missingSoft = keywords?.missing_keywords?.soft || [];
  const matchedTechnical = keywords?.matched_keywords?.technical || [];
  const matchedSoft = keywords?.matched_keywords?.soft || [];

  return (
    <div className="space-y-4">
      {/* ATS Score */}
      {atsScore !== null && (
        <div className="p-4 border rounded-lg bg-white">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-lg">ATS Score</h3>
            <span className={`text-2xl font-bold ${calculateATSColor(atsScore)}`}>
              {atsScore}%
            </span>
          </div>
          
          <div className="mt-2">
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div 
                className={`h-2.5 rounded-full ${atsScore >= 80 ? 'bg-green-500' : atsScore >= 60 ? 'bg-yellow-500' : 'bg-red-500'}`}
                style={{ width: `${atsScore}%` }}
              />
            </div>
          </div>
        </div>
      )}

      {/* Technical Keywords */}
      <div className="p-4 border rounded-lg bg-white">
        <h3 className="font-bold text-lg mb-3">Technical Keywords</h3>
        
        {/* Matched keywords */}
        <div className="mb-3">
          <h4 className="font-medium text-md mb-2">Matched:</h4>
          <div className="flex flex-wrap gap-2">
            {matchedTechnical.map((keyword, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm font-medium"
              >
                {keyword}
              </span>
            ))}
            {matchedTechnical.length === 0 && (
              <span className="text-gray-500 text-sm">
                No matched technical keywords
              </span>
            )}
          </div>
        </div>
        
        {/* Missing keywords */}
        <div>
          <h4 className="font-medium text-md mb-2">Missing:</h4>
          <div className="flex flex-wrap gap-2">
            {missingTechnical.map((keyword, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-medium"
              >
                {keyword}
              </span>
            ))}
            {missingTechnical.length === 0 && (
              <span className="text-gray-500 text-sm">
                No missing technical keywords
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Soft Skills */}
      <div className="p-4 border rounded-lg bg-white">
        <h3 className="font-bold text-lg mb-3">Soft Skills</h3>
        
        {/* Matched skills */}
        <div className="mb-3">
          <h4 className="font-medium text-md mb-2">Matched:</h4>
          <div className="flex flex-wrap gap-2">
            {matchedSoft.map((keyword, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm font-medium"
              >
                {keyword}
              </span>
            ))}
            {matchedSoft.length === 0 && (
              <span className="text-gray-500 text-sm">
                No matched soft skills
              </span>
            )}
          </div>
        </div>
        
        {/* Missing skills */}
        <div>
          <h4 className="font-medium text-md mb-2">Missing:</h4>
          <div className="flex flex-wrap gap-2">
            {missingSoft.map((keyword, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-red-50 text-red-700 rounded-full text-sm font-medium"
              >
                {keyword}
              </span>
            ))}
            {missingSoft.length === 0 && (
              <span className="text-gray-500 text-sm">
                No missing soft skills
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Recommendations */}
      {(missingTechnical.length > 0 || missingSoft.length > 0) && (
        <div className="p-4 border rounded-lg bg-white">
          <h3 className="font-bold text-lg mb-3">Recommendations</h3>
          <ul className="list-disc list-inside space-y-2 text-gray-700">
            {missingTechnical.length > 0 && (
              <li>
                Consider incorporating these technical skills into your relevant experience sections
              </li>
            )}
            {missingSoft.length > 0 && (
              <li>
                Try to demonstrate these soft skills through specific achievements in your experience
              </li>
            )}
            <li>
              Ensure keywords are used naturally and in context
            </li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default KeywordDisplay;