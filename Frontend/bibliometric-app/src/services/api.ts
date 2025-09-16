// Servicios para comunicación con la API del backend

import axios from 'axios'
import type { AxiosResponse } from 'axios'
import type { 
  ApiResponse, 
  PaginatedResponse, 
  ResearchPaper, 
  AnalysisResult, 
  SearchFilters,
  BiblioMetrics 
} from '../types'

// Configuración base de axios
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptores para manejo de errores
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: unknown) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// Servicios de búsqueda y análisis
export class BiblioMetricService {
  // Búsqueda de papers
  static async searchPapers(
    filters: SearchFilters,
    page = 1,
    limit = 20
  ): Promise<PaginatedResponse<ResearchPaper>> {
    const response: AxiosResponse<ApiResponse<PaginatedResponse<ResearchPaper>>> = 
      await apiClient.post('/api/v1/search/papers', {
        filters,
        page,
        limit
      })
    return response.data.data
  }

  // Análisis bibliométrico completo
  static async performAnalysis(filters: SearchFilters): Promise<AnalysisResult> {
    const response: AxiosResponse<ApiResponse<AnalysisResult>> = 
      await apiClient.post('/api/v1/analysis/bibliometric', { filters })
    return response.data.data
  }

  // Obtener métricas básicas
  static async getMetrics(papersIds: string[]): Promise<BiblioMetrics> {
    const response: AxiosResponse<ApiResponse<BiblioMetrics>> = 
      await apiClient.post('/api/v1/metrics/calculate', { papersIds })
    return response.data.data
  }

  // Análisis de similaridad
  static async calculateSimilarity(papersIds: string[]): Promise<number[][]> {
    const response: AxiosResponse<ApiResponse<number[][]>> = 
      await apiClient.post('/api/v1/analysis/similarity', { papersIds })
    return response.data.data
  }

  // Clustering de papers
  static async clusterPapers(
    papersIds: string[], 
    algorithm = 'kmeans', 
    numClusters = 5
  ): Promise<AnalysisResult['clusters']> {
    const response: AxiosResponse<ApiResponse<AnalysisResult['clusters']>> = 
      await apiClient.post('/api/v1/analysis/clustering', {
        papersIds,
        algorithm,
        numClusters
      })
    return response.data.data
  }

  // Health check
  static async healthCheck(): Promise<{ status: string; timestamp: string }> {
    const response: AxiosResponse<{ status: string; timestamp: string }> = 
      await apiClient.get('/health')
    return response.data
  }
}

// Servicio para manejo de datos externos (APIs académicas)
export class ExternalDataService {
  // Importar desde fuentes externas
  static async importFromSource(
    source: 'scopus' | 'pubmed' | 'arxiv',
    query: string,
    maxResults = 100
  ): Promise<ResearchPaper[]> {
    const response: AxiosResponse<ApiResponse<ResearchPaper[]>> = 
      await apiClient.post('/api/v1/import/external', {
        source,
        query,
        maxResults
      })
    return response.data.data
  }

  // Verificar disponibilidad de APIs externas
  static async checkExternalAPIs(): Promise<Record<string, boolean>> {
    const response: AxiosResponse<ApiResponse<Record<string, boolean>>> = 
      await apiClient.get('/api/v1/external/status')
    return response.data.data
  }
}

export default { BiblioMetricService, ExternalDataService }