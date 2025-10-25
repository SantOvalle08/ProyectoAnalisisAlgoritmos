import api from './api';
import type { FrequencyAnalysisRequest, FrequencyResult, ConceptAnalysisRequest, ConceptAnalysisResult } from '../types';

const frequencyService = {
  /**
   * Extract keywords from abstracts using frequency analysis
   */
  extractKeywords: async (
    request: FrequencyAnalysisRequest
  ): Promise<FrequencyResult> => {
    const response = await api.post<FrequencyResult>('/frequency/extract', request);
    return response.data;
  },

  /**
   * Analyze concept frequencies in abstracts
   */
  analyzeConcepts: async (
    request: ConceptAnalysisRequest
  ): Promise<ConceptAnalysisResult> => {
    const response = await api.post<ConceptAnalysisResult>('/frequency/concepts', request);
    return response.data;
  },
};

export default frequencyService;
