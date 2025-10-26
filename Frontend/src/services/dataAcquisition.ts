import api from './api';
import type { DownloadRequest, DownloadJob, Publication } from '../types';

export const dataAcquisitionService = {
  // Iniciar descarga de datos
  async startDownload(request: DownloadRequest): Promise<{ job_id: string }> {
    const response = await api.post('/api/v1/data/download', request);
    return response.data;
  },

  // Obtener estado de un trabajo
  async getJobStatus(jobId: string): Promise<DownloadJob> {
    const response = await api.get(`/api/v1/data/status/${jobId}`);
    return response.data;
  },

  // Listar todos los trabajos
  async listJobs(): Promise<DownloadJob[]> {
    const response = await api.get('/api/v1/data/jobs');
    return response.data;
  },

  // Obtener datos unificados
  async getUnifiedData(jobId?: string): Promise<Publication[]> {
    const response = await api.get('/api/v1/data/unified', {
      params: jobId ? { job_id: jobId } : undefined
    });
    return response.data;
  },

  // Obtener reporte de duplicados
  async getDuplicates(jobId: string): Promise<Record<string, unknown>> {
    const response = await api.get(`/api/v1/data/duplicates/${jobId}`);
    return response.data;
  },

  // Descargar archivo de resultados
  async downloadFile(jobId: string, format: string): Promise<Blob> {
    const response = await api.get(`/api/v1/data/download/${jobId}/${format}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Cancelar trabajo
  async cancelJob(jobId: string): Promise<void> {
    await api.delete(`/api/v1/data/cancel/${jobId}`);
  },

  // Listar fuentes disponibles
  async listSources(): Promise<string[]> {
    const response = await api.get('/api/v1/data/sources');
    // El backend retorna { sources: [{id, name, ...}, ...] }
    // Extraer solo los IDs
    if (response.data?.sources && Array.isArray(response.data.sources)) {
      return response.data.sources.map((source: { id: string }) => source.id);
    }
    return [];
  },

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await api.get('/api/v1/data/health');
    return response.data;
  },
};

export default dataAcquisitionService;
