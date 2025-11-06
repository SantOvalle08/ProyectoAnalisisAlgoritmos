import { Link } from 'react-router-dom';
import { 
  Database, 
  GitCompare, 
  BarChart3, 
  Network, 
  LineChart,
  BookOpen,
  Target,
  Zap 
} from 'lucide-react';

const features = [
  {
    name: 'Adquisición Automática de Datos',
    description: 'Descarga y unifica datos de múltiples fuentes científicas como CrossRef, ACM y ScienceDirect.',
    icon: Database,
    href: '/data-acquisition',
    color: 'bg-blue-500',
  },
  {
    name: 'Análisis de Similitud Textual',
    description: 'Compara textos usando 6 algoritmos: Levenshtein, TF-IDF, Jaccard, N-grams, Sentence-BERT y Word2Vec.',
    icon: GitCompare,
    href: '/similarity',
    color: 'bg-purple-500',
  },
  {
    name: 'Análisis de Frecuencias',
    description: 'Extrae y analiza frecuencias de conceptos clave en abstracts científicos con TF-IDF.',
    icon: BarChart3,
    href: '/frequency',
    color: 'bg-green-500',
  },
  {
    name: 'Clustering Jerárquico',
    description: 'Agrupa publicaciones similares usando métodos Ward, Average y Complete linkage.',
    icon: Network,
    href: '/clustering',
    color: 'bg-orange-500',
  },
  {
    name: 'Visualizaciones Interactivas',
    description: 'Genera word clouds, mapas geográficos y líneas temporales de publicaciones.',
    icon: LineChart,
    href: '/visualizations',
    color: 'bg-pink-500',
  },
];

const stats = [
  { label: 'Algoritmos Implementados', value: '12+' },
  { label: 'Tests Pasando', value: '132/133' },
  { label: 'Cobertura de Tests', value: '64%+' },
  { label: 'APIs REST', value: '5' },
];

export default function HomePage() {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="text-center">
        <div className="flex justify-center mb-6">
          <BookOpen className="w-16 h-16 text-blue-600" />
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Sistema de Análisis Bibliométrico
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
          Plataforma completa para análisis computacional de literatura científica
          con algoritmos avanzados de procesamiento de texto y visualización de datos.
        </p>
        <div className="flex justify-center gap-4">
          <Link
            to="/data-acquisition"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors flex items-center gap-2"
          >
            <Zap className="w-5 h-5" />
            Comenzar Análisis
          </Link>
          <a
            href="https://github.com/SantOvalle08/ProyectoAnalisisAlgoritmos"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-gray-100 text-gray-700 px-6 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
          >
            Ver Repositorio
          </a>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.label} className="bg-white rounded-lg shadow-sm p-6 text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">{stat.value}</div>
            <div className="text-sm text-gray-600">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Features */}
      <div>
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Funcionalidades Principales
          </h2>
          <p className="text-gray-600">
            Herramientas especializadas para análisis bibliométrico completo
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <Link
                key={feature.name}
                to={feature.href}
                className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow group"
              >
                <div className={`${feature.color} w-12 h-12 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {feature.name}
                </h3>
                <p className="text-gray-600 text-sm">
                  {feature.description}
                </p>
              </Link>
            );
          })}
        </div>
      </div>

      {/* About */}
      <div className="bg-white rounded-lg shadow-sm p-8">
        <div className="flex items-start gap-4">
          <Target className="w-8 h-8 text-blue-600 flex-shrink-0 mt-1" />
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Sobre el Proyecto
            </h2>
            <div className="text-gray-600 space-y-4">
              <p>
                Este sistema fue desarrollado como proyecto del curso de 
                <span className="font-semibold"> Análisis de Algoritmos</span> de la 
                Universidad del Quindío. Implementa algoritmos avanzados para el análisis
                bibliométrico y computacional de literatura científica.
              </p>
              <p>
                El dominio de conocimiento seleccionado es{' '}
                <span className="font-semibold">Inteligencia Artificial Generativa</span>,
                utilizando la cadena de búsqueda: "generative artificial intelligence".
              </p>
              <div className="flex flex-wrap gap-2 pt-4">
                <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                  FastAPI
                </span>
                <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
                  React + TypeScript
                </span>
                <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">
                  Machine Learning
                </span>
                <span className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm font-medium">
                  NLP
                </span>
                <span className="px-3 py-1 bg-pink-100 text-pink-700 rounded-full text-sm font-medium">
                  Data Visualization
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
