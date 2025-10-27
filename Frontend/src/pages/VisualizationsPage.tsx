import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { FileText, Loader2, Download, MapPin, Cloud, CalendarDays, Globe2, BarChart4, Calendar, BookOpen } from 'lucide-react';
import visualizationService from '../services/visualization';
import type { Publication } from '../types';

type VisualizationType = 'wordcloud' | 'heatmap' | 'timeline';

export default function VisualizationsPage() {
  const [publicationsJson, setPublicationsJson] = useState('');
  const [visualizationType, setVisualizationType] = useState<VisualizationType>('wordcloud');
  
  // WordCloud config
  const [maxWords, setMaxWords] = useState(50);
  
  // Heatmap config
  const [mapType, setMapType] = useState<'choropleth' | 'bar'>('choropleth');
  
  // Timeline config
  const [timelineType, setTimelineType] = useState<'simple' | 'journal'>('simple');

  const wordCloudMutation = useMutation({
    mutationFn: () => {
      const publications: Publication[] = JSON.parse(publicationsJson);
      return visualizationService.generateWordCloud({
        publications,
        max_words: maxWords,
      });
    },
    onError: (error) => {
      console.error('Error generando wordcloud:', error);
      alert('Error al generar nube de palabras. Verifica que el JSON sea válido y contenga los campos necesarios.');
    },
  });

  const heatmapMutation = useMutation({
    mutationFn: () => {
      const publications: Publication[] = JSON.parse(publicationsJson);
      return visualizationService.generateHeatmap({
        publications,
        map_type: mapType,
      });
    },
    onError: (error) => {
      console.error('Error generando heatmap:', error);
      alert('Error al generar mapa de calor. Verifica que el JSON sea válido y contenga los campos necesarios (authors con país).');
    },
  });

  const timelineMutation = useMutation({
    mutationFn: () => {
      const publications: Publication[] = JSON.parse(publicationsJson);
      return visualizationService.generateTimeline({
        publications,
        group_by_journal: timelineType === 'journal',
      });
    },
    onError: (error) => {
      console.error('Error generando timeline:', error);
      alert('Error al generar línea temporal. Verifica que el JSON sea válido y contenga los campos necesarios (year, journal).');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      JSON.parse(publicationsJson); // Validate JSON
      
      switch (visualizationType) {
        case 'wordcloud':
          wordCloudMutation.mutate();
          break;
        case 'heatmap':
          heatmapMutation.mutate();
          break;
        case 'timeline':
          timelineMutation.mutate();
          break;
      }
    } catch (error) {
      console.error('Invalid JSON', error);
      alert('JSON inválido. Por favor verifica el formato.');
    }
  };

  const loadExample = () => {
    const example = [
      {
        title: 'Machine Learning in Healthcare',
        authors: [
          { name: 'John Doe', affiliation: 'MIT, United States', country: 'United States' },
          { name: 'Jane Smith', affiliation: 'Stanford University, United States', country: 'United States' }
        ],
        year: 2023,
        journal: 'Nature Medicine',
        abstract: 'Machine learning algorithms are transforming healthcare with predictive analytics and diagnosis.',
        keywords: ['machine learning', 'healthcare', 'AI', 'predictive analytics'],
        source: 'IEEE',
        doi: '10.1109/example.2023',
      },
      {
        title: 'Deep Learning for Image Recognition',
        authors: [
          { name: 'Alice Johnson', affiliation: 'Oxford University, United Kingdom', country: 'United Kingdom' }
        ],
        year: 2022,
        journal: 'IEEE Transactions on Pattern Analysis',
        abstract: 'Deep neural networks achieve state-of-the-art results in computer vision tasks.',
        keywords: ['deep learning', 'computer vision', 'neural networks', 'image recognition'],
        source: 'ACM',
        doi: '10.1145/example.2022',
      },
      {
        title: 'Natural Language Processing with Transformers',
        authors: [
          { name: 'Carlos García', affiliation: 'Universidad Complutense, Spain', country: 'Spain' }
        ],
        year: 2023,
        journal: 'Computational Linguistics',
        abstract: 'Transformer architectures revolutionize NLP tasks with attention mechanisms.',
        keywords: ['natural language processing', 'transformers', 'attention', 'NLP'],
        source: 'CrossRef',
        doi: '10.1162/example.2023',
      },
      {
        title: 'Reinforcement Learning in Robotics',
        authors: [
          { name: 'Yuki Tanaka', affiliation: 'University of Tokyo, Japan', country: 'Japan' }
        ],
        year: 2022,
        journal: 'Robotics and Autonomous Systems',
        abstract: 'Reinforcement learning enables robots to learn complex behaviors through trial and error.',
        keywords: ['reinforcement learning', 'robotics', 'autonomous systems', 'AI'],
        source: 'ScienceDirect',
        doi: '10.1016/example.2022',
      },
    ];
    setPublicationsJson(JSON.stringify(example, null, 2));
  };

  const downloadHTML = (html: string, filename: string) => {
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  const getCurrentResult = () => {
    switch (visualizationType) {
      case 'wordcloud':
        return wordCloudMutation.data;
      case 'heatmap':
        return heatmapMutation.data;
      case 'timeline':
        return timelineMutation.data;
    }
  };

  const getCurrentError = () => {
    return wordCloudMutation.error || heatmapMutation.error || timelineMutation.error;
  };

  const isLoading = wordCloudMutation.isPending || heatmapMutation.isPending || timelineMutation.isPending;
  const currentResult = getCurrentResult();
  const currentError = getCurrentError();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Generación de Visualizaciones
        </h1>
        <p className="text-gray-600">
          Crea visualizaciones interactivas de nubes de palabras, mapas de calor y líneas de tiempo
        </p>
      </div>

      {/* Selector de tipo de visualización */}
      <div className="bg-white rounded-lg shadow-sm p-4">
        <div className="grid grid-cols-3 gap-3">
          <button
            onClick={() => setVisualizationType('wordcloud')}
            className={`flex items-center justify-center gap-2 py-3 px-4 rounded-lg font-medium transition-colors ${
              visualizationType === 'wordcloud'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <Cloud className="w-5 h-5" />
            Nube de Palabras
          </button>
          <button
            onClick={() => setVisualizationType('heatmap')}
            className={`flex items-center justify-center gap-2 py-3 px-4 rounded-lg font-medium transition-colors ${
              visualizationType === 'heatmap'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <MapPin className="w-5 h-5" />
            Mapa de Calor
          </button>
          <button
            onClick={() => setVisualizationType('timeline')}
            className={`flex items-center justify-center gap-2 py-3 px-4 rounded-lg font-medium transition-colors ${
              visualizationType === 'timeline'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <CalendarDays className="w-5 h-5" />
            Línea de Tiempo
          </button>
        </div>
      </div>

      {/* Formulario */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Input JSON */}
          <div>
            <label htmlFor="publications" className="block text-sm font-medium text-gray-700 mb-2">
              Publicaciones (formato JSON)
            </label>
            <textarea
              id="publications"
              value={publicationsJson}
              onChange={(e) => setPublicationsJson(e.target.value)}
              rows={12}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-xs"
              placeholder='[{"title": "...", "authors": [{"name": "...", "country": "..."}], "year": 2023, "journal": "...", "abstract": "...", "keywords": [...]}]'
              required
            />
            <button
              type="button"
              onClick={loadExample}
              className="mt-2 text-sm text-blue-600 hover:text-blue-700 underline"
            >
              Cargar ejemplo
            </button>
          </div>

          {/* Configuración específica por tipo */}
          {visualizationType === 'wordcloud' && (
            <div>
              <label htmlFor="maxWords" className="block text-sm font-medium text-gray-700 mb-2">
                Número máximo de palabras: {maxWords}
              </label>
              <input
                type="range"
                id="maxWords"
                min="10"
                max="200"
                value={maxWords}
                onChange={(e) => setMaxWords(Number(e.target.value))}
                className="w-full"
              />
            </div>
          )}

          {visualizationType === 'heatmap' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Tipo de Mapa
              </label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setMapType('choropleth')}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    mapType === 'choropleth'
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 bg-white hover:border-gray-300'
                  }`}
                >
                  <div className="flex flex-col items-center justify-center gap-1">
                    <Globe2 className={`w-6 h-6 ${mapType === 'choropleth' ? 'text-blue-600' : 'text-gray-500'}`} />
                    <div>
                      <div className="font-semibold text-base text-center">Choropleth</div>
                      <div className="text-sm text-gray-600 text-center">Mapa geográfico</div>
                    </div>
                  </div>
                </button>
                <button
                  type="button"
                  onClick={() => setMapType('bar')}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    mapType === 'bar'
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 bg-white hover:border-gray-300'
                  }`}
                >
                  <div className="flex flex-col items-center justify-center gap-1">
                    <BarChart4 className={`w-6 h-6 ${mapType === 'bar' ? 'text-blue-600' : 'text-gray-500'}`} />
                    <div>
                      <div className="font-semibold text-base text-center">Barras</div>
                      <div className="text-sm text-gray-600 text-center">Gráfico de barras</div>
                    </div>
                  </div>
                </button>
              </div>
            </div>
          )}

          {visualizationType === 'timeline' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Tipo de Timeline
              </label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setTimelineType('simple')}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    timelineType === 'simple'
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 bg-white hover:border-gray-300'
                  }`}
                >
                  <div className="flex flex-col items-center justify-center gap-1">
                    <Calendar className={`w-6 h-6 ${timelineType === 'simple' ? 'text-blue-600' : 'text-gray-500'}`} />
                    <div>
                      <div className="font-semibold text-base text-center">Simple</div>
                      <div className="text-sm text-gray-600 text-center">Por año</div>
                    </div>
                  </div>
                </button>
                <button
                  type="button"
                  onClick={() => setTimelineType('journal')}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    timelineType === 'journal'
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 bg-white hover:border-gray-300'
                  }`}
                >
                  <div className="flex flex-col items-center justify-center gap-1">
                    <BookOpen className={`w-6 h-6 ${timelineType === 'journal' ? 'text-blue-600' : 'text-gray-500'}`} />
                    <div>
                      <div className="font-semibold text-base text-center">Por Journal</div>
                      <div className="text-sm text-gray-600 text-center">Agrupado por revista</div>
                    </div>
                  </div>
                </button>
              </div>
            </div>
          )}

          {/* Botón generar */}
          <button
            type="submit"
            disabled={isLoading || !publicationsJson.trim()}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Generando...
              </>
            ) : (
              <>
                <FileText className="w-5 h-5" />
                Generar Visualización
              </>
            )}
          </button>
        </form>
      </div>

      {/* Resultado */}
      {currentResult && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Resultado</h2>
            {(visualizationType === 'heatmap' || visualizationType === 'timeline') && 'html' in currentResult && (
              <button
                onClick={() => downloadHTML(currentResult.html as string, `visualization_${visualizationType}.html`)}
                className="flex items-center gap-2 px-4 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <Download className="w-4 h-4" />
                Descargar HTML
              </button>
            )}
          </div>

          {/* Preview HTML (solo para heatmap y timeline) */}
          {(visualizationType === 'heatmap' || visualizationType === 'timeline') && 'html' in currentResult && (
            <div className="border-2 border-gray-200 rounded-lg overflow-hidden mb-4">
              <iframe
                srcDoc={currentResult.html as string}
                className="w-full h-96 bg-white"
                title="Visualization Preview"
                sandbox="allow-scripts"
              />
            </div>
          )}

          {/* WordCloud preview (imagen base64) */}
          {visualizationType === 'wordcloud' && wordCloudMutation.data && (
            <div className="border-2 border-gray-200 rounded-lg overflow-hidden mb-4 p-6 bg-gray-50 text-center">
              {wordCloudMutation.data.image_base64 ? (
                <img 
                  src={wordCloudMutation.data.image_base64.startsWith('data:') ? wordCloudMutation.data.image_base64 : `data:image/png;base64,${wordCloudMutation.data.image_base64}`}
                  alt="Word Cloud" 
                  className="max-w-full mx-auto"
                />
              ) : (
                <div className="py-12">
                  <Cloud className="w-16 h-16 mx-auto text-gray-400 mb-2" />
                  <p className="text-gray-600">Nube de palabras generada</p>
                </div>
              )}
            </div>
          )}

          {/* Metadata - WordCloud */}
          {visualizationType === 'wordcloud' && wordCloudMutation.data?.top_terms && (
            <div className="p-4 bg-gray-50 rounded-lg">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Top Términos</h3>
              <div className="flex flex-wrap gap-2">
                {wordCloudMutation.data.top_terms.slice(0, 10).map((term) => (
                  <span key={term.term} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
                    {term.term}: {term.weight.toFixed(3)}
                  </span>
                ))}
              </div>
              <div className="mt-3 text-sm text-gray-600">
                <span>Publicaciones: {wordCloudMutation.data.num_publications}</span>
                <span className="mx-2">•</span>
                <span>Total términos: {wordCloudMutation.data.total_terms}</span>
              </div>
            </div>
          )}

          {/* Metadata - Heatmap */}
          {visualizationType === 'heatmap' && heatmapMutation.data && (
            <div className="p-4 bg-gray-50 rounded-lg">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Distribución por País</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                {heatmapMutation.data.country_distribution.slice(0, 6).map((item) => (
                  <div key={item.country} className="px-3 py-2 bg-white rounded border border-gray-200">
                    <div className="text-xs text-gray-600">{item.country}</div>
                    <div className="text-lg font-semibold text-blue-600">{item.count}</div>
                  </div>
                ))}
              </div>
              <div className="mt-3 text-sm text-gray-600">
                <span>Publicaciones: {heatmapMutation.data.num_publications}</span>
                <span className="mx-2">•</span>
                <span>Países: {heatmapMutation.data.num_countries}</span>
              </div>
            </div>
          )}

          {/* Metadata - Timeline */}
          {visualizationType === 'timeline' && timelineMutation.data && (
            <div className="p-4 bg-gray-50 rounded-lg">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Distribución Temporal</h3>
              <div className="flex gap-2">
                {timelineMutation.data.yearly_distribution.map((item) => (
                  <div key={item.year} className="px-3 py-2 bg-white rounded border border-gray-200">
                    <div className="text-xs text-gray-600">{item.year}</div>
                    <div className="text-lg font-semibold text-purple-600">{item.count}</div>
                  </div>
                ))}
              </div>
              <div className="mt-3 text-sm text-gray-600">
                <span>Publicaciones: {timelineMutation.data.num_publications}</span>
                <span className="mx-2">•</span>
                <span>Rango: {timelineMutation.data.year_range.min}-{timelineMutation.data.year_range.max}</span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Error */}
      {currentError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm text-red-800">
            Error al generar visualización. Verifica que el JSON sea válido.
          </p>
        </div>
      )}
    </div>
  );
}
