import api from './api';
import type { ClusteringRequest, ClusteringResult } from '../types';

const clusteringService = {
  /**
   * Perform hierarchical clustering on abstracts
   */
  performClustering: async (
    request: ClusteringRequest
  ): Promise<ClusteringResult> => {
    const response = await api.post<ClusteringResult>('/clustering/analyze', request);
    return response.data;
  },

  /**
   * Get clustering recommendations
   */
  getRecommendations: async (abstracts: string[]): Promise<{ recommended_clusters: number; silhouette_scores: number[] }> => {
    const response = await api.post('/clustering/recommend', { abstracts });
    return response.data;
  },
};

export default clusteringService;
