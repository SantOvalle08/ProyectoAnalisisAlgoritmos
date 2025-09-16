// Tipos principales para análisis bibliométrico

export interface ResearchPaper {
  id: string
  title: string
  authors: string[]
  year: number
  abstract: string
  keywords: string[]
  doi?: string
  citations?: number
  journal?: string
  url?: string
}

export interface Author {
  id: string
  name: string
  affiliation?: string
  publications: ResearchPaper[]
  totalCitations: number
  hIndex?: number
}

export interface BiblioMetrics {
  totalPapers: number
  totalCitations: number
  yearlyDistribution: YearlyData[]
  topKeywords: KeywordData[]
  collaborationNetwork: NetworkData
  citationTrends: CitationTrend[]
}

export interface YearlyData {
  year: number
  count: number
  citations: number
}

export interface KeywordData {
  keyword: string
  frequency: number
  relevance: number
}

export interface NetworkData {
  nodes: NetworkNode[]
  links: NetworkLink[]
}

export interface NetworkNode {
  id: string
  name: string
  value: number
  group?: string
}

export interface NetworkLink {
  source: string
  target: string
  value: number
}

export interface CitationTrend {
  year: number
  citations: number
  papers: number
  avgCitationsPerPaper: number
}

export interface SearchFilters {
  query: string
  startYear?: number
  endYear?: number
  authors?: string[]
  keywords?: string[]
  journals?: string[]
}

export interface AnalysisResult {
  papers: ResearchPaper[]
  metrics: BiblioMetrics
  similarityMatrix?: number[][]
  clusters?: ClusterData[]
  timeline?: TimelineData[]
}

export interface ClusterData {
  id: string
  name: string
  papers: ResearchPaper[]
  keywords: string[]
  centroid: number[]
}

export interface TimelineData {
  year: number
  events: TimelineEvent[]
}

export interface TimelineEvent {
  title: string
  description: string
  papers: ResearchPaper[]
  impact: number
}

// API Response types
export interface ApiResponse<T> {
  data: T
  message: string
  status: 'success' | 'error'
  timestamp: string
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  limit: number
  hasNext: boolean
  hasPrev: boolean
}

// Chart data types
export interface ChartDataPoint {
  x: string | number
  y: number
  label?: string
  color?: string
}

export interface NetworkChartData {
  nodes: NetworkNode[]
  links: NetworkLink[]
}

export interface HeatmapData {
  x: string
  y: string
  value: number
}