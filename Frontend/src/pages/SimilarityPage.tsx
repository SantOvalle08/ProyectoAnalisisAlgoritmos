import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { GitCompare, Loader2, AlertCircle } from 'lucide-react';
import similarityService from '../services/similarity';
import type { SimilarityResult } from '../types';

const ALGORITHMS = [
  { id: 'levenshtein', name: 'Levenshtein', description: 'Distancia de edición' },
  { id: 'tfidf_cosine', name: 'TF-IDF', description: 'Similitud coseno con vectorización' },
  { id: 'jaccard', name: 'Jaccard', description: 'Coeficiente de Jaccard' },
  { id: 'ngram', name: 'N-grams', description: 'Similitud por n-gramas' },
  { id: 'sentence_bert', name: 'Sentence-BERT', description: 'Embeddings de IA' },
  { id: 'bert', name: 'BERT', description: 'Embeddings de IA con BERT' },
];

export default function SimilarityPage() {
  const [text1, setText1] = useState('');
  const [text2, setText2] = useState('');
  const [selectedAlgorithm, setSelectedAlgorithm] = useState('levenshtein');
  const [compareAllMode, setCompareAllMode] = useState(false);

  // Mutation para comparar con un algoritmo
  const compareMutation = useMutation({
    mutationFn: () =>
      similarityService.compare({
        text1,
        text2,
        algorithm: selectedAlgorithm as 'levenshtein' | 'tfidf_cosine' | 'jaccard' | 'ngram' | 'sentence_bert' | 'bert',
      }),
  });

  // Mutation para comparar con todos los algoritmos
  const compareAllMutation = useMutation({
    mutationFn: () => similarityService.compareAll(text1, text2),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (compareAllMode) {
      compareAllMutation.mutate();
    } else {
      compareMutation.mutate();
    }
  };

  const loadExample = () => {
    setText1(
      'Machine learning is a subset of artificial intelligence that focuses on the development of algorithms and statistical models.'
    );
    setText2(
      'Artificial intelligence encompasses machine learning, which involves creating algorithms and models for data analysis.'
    );
  };

  const getSimilarityColor = (similarity: number) => {
    if (similarity >= 0.8) return 'text-green-600';
    if (similarity >= 0.5) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getSimilarityBgColor = (similarity: number) => {
    if (similarity >= 0.8) return 'bg-green-100';
    if (similarity >= 0.5) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  const results = compareAllMode ? compareAllMutation.data : compareMutation.data ? [compareMutation.data] : [];
  const isLoading = compareAllMode ? compareAllMutation.isPending : compareMutation.isPending;
  const error = compareAllMode ? compareAllMutation.error : compareMutation.error;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Análisis de Similitud Textual
        </h1>
        <p className="text-gray-600">
          Compara dos textos usando algoritmos clásicos y de inteligencia artificial
        </p>
      </div>

      {/* Formulario */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Texto 1 */}
          <div>
            <label htmlFor="text1" className="block text-sm font-medium text-gray-700 mb-2">
              Texto 1
            </label>
            <textarea
              id="text1"
              value={text1}
              onChange={(e) => setText1(e.target.value)}
              rows={5}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
              placeholder="Ingresa el primer texto..."
              required
            />
          </div>

          {/* Texto 2 */}
          <div>
            <label htmlFor="text2" className="block text-sm font-medium text-gray-700 mb-2">
              Texto 2
            </label>
            <textarea
              id="text2"
              value={text2}
              onChange={(e) => setText2(e.target.value)}
              rows={5}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
              placeholder="Ingresa el segundo texto..."
              required
            />
          </div>

          {/* Botón ejemplo */}
          <button
            type="button"
            onClick={loadExample}
            className="text-sm text-blue-600 hover:text-blue-700 underline"
          >
            Cargar textos de ejemplo
          </button>

          {/* Modo de comparación */}
          <div>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={compareAllMode}
                onChange={(e) => setCompareAllMode(e.target.checked)}
                className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              <span className="text-sm font-medium text-gray-700">
                Comparar con todos los algoritmos
              </span>
            </label>
          </div>

          {/* Selección de algoritmo */}
          {!compareAllMode && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Algoritmo de Similitud
              </label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {ALGORITHMS.map((algo) => (
                  <button
                    key={algo.id}
                    type="button"
                    onClick={() => setSelectedAlgorithm(algo.id)}
                    className={`
                      p-4 rounded-lg border-2 transition-all text-left
                      ${
                        selectedAlgorithm === algo.id
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 bg-white hover:border-gray-300'
                      }
                    `}
                  >
                    <div className="font-semibold text-gray-900">{algo.name}</div>
                    <div className="text-xs text-gray-600 mt-1">{algo.description}</div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Botón de comparación */}
          <button
            type="submit"
            disabled={isLoading || !text1 || !text2}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Analizando...
              </>
            ) : (
              <>
                <GitCompare className="w-5 h-5" />
                {compareAllMode ? 'Comparar con Todos' : 'Comparar Textos'}
              </>
            )}
          </button>
        </form>
      </div>

      {/* Resultados */}
      {results && results.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Resultados</h2>
          
          <div className="space-y-4">
            {results.map((result: SimilarityResult, index: number) => (
              <div
                key={index}
                className={`p-4 rounded-lg border-2 ${getSimilarityBgColor(result.similarity)} border-gray-200`}
              >
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-semibold text-gray-900 capitalize">
                    {result.algorithm.replace('_', '-')}
                  </h3>
                  <div className="flex items-center gap-3">
                    <span className="text-sm text-gray-600">
                      {result.execution_time ? result.execution_time.toFixed(3) : '0.000'}s
                    </span>
                    <span className={`text-2xl font-bold ${getSimilarityColor(result.similarity)}`}>
                      {result.similarity !== undefined && result.similarity !== null ? (result.similarity * 100).toFixed(1) : '0.0'}%
                    </span>
                  </div>
                </div>

                {result.distance !== undefined && (
                  <div className="text-sm text-gray-600">
                    Distancia: <span className="font-mono font-semibold">{result.distance}</span>
                  </div>
                )}

                {result.details && Object.keys(result.details).length > 0 && (
                  <details className="mt-3">
                    <summary className="text-sm text-blue-600 cursor-pointer hover:text-blue-700">
                      Ver detalles técnicos
                    </summary>
                    <pre className="mt-2 text-xs bg-gray-50 p-3 rounded overflow-x-auto">
                      {JSON.stringify(result.details, null, 2)}
                    </pre>
                  </details>
                )}
              </div>
            ))}
          </div>

          {/* Interpretación */}
          {compareAllMode && results.length > 1 && (
            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex items-start gap-2">
                <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <div className="text-sm text-blue-800">
                  <p className="font-semibold mb-1">Interpretación:</p>
                  <p>
                    Los diferentes algoritmos pueden dar resultados variados debido a sus enfoques distintos.
                    Levenshtein mide ediciones, TF-IDF y Word2Vec capturan significado semántico,
                    mientras que Jaccard y N-grams se enfocan en tokens compartidos.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm text-red-800">
            Error al comparar textos. Por favor, intenta de nuevo.
          </p>
        </div>
      )}
    </div>
  );
}
