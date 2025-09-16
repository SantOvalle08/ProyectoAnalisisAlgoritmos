// Custom hooks para análisis bibliométrico

import { useState, useEffect, useCallback } from 'react'
import { BiblioMetricService } from '../services/api'
import type { 
  ResearchPaper, 
  SearchFilters, 
  AnalysisResult, 
  BiblioMetrics,
  PaginatedResponse 
} from '../types'

// Hook para búsqueda de papers
export const useSearchPapers = () => {
  const [papers, setPapers] = useState<ResearchPaper[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    limit: 20,
    hasNext: false,
    hasPrev: false
  })

  const searchPapers = useCallback(async (
    filters: SearchFilters, 
    page = 1, 
    limit = 20
  ) => {
    setLoading(true)
    setError(null)
    
    try {
      const result: PaginatedResponse<ResearchPaper> = 
        await BiblioMetricService.searchPapers(filters, page, limit)
      
      setPapers(result.data)
      setPagination({
        total: result.total,
        page: result.page,
        limit: result.limit,
        hasNext: result.hasNext,
        hasPrev: result.hasPrev
      })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al buscar papers')
    } finally {
      setLoading(false)
    }
  }, [])

  const clearResults = useCallback(() => {
    setPapers([])
    setPagination({
      total: 0,
      page: 1,
      limit: 20,
      hasNext: false,
      hasPrev: false
    })
    setError(null)
  }, [])

  return {
    papers,
    loading,
    error,
    pagination,
    searchPapers,
    clearResults
  }
}

// Hook para análisis bibliométrico
export const useBibliometricAnalysis = () => {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const performAnalysis = useCallback(async (filters: SearchFilters) => {
    setLoading(true)
    setError(null)
    
    try {
      const result = await BiblioMetricService.performAnalysis(filters)
      setAnalysisResult(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error en el análisis')
    } finally {
      setLoading(false)
    }
  }, [])

  const clearAnalysis = useCallback(() => {
    setAnalysisResult(null)
    setError(null)
  }, [])

  return {
    analysisResult,
    loading,
    error,
    performAnalysis,
    clearAnalysis
  }
}

// Hook para métricas en tiempo real
export const useMetrics = (papersIds: string[]) => {
  const [metrics, setMetrics] = useState<BiblioMetrics | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (papersIds.length === 0) {
      setMetrics(null)
      return
    }

    const fetchMetrics = async () => {
      setLoading(true)
      setError(null)
      
      try {
        const result = await BiblioMetricService.getMetrics(papersIds)
        setMetrics(result)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error al calcular métricas')
      } finally {
        setLoading(false)
      }
    }

    fetchMetrics()
  }, [papersIds])

  return { metrics, loading, error }
}

// Hook para manejo de filtros de búsqueda
export const useSearchFilters = () => {
  const [filters, setFilters] = useState<SearchFilters>({
    query: '',
    startYear: undefined,
    endYear: undefined,
    authors: [],
    keywords: [],
    journals: []
  })

  const updateFilter = useCallback(<K extends keyof SearchFilters>(
    key: K,
    value: SearchFilters[K]
  ) => {
    setFilters(prev => ({ ...prev, [key]: value }))
  }, [])

  const resetFilters = useCallback(() => {
    setFilters({
      query: '',
      startYear: undefined,
      endYear: undefined,
      authors: [],
      keywords: [],
      journals: []
    })
  }, [])

  const hasActiveFilters = useCallback(() => {
    return !!(
      filters.query ||
      filters.startYear ||
      filters.endYear ||
      filters.authors?.length ||
      filters.keywords?.length ||
      filters.journals?.length
    )
  }, [filters])

  return {
    filters,
    updateFilter,
    resetFilters,
    hasActiveFilters
  }
}

// Hook para debounce de búsqueda
export const useDebounce = <T>(value: T, delay: number): T => {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(handler)
    }
  }, [value, delay])

  return debouncedValue
}

// Hook para estado local persistente
export const useLocalStorage = <T>(
  key: string,
  initialValue: T
): [T, (value: T | ((val: T) => T)) => void] => {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error)
      return initialValue
    }
  })

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error)
    }
  }

  return [storedValue, setValue]
}