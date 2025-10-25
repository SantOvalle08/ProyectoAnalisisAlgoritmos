import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Network, Loader2, Download } from 'lucide-react';
import clusteringService from '../services/clustering';

const METHODS = [
  { id: 'ward', name: 'Ward', description: 'Mínima varianza' },
  { id: 'average', name: 'Average', description: 'Distancia promedio' },
  { id: 'complete', name: 'Complete', description: 'Distancia máxima' },
];

export default function ClusteringPage() {
  const [abstracts, setAbstracts] = useState('');
  const [method, setMethod] = useState<'ward' | 'average' | 'complete'>('ward');
  const [nClusters, setNClusters] = useState<number | undefined>(undefined);
  const [autoDetect, setAutoDetect] = useState(true);
  const [labels, setLabels] = useState('');

  const clusteringMutation = useMutation({
    mutationFn: () => {
      const abstractsList = abstracts.split('\n').filter(a => a.trim());
      const labelsList = labels.trim() ? labels.split('\n').filter(l => l.trim()) : undefined;
      return clusteringService.performClustering({
        abstracts: abstractsList,
        method,
        n_clusters: autoDetect ? undefined : nClusters,
        labels: labelsList,
      });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    clusteringMutation.mutate();
  };

  const loadExample = () => {
    setAbstracts(
      `Machine learning algorithms learn patterns from data to make predictions.
Deep learning uses neural networks with multiple layers for complex tasks.
Natural language processing enables computers to understand human language.
Computer vision allows machines to interpret visual information.
Reinforcement learning trains agents through rewards and penalties.
Supervised learning requires labeled data for training models.
Unsupervised learning finds hidden patterns in unlabeled data.`
    );
    setLabels('ML Basics\nDeep Learning\nNLP\nComputer Vision\nRL\nSupervised\nUnsupervised');
  };

  const downloadResults = () => {
    if (!clusteringMutation.data) return;

    const json = JSON.stringify(clusteringMutation.data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'clustering_results.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  const getSilhouetteColor = (score: number) => {
    if (score >= 0.7) return 'text-green-600';
    if (score >= 0.5) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getSilhouetteBgColor = (score: number) => {
    if (score >= 0.7) return 'bg-green-50 border-green-200';
    if (score >= 0.5) return 'bg-yellow-50 border-yellow-200';
    return 'bg-red-50 border-red-200';
  };

  const abstractsList = abstracts.split('\n').filter(a => a.trim());
  const labelsList = labels.trim() ? labels.split('\n').filter(l => l.trim()) : [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Análisis de Clustering Jerárquico
        </h1>
        <p className="text-gray-600">
          Agrupa abstracts similares usando algoritmos de clustering jerárquico
        </p>
      </div>

      {/* Formulario */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Abstracts */}
          <div>
            <label htmlFor="abstracts" className="block text-sm font-medium text-gray-700 mb-2">
              Abstracts (uno por línea)
            </label>
            <textarea
              id="abstracts"
              value={abstracts}
              onChange={(e) => setAbstracts(e.target.value)}
              rows={10}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
              placeholder="Ingresa los abstracts, uno por línea..."
              required
            />
            <p className="text-sm text-gray-500 mt-1">
              {abstractsList.length} abstracts ingresados
            </p>
          </div>

          {/* Labels opcionales */}
          <div>
            <label htmlFor="labels" className="block text-sm font-medium text-gray-700 mb-2">
              Etiquetas (opcional, una por línea)
            </label>
            <textarea
              id="labels"
              value={labels}
              onChange={(e) => setLabels(e.target.value)}
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
              placeholder="Label 1&#10;Label 2&#10;Label 3"
            />
            <p className="text-sm text-gray-500 mt-1">
              {labelsList.length} etiquetas ingresadas
            </p>
          </div>

          {/* Método */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Método de Linkage
            </label>
            <div className="grid grid-cols-3 gap-3">
              {METHODS.map((m) => (
                <button
                  key={m.id}
                  type="button"
                  onClick={() => setMethod(m.id as 'ward' | 'average' | 'complete')}
                  className={`
                    p-4 rounded-lg border-2 transition-all text-left
                    ${
                      method === m.id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 bg-white hover:border-gray-300'
                    }
                  `}
                >
                  <div className="font-semibold text-gray-900">{m.name}</div>
                  <div className="text-xs text-gray-600 mt-1">{m.description}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Número de clusters */}
          <div>
            <label className="flex items-center gap-2 cursor-pointer mb-3">
              <input
                type="checkbox"
                checked={autoDetect}
                onChange={(e) => setAutoDetect(e.target.checked)}
                className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              <span className="text-sm font-medium text-gray-700">
                Detectar automáticamente el número óptimo de clusters
              </span>
            </label>

            {!autoDetect && (
              <div>
                <label htmlFor="nClusters" className="block text-sm font-medium text-gray-700 mb-2">
                  Número de clusters: {nClusters || 3}
                </label>
                <input
                  type="range"
                  id="nClusters"
                  min="2"
                  max="10"
                  value={nClusters || 3}
                  onChange={(e) => setNClusters(Number(e.target.value))}
                  className="w-full"
                />
              </div>
            )}
          </div>

          {/* Botones */}
          <div className="flex gap-3">
            <button
              type="button"
              onClick={loadExample}
              className="text-sm text-blue-600 hover:text-blue-700 underline"
            >
              Cargar datos de ejemplo
            </button>
          </div>

          <button
            type="submit"
            disabled={clusteringMutation.isPending || abstractsList.length < 2}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
          >
            {clusteringMutation.isPending ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Analizando...
              </>
            ) : (
              <>
                <Network className="w-5 h-5" />
                Realizar Clustering
              </>
            )}
          </button>
        </form>
      </div>

      {/* Resultados */}
      {clusteringMutation.data && (
        <div className="space-y-6">
          {/* Métricas principales */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="text-sm text-gray-600 mb-1">Número de Clusters</div>
              <div className="text-4xl font-bold text-blue-600">
                {clusteringMutation.data.num_clusters}
              </div>
            </div>

            <div className={`rounded-lg shadow-sm p-6 border-2 ${getSilhouetteBgColor(clusteringMutation.data.silhouette_score)}`}>
              <div className="text-sm text-gray-600 mb-1">Silhouette Score</div>
              <div className={`text-4xl font-bold ${getSilhouetteColor(clusteringMutation.data.silhouette_score)}`}>
                {clusteringMutation.data.silhouette_score.toFixed(3)}
              </div>
              <div className="text-xs text-gray-500 mt-2">
                {clusteringMutation.data.silhouette_score >= 0.7
                  ? 'Excelente separación'
                  : clusteringMutation.data.silhouette_score >= 0.5
                  ? 'Buena separación'
                  : 'Separación moderada'}
              </div>
            </div>
          </div>

          {/* Asignaciones de clusters */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Asignación de Clusters</h2>
              <button
                onClick={downloadResults}
                className="flex items-center gap-2 px-4 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <Download className="w-4 h-4" />
                Descargar JSON
              </button>
            </div>

            <div className="space-y-4">
              {Array.from({ length: clusteringMutation.data.num_clusters }, (_, i) => i).map((clusterId) => {
                const members = abstractsList
                  .map((abstract, idx) => ({
                    abstract,
                    label: labelsList[idx] || `Doc ${idx + 1}`,
                    cluster: clusteringMutation.data!.clusters[idx],
                  }))
                  .filter((item) => item.cluster === clusterId);

                const colors = ['bg-blue-100', 'bg-green-100', 'bg-purple-100', 'bg-yellow-100', 'bg-pink-100', 'bg-indigo-100'];
                const textColors = ['text-blue-800', 'text-green-800', 'text-purple-800', 'text-yellow-800', 'text-pink-800', 'text-indigo-800'];

                return (
                  <div key={clusterId} className={`p-4 rounded-lg border-2 ${colors[clusterId % colors.length]}`}>
                    <div className="flex items-center justify-between mb-3">
                      <h3 className={`font-semibold ${textColors[clusterId % textColors.length]}`}>
                        Cluster {clusterId + 1}
                      </h3>
                      <span className="text-sm text-gray-600">{members.length} miembros</span>
                    </div>
                    <ul className="space-y-2">
                      {members.map((member, idx) => (
                        <li key={idx} className="text-sm">
                          <span className="font-mono font-semibold">{member.label}:</span>{' '}
                          <span className="text-gray-700">{member.abstract.substring(0, 100)}...</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Error */}
      {clusteringMutation.error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm text-red-800">
            Error al realizar clustering. Por favor, intenta de nuevo.
          </p>
        </div>
      )}
    </div>
  );
}
