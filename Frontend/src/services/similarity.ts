import api from './api';
import type { SimilarityRequest, SimilarityResult, BatchSimilarityRequest } from '../types';

export const similarityService = {
  // Comparar dos textos con un algoritmo específico
  async compare(request: SimilarityRequest): Promise<SimilarityResult> {
    const response = await api.post('/api/v1/similarity/compare', request);
    return response.data;
  },

  // Comparar dos textos con todos los algoritmos
  async compareAll(text1: string, text2: string): Promise<SimilarityResult[]> {
    const response = await api.post('/api/v1/similarity/compare-all', {
      text1,
      text2,
    });
    return response.data;
  },

  // Analizar un par de textos con detalles
  async analyze(request: SimilarityRequest): Promise<SimilarityResult> {
    const response = await api.post('/api/v1/similarity/analyze', request);
    return response.data;
  },

  // Comparar múltiples pares en batch
  async batch(request: BatchSimilarityRequest): Promise<SimilarityResult[]> {
    const response = await api.post('/api/v1/similarity/batch', request);
    return response.data;
  },

  // Listar algoritmos disponibles
  async listAlgorithms(): Promise<string[]> {
    const response = await api.get('/api/v1/similarity/algorithms');
    return response.data;
  },

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await api.get('/api/v1/similarity/health');
    return response.data;
  },
};

export default similarityService;
