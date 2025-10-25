import api from './api';
import type { ClusteringRequest, ClusteringResult } from '../types';

const clusteringService = {
  /**
   * Perform hierarchical clustering on abstracts
   */
  performClustering: async (
    request: ClusteringRequest
  ): Promise<ClusteringResult> => {
    const response = await api.post<ClusteringResult>('/api/v1/clustering/hierarchical', request);
    return response.data;
  },

  /**
   * Compare different clustering methods
   */
  compareMethods: async (request: ClusteringRequest): Promise<Record<string, ClusteringResult>> => {
    const response = await api.post('/api/v1/clustering/compare', request);
    return response.data;
  },

  /**
   * Get available methods
   */
  getMethods: async (): Promise<string[]> => {
    const response = await api.get('/api/v1/clustering/methods');
    return response.data;
  },

  /**
   * Health check
   */
  healthCheck: async (): Promise<{ status: string }> => {
    const response = await api.get('/api/v1/clustering/health');
    return response.data;
  },
};

export default clusteringService;
