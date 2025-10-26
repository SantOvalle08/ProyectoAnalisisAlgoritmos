import api from './api';
import type { FrequencyAnalysisRequest, FrequencyResult, ConceptAnalysisRequest, ConceptAnalysisResult } from '../types';

const frequencyService = {
  /**
   * Extract keywords from abstracts using frequency analysis
   */
  extractKeywords: async (
    request: FrequencyAnalysisRequest
  ): Promise<FrequencyResult[]> => {
    const method = request.use_tfidf ? 'tfidf' : 'frequency';
    const response = await api.post<FrequencyResult[]>('/api/v1/frequency/extract-keywords', {
      ...request,
      method,
      use_tfidf: undefined, // Remove use_tfidf as backend expects method instead
    });
    return response.data;
  },

  /**
   * Analyze concept frequencies in abstracts
   */
  analyzeConcepts: async (
    request: ConceptAnalysisRequest
  ): Promise<ConceptAnalysisResult> => {
    const response = await api.post<ConceptAnalysisResult>('/api/v1/frequency/analyze-concepts', request);
    return response.data;
  },

  /**
   * Health check
   */
  healthCheck: async (): Promise<{ status: string }> => {
    const response = await api.get('/api/v1/frequency/health');
    return response.data;
  },

  /**
   * Get predefined concepts
   */
  getPredefinedConcepts: async (): Promise<string[]> => {
    const response = await api.get('/api/v1/frequency/concepts');
    return response.data;
  },

  /**
   * Get extraction methods
   */
  getExtractionMethods: async (): Promise<string[]> => {
    const response = await api.get('/api/v1/frequency/methods');
    return response.data;
  },
};

export default frequencyService;
