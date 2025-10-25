import api from './api';
import type {
  WordCloudRequest,
  WordCloudResult,
  HeatmapRequest,
  HeatmapResult,
  TimelineRequest,
  TimelineResult,
  PDFExportRequest,
} from '../types';

export const visualizationService = {
  // Generar word cloud
  async generateWordCloud(request: WordCloudRequest): Promise<WordCloudResult> {
    const response = await api.post('/api/v1/visualizations/wordcloud', request);
    return response.data;
  },

  // Generar heatmap geográfico
  async generateHeatmap(request: HeatmapRequest): Promise<HeatmapResult> {
    const response = await api.post('/api/v1/visualizations/heatmap', request);
    return response.data;
  },

  // Generar línea temporal
  async generateTimeline(request: TimelineRequest): Promise<TimelineResult> {
    const response = await api.post('/api/v1/visualizations/timeline', request);
    return response.data;
  },

  // Exportar visualizaciones a PDF
  async exportToPDF(request: PDFExportRequest): Promise<Blob> {
    const response = await api.post('/api/v1/visualizations/export-pdf', request, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await api.get('/api/v1/visualizations/health');
    return response.data;
  },
};

export default visualizationService;
