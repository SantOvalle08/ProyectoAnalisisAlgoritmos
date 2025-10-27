import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { BarChart3, Loader2, Download } from 'lucide-react';
import frequencyService from '../services/frequency';

export default function FrequencyPage() {
  const [abstracts, setAbstracts] = useState('');
  const [maxKeywords, setMaxKeywords] = useState(10);
  const [useTfidf, setUseTfidf] = useState(true);
  const [concepts, setConcepts] = useState('');
  const [mode, setMode] = useState<'keywords' | 'concepts'>('keywords');

  // Mutation para extraer keywords
  const keywordsMutation = useMutation({
    mutationFn: () => {
      const abstractsList = abstracts.split('\n').filter(a => a.trim());
      return frequencyService.extractKeywords({
        abstracts: abstractsList,
        max_keywords: maxKeywords,
        use_tfidf: useTfidf,
      });
    },
  });

  // Mutation para analizar conceptos
  const conceptsMutation = useMutation({
    mutationFn: () => {
      const abstractsList = abstracts.split('\n').filter(a => a.trim());
      const conceptsList = concepts.split('\n').filter(c => c.trim());
      return frequencyService.analyzeConcepts({
        abstracts: abstractsList,
        concepts: conceptsList,
      });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (mode === 'keywords') {
      keywordsMutation.mutate();
    } else {
      conceptsMutation.mutate();
    }
  };

  const loadExample = () => {
    setAbstracts(
      `Machine learning is a subset of artificial intelligence that enables systems to learn from data.
Deep learning uses neural networks with multiple layers to extract features automatically.
Natural language processing focuses on the interaction between computers and human language.
Computer vision enables machines to interpret and understand visual information from the world.
Reinforcement learning trains agents to make decisions through trial and error interactions.`
    );
    setConcepts('machine learning\nartificial intelligence\nneural networks');
  };

  const downloadCSV = () => {
    if (!keywordsMutation.data) return;

    const csv = [
      ['Keyword', 'Frequency', 'Score'],
      ...keywordsMutation.data.map(k => [k.keyword, k.frequency.toString(), k.score.toFixed(3)]),
    ]
      .map(row => row.join(','))
      .join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'keywords_frequency.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  const isLoading = keywordsMutation.isPending || conceptsMutation.isPending;
  const error = keywordsMutation.error || conceptsMutation.error;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Análisis de Frecuencia
        </h1>
        <p className="text-gray-600">
          Extrae palabras clave y analiza frecuencia de conceptos en abstracts
        </p>
      </div>

      {/* Selector de modo */}
      <div className="bg-white rounded-lg shadow-sm p-4">
        <div className="flex gap-2">
          <button
            onClick={() => setMode('keywords')}
            className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
              mode === 'keywords'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Extracción de Keywords
          </button>
          <button
            onClick={() => setMode('concepts')}
            className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
              mode === 'concepts'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Análisis de Conceptos
          </button>
        </div>
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
              rows={8}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
              placeholder="Ingresa los abstracts, uno por línea..."
              required
            />
            <p className="text-sm text-gray-500 mt-1">
              {abstracts.split('\n').filter(a => a.trim()).length} abstracts ingresados
            </p>
          </div>

          {mode === 'keywords' ? (
            <>
              {/* Configuración Keywords */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="maxKeywords" className="block text-sm font-medium text-gray-700 mb-2">
                    Número máximo de keywords: {maxKeywords}
                  </label>
                  <input
                    type="range"
                    id="maxKeywords"
                    min="5"
                    max="50"
                    value={maxKeywords}
                    onChange={(e) => setMaxKeywords(Number(e.target.value))}
                    className="w-full"
                  />
                </div>

                <div className="flex items-center">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={useTfidf}
                      onChange={(e) => setUseTfidf(e.target.checked)}
                      className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <span className="text-sm font-medium text-gray-700">
                      Usar TF-IDF para ponderación
                    </span>
                  </label>
                </div>
              </div>
            </>
          ) : (
            <>
              {/* Conceptos a buscar */}
              <div>
                <label htmlFor="concepts" className="block text-sm font-medium text-gray-700 mb-2">
                  Conceptos a analizar (uno por línea)
                </label>
                <textarea
                  id="concepts"
                  value={concepts}
                  onChange={(e) => setConcepts(e.target.value)}
                  rows={4}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
                  placeholder="machine learning&#10;artificial intelligence&#10;neural networks"
                  required
                />
              </div>
            </>
          )}

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
            disabled={isLoading || !abstracts.trim()}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Analizando...
              </>
            ) : (
              <>
                <BarChart3 className="w-5 h-5" />
                {mode === 'keywords' ? 'Extraer Keywords' : 'Analizar Conceptos'}
              </>
            )}
          </button>
        </form>
      </div>

      {/* Resultados Keywords */}
      {mode === 'keywords' && keywordsMutation.data && (
        <div className="bg-white rounded-lg shadow-sm p-6 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900">Keywords Extraídas</h2>
            <button
              onClick={downloadCSV}
              className="flex items-center gap-2 px-4 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <Download className="w-4 h-4" />
              Descargar CSV
            </button>
          </div>

          {/* Tabla */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Keyword</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">Frecuencia</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">Peso</th>
                  <th className="py-3 px-4 text-sm font-semibold text-gray-700">Distribución</th>
                </tr>
              </thead>
              <tbody>
                {keywordsMutation.data
                  ?.sort((a, b) => (b.frequency || 0) - (a.frequency || 0))
                  ?.map((keyword) => {
                    const maxFreq = Math.max(...keywordsMutation.data!.map(k => k.frequency || 0));
                    return (
                      <tr key={keyword.keyword} className="border-b border-gray-100 hover:bg-gray-50">
                        <td className="py-3 px-4 font-mono text-sm text-gray-900">{keyword.keyword}</td>
                        <td className="py-3 px-4 text-right font-semibold text-gray-900">{keyword.frequency}</td>
                        <td className="py-3 px-4 text-right text-sm text-gray-600">
                          {keyword.score ? keyword.score.toFixed(3) : 'N/A'}
                        </td>
                        <td className="py-3 px-4">
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full"
                              style={{
                                width: `${(keyword.frequency / maxFreq) * 100}%`,
                              }}
                            />
                          </div>
                        </td>
                      </tr>
                    );
                  })}
              </tbody>
            </table>
          </div>

          {/* Gráfico simple de barras */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Distribución Visual</h3>
            <div className="space-y-2">
              {keywordsMutation.data?.slice(0, 10).map((keyword) => {
                const maxFreq = Math.max(...keywordsMutation.data!.map(k => k.frequency || 0));
                return (
                  <div key={keyword.keyword} className="flex items-center gap-3">
                    <div className="w-48 text-sm font-mono text-gray-700 truncate">{keyword.keyword}</div>
                    <div className="flex-1 bg-gray-200 rounded-full h-8">
                      <div
                        className="bg-blue-600 h-8 rounded-full flex items-center justify-end pr-3"
                        style={{
                          width: `${(keyword.frequency / maxFreq) * 100}%`,
                        }}
                      >
                        <span className="text-white text-sm font-semibold">{keyword.frequency}</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Resultados Conceptos */}
      {mode === 'concepts' && conceptsMutation.data && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Análisis de Conceptos</h2>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Concepto</th>
                  <th className="text-center py-3 px-4 text-sm font-semibold text-gray-700">Apariciones</th>
                  <th className="text-center py-3 px-4 text-sm font-semibold text-gray-700">Frecuencia Doc.</th>
                  <th className="text-center py-3 px-4 text-sm font-semibold text-gray-700">Frecuencia Rel.</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(conceptsMutation.data).map(([concept, data]) => (
                  <tr key={concept} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4 font-mono text-sm text-gray-900">{concept}</td>
                    <td className="py-3 px-4 text-center font-semibold text-gray-900">{data.total_occurrences}</td>
                    <td className="py-3 px-4 text-center text-sm text-gray-600">{data.document_frequency}</td>
                    <td className="py-3 px-4 text-center text-sm text-gray-600">
                      {(data.relative_frequency * 100).toFixed(1)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm text-red-800">
            Error al analizar frecuencias. Por favor, intenta de nuevo.
          </p>
        </div>
      )}
    </div>
  );
}
