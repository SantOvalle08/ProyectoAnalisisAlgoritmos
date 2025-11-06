import { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Download, Database, CheckCircle, XCircle, Loader2, FileDown } from 'lucide-react';
import dataAcquisitionService from '../services/dataAcquisition';
import type { DownloadRequest } from '../types';

export default function DataAcquisitionPage() {
  const [query, setQuery] = useState('generative artificial intelligence');
  const [selectedSources, setSelectedSources] = useState<string[]>(['crossref']);
  const [maxResults, setMaxResults] = useState(50);
  const [currentJobId, setCurrentJobId] = useState<string | null>(null);

  // Query para listar fuentes disponibles
  const { data: sourcesData } = useQuery({
    queryKey: ['sources'],
    queryFn: () => dataAcquisitionService.listSources(),
  });

  // Asegurar que sources siempre sea un array
  const sources = Array.isArray(sourcesData) ? sourcesData : [];

  // Query para obtener estado del trabajo
  const { data: jobStatus } = useQuery({
    queryKey: ['jobStatus', currentJobId],
    queryFn: () => {
      if (!currentJobId) {
        return Promise.reject('No job ID');
      }
      return dataAcquisitionService.getJobStatus(currentJobId);
    },
    enabled: !!currentJobId && currentJobId !== null && currentJobId !== 'null',
    refetchInterval: (query) => {
      // Dejar de hacer polling si el trabajo terminó o no hay job_id
      const data = query.state.data;
      if (!currentJobId || !data || data.status === 'completed' || data.status === 'failed') {
        return false;
      }
      return 2000; // Polling cada 2 segundos
    },
    retry: 1,
  });

  // Mutation para iniciar descarga
  const downloadMutation = useMutation({
    mutationFn: (request: DownloadRequest) => dataAcquisitionService.startDownload(request),
    onSuccess: (data) => {
      console.log('Download started:', data);
      if (data && data.job_id) {
        setCurrentJobId(data.job_id);
      }
    },
    onError: (error) => {
      console.error('Download error:', error);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    downloadMutation.mutate({
      query,
      sources: selectedSources,
      max_results_per_source: maxResults,
      export_formats: ['json', 'bibtex', 'ris', 'csv'],
    });
  };

  const handleSourceToggle = (source: string) => {
    setSelectedSources((prev) =>
      prev.includes(source)
        ? prev.filter((s) => s !== source)
        : [...prev, source]
    );
  };

  const handleDownloadFile = async (format: string) => {
    if (!currentJobId) return;
    try {
      const blob = await dataAcquisitionService.downloadFile(currentJobId, format);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `publications_${currentJobId}.${format}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error al descargar archivo:', error);
    }
  };

  const getStatusIcon = () => {
    if (!jobStatus) return null;
    switch (jobStatus.status) {
      case 'completed':
        return <CheckCircle className="w-6 h-6 text-green-500" />;
      case 'failed':
        return <XCircle className="w-6 h-6 text-red-500" />;
      case 'running':
        return <Loader2 className="w-6 h-6 text-blue-500 animate-spin" />;
      default:
        return <Loader2 className="w-6 h-6 text-gray-400 animate-spin" />;
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Adquisición de Datos
        </h1>
        <p className="text-gray-600">
          Descarga y unifica publicaciones científicas de múltiples fuentes
        </p>
      </div>

      {/* Formulario de búsqueda */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Query de búsqueda */}
          <div>
            <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
              Consulta de Búsqueda
            </label>
            <input
              type="text"
              id="query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Ej: generative artificial intelligence"
              required
            />
            <p className="mt-1 text-sm text-gray-500">
              Ingresa términos de búsqueda para encontrar publicaciones científicas
            </p>
          </div>

          {/* Fuentes */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Fuentes de Datos
            </label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {sources.length === 0 ? (
                <div className="col-span-2 md:col-span-3 text-center py-8 text-gray-500">
                  <Database className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>Cargando fuentes disponibles...</p>
                </div>
              ) : (
                sources.map((source) => (
                  <button
                    key={source}
                    type="button"
                    onClick={() => handleSourceToggle(source)}
                    className={`
                      px-4 py-3 rounded-lg border-2 transition-all text-left
                      ${
                        selectedSources.includes(source)
                          ? 'border-blue-500 bg-blue-50 text-blue-700'
                          : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300'
                      }
                    `}
                  >
                    <Database className="w-5 h-5 mb-1" />
                    <div className="text-sm font-medium capitalize">{source}</div>
                  </button>
                ))
              )}
            </div>
          </div>

          {/* Resultados máximos */}
          <div>
            <label htmlFor="maxResults" className="block text-sm font-medium text-gray-700 mb-2">
              Resultados Máximos por Fuente
            </label>
            <input
              type="number"
              id="maxResults"
              value={maxResults}
              onChange={(e) => setMaxResults(parseInt(e.target.value))}
              min="1"
              max="1000"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {/* Botón de descarga */}
          <button
            type="submit"
            disabled={downloadMutation.isPending || selectedSources.length === 0}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
          >
            {downloadMutation.isPending ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Iniciando descarga...
              </>
            ) : (
              <>
                <Download className="w-5 h-5" />
                Iniciar Descarga
              </>
            )}
          </button>
        </form>
      </div>

      {/* Estado del trabajo */}
      {(currentJobId || downloadMutation.isPending) && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Estado de la Descarga</h2>
            {getStatusIcon()}
          </div>

          {!jobStatus && downloadMutation.isPending && (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="w-8 h-8 text-blue-500 animate-spin mr-3" />
              <span className="text-gray-600">Iniciando descarga...</span>
            </div>
          )}

          {jobStatus && (
            <div className="space-y-4">
              {/* Información del trabajo */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-50 p-3 rounded-lg">
                  <p className="text-xs font-medium text-gray-500 uppercase mb-1">Job ID</p>
                  <p className="font-mono text-sm font-semibold text-gray-900 break-all">{jobStatus.job_id}</p>
                </div>
                <div className="bg-gray-50 p-3 rounded-lg">
                  <p className="text-xs font-medium text-gray-500 uppercase mb-1">Estado</p>
                  <p className="text-sm font-bold text-gray-900 capitalize">{jobStatus.status}</p>
                </div>
                <div className="bg-gray-50 p-3 rounded-lg">
                  <p className="text-xs font-medium text-gray-500 uppercase mb-1">Progreso</p>
                  <p className="text-sm font-bold text-gray-900">{jobStatus.progress}%</p>
                </div>
                <div className="bg-gray-50 p-3 rounded-lg">
                  <p className="text-xs font-medium text-gray-500 uppercase mb-1">Publicaciones</p>
                  <p className="text-sm font-bold text-gray-900">{jobStatus.total_publications || 0}</p>
                </div>
              </div>

              {/* Barra de progreso */}
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-700">Progreso de descarga</span>
                  <span className="text-sm font-bold text-blue-600">{Math.round(jobStatus.progress)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3 shadow-inner">
                  <div
                    className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-500 ease-out shadow-sm"
                    style={{ width: `${jobStatus.progress}%` }}
                  />
                </div>
                {jobStatus.current_source && (
                  <p className="text-xs text-gray-600 italic">
                    Procesando: <span className="font-semibold text-gray-900">{jobStatus.current_source}</span>
                  </p>
                )}
              </div>

              {/* Mensaje */}
              {jobStatus.message && (
                <div className="bg-blue-50 border-l-4 border-blue-500 rounded-r-lg p-4">
                  <p className="text-sm text-blue-900 font-medium">{jobStatus.message}</p>
                </div>
              )}

              {/* Estadísticas detalladas (cuando está completado) */}
              {jobStatus.status === 'completed' && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h3 className="text-sm font-semibold text-green-900 mb-3 flex items-center gap-2">
                    <CheckCircle className="w-4 h-4" />
                    Descarga Completada
                  </h3>
                  <div className="grid grid-cols-3 gap-4 text-center">
                    <div>
                      <p className="text-xs text-green-700 uppercase mb-1">Total Descargado</p>
                      <p className="text-2xl font-bold text-green-900">{jobStatus.total_downloaded}</p>
                    </div>
                    <div>
                      <p className="text-xs text-green-700 uppercase mb-1">Publicaciones Únicas</p>
                      <p className="text-2xl font-bold text-green-900">{jobStatus.total_unique}</p>
                    </div>
                    <div>
                      <p className="text-xs text-green-700 uppercase mb-1">Duplicados Eliminados</p>
                      <p className="text-2xl font-bold text-orange-600">{jobStatus.total_duplicates}</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Botones de descarga */}
              {jobStatus.status === 'completed' && (
                <div>
                  <h3 className="text-sm font-medium text-gray-700 mb-3">Descargar Resultados</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    {['json', 'bibtex', 'ris', 'csv'].map((format) => (
                      <button
                        key={format}
                        onClick={() => handleDownloadFile(format)}
                        className="flex items-center justify-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors"
                      >
                        <FileDown className="w-4 h-4" />
                        <span className="text-sm font-medium uppercase">{format}</span>
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Error */}
      {downloadMutation.isError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm text-red-800">
            Error al iniciar la descarga. Por favor, intenta de nuevo.
          </p>
        </div>
      )}
    </div>
  );
}
