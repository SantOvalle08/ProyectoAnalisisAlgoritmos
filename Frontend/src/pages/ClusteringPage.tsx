import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Network, Loader2, Download, Info } from 'lucide-react';
import clusteringService from '../services/clustering';

const METHODS = [
  { id: 'ward', name: 'Ward', description: 'Mínima varianza' },
  { id: 'average', name: 'Average', description: 'Distancia promedio' },
  { id: 'complete', name: 'Complete', description: 'Distancia máxima' },
];

export default function ClusteringPage() {
  const [abstracts, setAbstracts] = useState('');
  const [method, setMethod] = useState<'ward' | 'average' | 'complete'>('ward');
  const [nClusters, setNClusters] = useState<number>(3); // Valor por defecto 3
  const [autoDetect, setAutoDetect] = useState(true);
  const [labels, setLabels] = useState('');

  const clusteringMutation = useMutation({
    mutationFn: () => {
      const abstractsList = abstracts.split('\n').filter(a => a.trim());
      const labelsList = labels.trim() ? labels.split('\n').filter(l => l.trim()) : undefined;
      const requestData = {
        abstracts: abstractsList,
        method,
        num_clusters: autoDetect ? undefined : nClusters,
        labels: labelsList,
      };
      
      // Debug: Ver qué se está enviando
      console.log('=== CLUSTERING REQUEST ===', requestData);
      
      return clusteringService.performClustering(requestData);
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

  const loadDiverseExample = () => {
    setAbstracts(
      `Machine learning algorithms learn patterns from data to make predictions and decisions autonomously.
Deep learning uses neural networks with multiple layers to extract features automatically from raw data.
Natural language processing enables computers to understand and generate human language effectively.
Computer vision allows machines to interpret and understand visual information from the world.
Photosynthesis is the process by which plants convert light energy into chemical energy stored in glucose.
DNA contains the genetic instructions used in the development and functioning of all living organisms.
Cell division is the process by which a parent cell divides into daughter cells for growth and reproduction.
Mitosis and meiosis are two types of cell division essential for organism development and reproduction.
The French Revolution was a period of radical social and political upheaval in France from 1789 to 1799.
World War II lasted from 1939 to 1945 and was the deadliest military conflict in human history.
Ancient Rome was a civilization that began in the Italian Peninsula and became one of largest empires.
The Renaissance was a period of cultural rebirth in Europe that began in Italy during the 14th century.
Quantum mechanics describes the physical properties of nature at atomic and subatomic particle scales.
General relativity is Einstein's theory that explains gravity as the curvature of spacetime by mass.
Black holes are regions of spacetime where gravity is so strong that nothing can escape from them.`
    );
    setLabels('ML1\nML2\nML3\nML4\nBio1\nBio2\nBio3\nBio4\nHist1\nHist2\nHist3\nHist4\nPhys1\nPhys2\nPhys3');
    setNClusters(4); // 4 clusters para 4 dominios (ML, Bio, Historia, Física)
    setAutoDetect(false);
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
    if (score >= 0.25) return 'text-orange-600';
    return 'text-red-600';
  };

  const getSilhouetteBgColor = (score: number) => {
    if (score >= 0.7) return 'bg-green-50 border-green-200';
    if (score >= 0.5) return 'bg-yellow-50 border-yellow-200';
    if (score >= 0.25) return 'bg-orange-50 border-orange-200';
    return 'bg-red-50 border-red-200';
  };

  // Detectar si el clustering falló (todos en un cluster o clusters vacíos)
  const checkClusteringQuality = (labels: number[] | null) => {
    if (!labels || labels.length === 0) return { isValid: true, message: '' };
    
    const uniqueClusters = new Set(labels);
    const clusterCounts: Record<number, number> = {};
    labels.forEach(label => {
      clusterCounts[label] = (clusterCounts[label] || 0) + 1;
    });
    
    // Todos en un cluster
    if (uniqueClusters.size === 1) {
      return {
        isValid: false,
        message: `⚠️ El algoritmo "${method}" puso todos los documentos (${labels.length}) en un solo cluster, cuando solicitaste ${nClusters} clusters. Esto significa que el algoritmo no pudo encontrar diferencias suficientes. Prueba: (1) Cambiar a método "ward" (más robusto), (2) Usar diferente número de clusters, o (3) Agregar documentos de temas más diversos.`
      };
    }
    
    // Clusters muy desbalanceados (>90% en un cluster)
    const maxCount = Math.max(...Object.values(clusterCounts));
    if (maxCount > labels.length * 0.9) {
      return {
        isValid: false,
        message: `⚠️ Clustering muy desbalanceado: ${maxCount} de ${labels.length} documentos cayeron en un solo cluster (${((maxCount/labels.length)*100).toFixed(0)}%). El algoritmo "${method}" no logró separar bien tus documentos. Prueba: (1) Método "ward", (2) Ajustar número de clusters, o (3) Documentos más diversos.`
      };
    }
    
    return { isValid: true, message: '' };
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
          <div className="space-y-2">
            <div className="flex gap-3 flex-wrap">
              <button
                type="button"
                onClick={loadExample}
                className="text-sm text-blue-600 hover:text-blue-700 underline"
              >
                📚 Ejemplo básico (mismo dominio)
              </button>
              <button
                type="button"
                onClick={loadDiverseExample}
                className="text-sm text-green-600 hover:text-green-700 underline font-medium"
              >
                🎯 Ejemplo diverso (mejor score)
              </button>
            </div>
            <p className="text-xs text-gray-500">
              💡 <strong>Tip:</strong> El ejemplo diverso mezcla abstracts de ML, Biología, Historia y Física (15 docs, 4 clusters) 
              para mostrar mejor separación. Con datasets pequeños (~7-15 docs), es normal obtener Silhouette Scores bajos (0.01-0.03). 
              Para scores más altos (&gt;0.25), se necesitan 50+ documentos de dominios claramente diferentes.
            </p>
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
              <div className="text-sm text-gray-600 mb-1">Documentos Analizados</div>
              <div className="text-4xl font-bold text-blue-600">
                {clusteringMutation.data.num_documents}
              </div>
              <div className="text-xs text-gray-500 mt-2">
                Abstracts procesados
              </div>
            </div>

            <div className={`rounded-lg shadow-sm p-6 border-2 ${clusteringMutation.data.silhouette_score !== null ? getSilhouetteBgColor(clusteringMutation.data.silhouette_score) : 'bg-gray-50 border-gray-200'}`}>
              <div className="text-sm text-gray-600 mb-1">Silhouette Score</div>
              <div className={`text-4xl font-bold ${clusteringMutation.data.silhouette_score !== null ? getSilhouetteColor(clusteringMutation.data.silhouette_score) : 'text-gray-400'}`}>
                {clusteringMutation.data.silhouette_score !== null && clusteringMutation.data.silhouette_score !== undefined 
                  ? clusteringMutation.data.silhouette_score.toFixed(3) 
                  : 'N/A'}
              </div>
              <div className="text-xs text-gray-500 mt-2">
                {clusteringMutation.data.silhouette_score !== null && clusteringMutation.data.silhouette_score >= 0.7
                  ? '✅ Excelente separación entre clusters'
                  : clusteringMutation.data.silhouette_score !== null && clusteringMutation.data.silhouette_score >= 0.5
                  ? '👍 Buena separación entre clusters'
                  : clusteringMutation.data.silhouette_score !== null && clusteringMutation.data.silhouette_score >= 0.25
                  ? '⚠️ Separación moderada - Overlap visible'
                  : clusteringMutation.data.silhouette_score !== null && clusteringMutation.data.silhouette_score >= 0.0
                  ? '❗ Separación débil - Considera más docs o dominios diversos'
                  : clusteringMutation.data.cluster_labels
                  ? '⚠️ No calculable - Clustering degenerado'
                  : 'Especifica clusters para ver métrica'}
              </div>
            </div>
          </div>

          {/* Advertencia de clustering degenerado */}
          {clusteringMutation.data.cluster_labels && (() => {
            const quality = checkClusteringQuality(clusteringMutation.data.cluster_labels);
            return !quality.isValid ? (
              <div className="bg-orange-50 border-2 border-orange-300 rounded-lg p-4">
                <div className="flex items-start gap-3">
                  <Info className="w-5 h-5 text-orange-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm text-gray-900 font-bold mb-1">
                      Clustering No Efectivo
                    </p>
                    <p className="text-sm text-gray-700">
                      {quality.message}
                    </p>
                  </div>
                </div>
              </div>
            ) : null;
          })()}

          {/* Mensaje informativo si no hay asignaciones */}
          {!clusteringMutation.data.cluster_labels && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <Info className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm text-gray-900 font-medium mb-1">
                    Dendrograma Generado (Sin Asignación de Clusters)
                  </p>
                  <p className="text-sm text-gray-700">
                    El dendrograma muestra la estructura jerárquica completa de tus documentos. 
                    Para obtener asignaciones específicas de clusters y métricas de calidad, 
                    <strong> desactiva "Detectar automáticamente"</strong> y selecciona un número específico de clusters (2-10).
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Asignaciones de clusters */}
          {clusteringMutation.data.cluster_labels && (
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
                      cluster: clusteringMutation.data!.cluster_labels![idx],
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
                        <span className="text-sm text-gray-600 text-gray-900">{members.length} miembros</span>
                      </div>
                      <ul className="space-y-2">
                        {members.map((member, idx) => (
                          <li key={idx} className="text-sm">
                            <span className="font-mono font-semibold text-gray-900">{member.label}:</span>{' '}
                            <span className="text-gray-700">{member.abstract.substring(0, 100)}...</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Dendrograma */}
          {clusteringMutation.data.dendrogram_base64 && (
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Dendrograma</h2>
              <div className="flex justify-center">
                <img
                  src={`data:image/png;base64,${clusteringMutation.data.dendrogram_base64}`}
                  alt="Dendrograma"
                  className="max-w-full h-auto rounded-lg border border-gray-200"
                />
              </div>
            </div>
          )}
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
