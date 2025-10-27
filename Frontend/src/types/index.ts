// Tipos para publicaciones
export interface Publication {
  doi?: string;
  title: string;
  abstract?: string;
  authors?: Author[];
  keywords?: string[];
  year?: string;
  journal?: string;
  published_date?: string;
  venue?: string;
}

export interface Author {
  name: string;
  affiliation?: string;
  orcid?: string;
  country?: string;
}

// Tipos para descarga de datos
export interface DownloadRequest {
  query: string;
  sources: string[];
  max_results_per_source?: number;
  export_formats?: string[];
}

export interface DownloadJob {
  job_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  total_publications?: number;
  message?: string;
  created_at: string;
  completed_at?: string;
}

// Tipos para similitud
export interface SimilarityRequest {
  text1: string;
  text2: string;
  algorithm: 'levenshtein' | 'tfidf_cosine' | 'jaccard' | 'ngram' | 'sentence_bert' | 'bert';
}

export interface SimilarityResult {
  algorithm: string;
  similarity: number;
  distance?: number;
  execution_time: number;
  details?: Record<string, unknown>;
}

export interface BatchSimilarityRequest {
  pairs: Array<{ text1: string; text2: string }>;
  algorithm: string;
}

// Tipos para análisis de frecuencias
export interface FrequencyAnalysisRequest {
  abstracts: string[];
  max_keywords?: number;
  use_tfidf?: boolean;
}

export interface FrequencyResult {
  keyword: string;
  score: number;
  method: string;
  frequency: number;
}

export interface KeywordFrequency {
  keyword: string;
  score: number;
  method: string;
  frequency: number;
}

export interface ConceptAnalysisRequest {
  abstracts: string[];
  concepts?: string[];
}

export interface ConceptFrequency {
  concept: string;
  total_occurrences: number;
  document_frequency: number;
  relative_frequency: number;
  documents_with_concept: number[];
  example_contexts?: string[] | null;
}

export type ConceptAnalysisResult = Record<string, ConceptFrequency>;

// Tipos para clustering
export interface ClusteringRequest {
  abstracts: string[];
  method?: 'ward' | 'average' | 'complete';
  num_clusters?: number; // Cambiado de n_clusters a num_clusters para coincidir con backend
  labels?: string[];
}

export interface ClusteringResult {
  cluster_labels: number[] | null;
  num_clusters: number;
  silhouette_score: number | null;
  dendrogram_base64?: string;
  cophenetic_correlation?: number;
  davies_bouldin_score?: number | null;
  calinski_harabasz_score?: number | null;
  method: string;
  num_documents: number;
  num_features?: number;
}

// Tipos para visualizaciones
export interface WordCloudRequest {
  publications: Publication[];
  max_words?: number;
  use_tfidf?: boolean;
  include_keywords?: boolean;
}

export interface WordCloudResult {
  image_base64: string;
  top_terms: Array<{ term: string; weight: number }>;
  num_publications: number;
  total_terms: number;
}

export interface HeatmapRequest {
  publications: Publication[];
  map_type?: 'choropleth' | 'bar';
  title?: string;
  top_n?: number;
}

export interface HeatmapResult {
  html: string;
  country_distribution: Array<{ country: string; count: number }>;
  num_publications: number;
  num_countries: number;
}

export interface TimelineRequest {
  publications: Publication[];
  group_by_journal?: boolean;
  top_n_journals?: number;
  title?: string;
}

export interface TimelineResult {
  html: string;
  yearly_distribution: Array<{ year: number; count: number }>;
  num_publications: number;
  year_range: { min: number; max: number };
}

export interface PDFExportRequest {
  visualizations: {
    wordcloud?: WordCloudResult;
    heatmap?: HeatmapResult;
    timeline?: TimelineResult;
  };
  metadata?: Record<string, unknown>;
}

// Tipos para la UI
export interface NavItem {
  name: string;
  href: string;
  icon?: React.ComponentType<{ className?: string }>;
}

export interface LoadingState {
  isLoading: boolean;
  message?: string;
}

export interface ErrorState {
  hasError: boolean;
  message?: string;
}
