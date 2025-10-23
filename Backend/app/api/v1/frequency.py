"""
API REST para Análisis de Frecuencias de Conceptos
===================================================

Endpoints para análisis de frecuencias de conceptos predefinidos
y extracción automática de keywords desde abstracts científicos.

Requerimiento 3: Análisis de Frecuencias

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Date: Octubre 2025
University: Universidad del Quindío - Análisis de Algoritmos
"""

from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional, Literal
from enum import Enum
import logging

from app.services.ml_analysis.frequency import (
    ConceptAnalyzer,
    ExtractionMethod
)
from app.config.concepts import (
    get_generative_ai_concepts,
    GENERATIVE_AI_EDUCATION_CONCEPTS,
    EDUCATION_RELATED_CONCEPTS,
    AI_TECHNICAL_CONCEPTS
)

# Configurar logging
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(prefix="/frequency", tags=["Frequency Analysis"])


# ============================================================================
# MODELOS PYDANTIC
# ============================================================================

class AnalyzeConceptsRequest(BaseModel):
    """Request para analizar conceptos predefinidos."""
    abstracts: List[str] = Field(
        ...,
        min_items=1,
        max_items=1000,
        description="Lista de abstracts a analizar"
    )
    concepts: Optional[List[str]] = Field(
        default=None,
        description="Conceptos a buscar. Si no se especifica, usa los 15 predefinidos"
    )
    include_contexts: bool = Field(
        default=True,
        description="Incluir contextos donde aparecen los conceptos"
    )
    
    @validator('abstracts')
    def validate_abstracts(cls, v):
        """Valida que los abstracts no estén vacíos."""
        for i, abstract in enumerate(v):
            if not abstract or not abstract.strip():
                raise ValueError(f"Abstract {i} está vacío")
        return v


class ExtractKeywordsRequest(BaseModel):
    """Request para extraer keywords automáticamente."""
    abstracts: List[str] = Field(
        ...,
        min_items=1,
        max_items=1000,
        description="Lista de abstracts"
    )
    max_keywords: int = Field(
        default=15,
        ge=1,
        le=50,
        description="Número máximo de keywords a extraer"
    )
    method: ExtractionMethod = Field(
        default=ExtractionMethod.TFIDF,
        description="Método de extracción: tfidf, frequency, o combined"
    )
    include_ngrams: bool = Field(
        default=True,
        description="Incluir n-gramas (frases multi-palabra)"
    )
    ngram_range: tuple = Field(
        default=(1, 3),
        description="Rango de n-gramas (min, max)"
    )


class PrecisionAnalysisRequest(BaseModel):
    """Request para análisis de precisión."""
    abstracts: List[str] = Field(
        ...,
        min_items=1,
        max_items=1000
    )
    predefined_concepts: Optional[List[str]] = Field(
        default=None,
        description="Conceptos predefinidos. Si no se especifica, usa los 15 de IA Generativa"
    )
    max_keywords: int = Field(default=15, ge=1, le=50)
    extraction_method: ExtractionMethod = Field(default=ExtractionMethod.TFIDF)
    precision_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Umbral para coincidencias parciales"
    )


class FullReportRequest(BaseModel):
    """Request para reporte completo."""
    abstracts: List[str] = Field(..., min_items=1, max_items=1000)
    predefined_concepts: Optional[List[str]] = Field(default=None)
    max_keywords: int = Field(default=15, ge=1, le=50)


class ConceptFrequencyResponse(BaseModel):
    """Response para frecuencia de un concepto."""
    concept: str
    total_occurrences: int
    document_frequency: int
    relative_frequency: float
    documents_with_concept: List[int]
    example_contexts: Optional[List[str]] = None


class KeywordResponse(BaseModel):
    """Response para un keyword extraído."""
    keyword: str
    score: float
    method: str
    frequency: int


class PrecisionMetricsResponse(BaseModel):
    """Response para métricas de precisión."""
    precision: float
    recall: float
    f1_score: float
    exact_matches: List[str]
    partial_matches: List[Dict[str, Any]]
    total_extracted: int
    total_predefined: int
    num_exact_matches: int
    num_partial_matches: int
    num_no_match: int


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

# Instancia global del analizador (inicializado una sola vez)
_analyzer: Optional[ConceptAnalyzer] = None


def get_analyzer() -> ConceptAnalyzer:
    """
    Obtiene o crea la instancia del analizador.
    
    Returns:
        Instancia de ConceptAnalyzer
    """
    global _analyzer
    
    if _analyzer is None:
        logger.info("Inicializando ConceptAnalyzer global...")
        _analyzer = ConceptAnalyzer(
            language='english',
            use_stemming=False,
            use_lemmatization=True,
            min_word_length=3,
            max_ngram_size=3
        )
        logger.info("ConceptAnalyzer inicializado correctamente")
    
    return _analyzer


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post(
    "/analyze-concepts",
    response_model=Dict[str, ConceptFrequencyResponse],
    summary="Analizar conceptos predefinidos",
    description="""
    Analiza la frecuencia de conceptos predefinidos en un corpus de abstracts.
    
    Para cada concepto calcula:
    - Frecuencia total (número de ocurrencias)
    - Frecuencia documental (en cuántos documentos aparece)
    - Frecuencia relativa (porcentaje del total de palabras)
    - Lista de documentos donde aparece
    - Contextos de aparición (opcional)
    
    Por defecto analiza los 15 conceptos de "Generative AI in Education".
    Se pueden especificar conceptos personalizados.
    
    Ejemplo:
    ```json
    {
      "abstracts": [
        "Machine learning enables personalized education...",
        "Generative AI models create customized content..."
      ],
      "concepts": null,
      "include_contexts": true
    }
    ```
    """
)
async def analyze_predefined_concepts(request: AnalyzeConceptsRequest):
    """
    Analiza frecuencias de conceptos predefinidos.
    
    Args:
        request: Datos de la petición
    
    Returns:
        Diccionario {concepto: frecuencia_info}
    """
    try:
        logger.info(f"Analizando conceptos en {len(request.abstracts)} abstracts")
        
        # Obtener analizador
        analyzer = get_analyzer()
        
        # Usar conceptos predefinidos si no se especificaron
        concepts = request.concepts if request.concepts else get_generative_ai_concepts()
        
        # Analizar conceptos
        results = analyzer.analyze_predefined_concepts(
            request.abstracts,
            concepts
        )
        
        # Convertir a formato de respuesta
        response = {}
        for concept, freq in results.items():
            response[concept] = ConceptFrequencyResponse(
                concept=freq.concept,
                total_occurrences=freq.total_occurrences,
                document_frequency=freq.document_frequency,
                relative_frequency=freq.relative_frequency,
                documents_with_concept=freq.documents_with_concept[:10],
                example_contexts=freq.contexts[:3] if request.include_contexts else None
            )
        
        logger.info(f"Análisis completado: {len(results)} conceptos procesados")
        
        return response
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error en analyze_predefined_concepts: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analizando conceptos: {str(e)}"
        )


@router.post(
    "/extract-keywords",
    response_model=List[KeywordResponse],
    summary="Extraer keywords automáticamente",
    description="""
    Extrae keywords automáticamente de un corpus de abstracts usando
    algoritmos de NLP.
    
    Métodos disponibles:
    - `tfidf`: TF-IDF (Term Frequency-Inverse Document Frequency)
    - `frequency`: Frecuencia simple
    - `combined`: Combinación de TF-IDF y frecuencia
    
    El método TF-IDF es generalmente el más efectivo para textos científicos.
    
    Características:
    - Elimina stopwords automáticamente
    - Soporta n-gramas (frases multi-palabra)
    - Normaliza y lemmatiza términos
    - Ordena por relevancia
    
    Ejemplo:
    ```json
    {
      "abstracts": ["Abstract 1...", "Abstract 2..."],
      "max_keywords": 15,
      "method": "tfidf",
      "include_ngrams": true,
      "ngram_range": [1, 3]
    }
    ```
    """
)
async def extract_keywords(request: ExtractKeywordsRequest):
    """
    Extrae keywords automáticamente.
    
    Args:
        request: Datos de la petición
    
    Returns:
        Lista de keywords con scores
    """
    try:
        logger.info(f"Extrayendo keywords de {len(request.abstracts)} abstracts "
                   f"usando método {request.method}")
        
        # Obtener analizador
        analyzer = get_analyzer()
        
        # Extraer keywords según el método
        if request.method == ExtractionMethod.TFIDF:
            keywords = analyzer.extract_keywords_tfidf(
                request.abstracts,
                max_keywords=request.max_keywords,
                ngram_range=request.ngram_range
            )
        
        elif request.method == ExtractionMethod.FREQUENCY:
            keywords = analyzer.extract_keywords_frequency(
                request.abstracts,
                max_keywords=request.max_keywords,
                include_ngrams=request.include_ngrams
            )
        
        else:  # COMBINED
            keywords = analyzer.extract_keywords(
                request.abstracts,
                max_keywords=request.max_keywords,
                method=ExtractionMethod.COMBINED
            )
        
        # Convertir a formato de respuesta
        response = [
            KeywordResponse(
                keyword=kw.keyword,
                score=kw.score,
                method=kw.method,
                frequency=kw.frequency
            )
            for kw in keywords
        ]
        
        logger.info(f"Extraídos {len(response)} keywords")
        
        return response
    
    except Exception as e:
        logger.error(f"Error en extract_keywords: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error extrayendo keywords: {str(e)}"
        )


@router.post(
    "/precision-analysis",
    response_model=PrecisionMetricsResponse,
    summary="Analizar precisión de extracción",
    description="""
    Calcula la precisión de los keywords extraídos comparándolos
    con conceptos predefinidos.
    
    Métricas calculadas:
    - **Precision**: Keywords extraídos que coinciden / Total extraídos
    - **Recall**: Conceptos predefinidos encontrados / Total predefinidos
    - **F1-Score**: Media armónica de Precision y Recall
    - **Coincidencias exactas**: Matches perfectos
    - **Coincidencias parciales**: Matches con similitud > umbral
    
    Útil para:
    - Evaluar calidad de extracción automática
    - Comparar diferentes métodos de extracción
    - Validar keywords generados
    
    Ejemplo:
    ```json
    {
      "abstracts": ["Abstract 1...", "Abstract 2..."],
      "predefined_concepts": null,
      "max_keywords": 15,
      "extraction_method": "tfidf",
      "precision_threshold": 0.7
    }
    ```
    """
)
async def analyze_precision(request: PrecisionAnalysisRequest):
    """
    Calcula métricas de precisión.
    
    Args:
        request: Datos de la petición
    
    Returns:
        Métricas de precisión
    """
    try:
        logger.info(f"Analizando precisión en {len(request.abstracts)} abstracts")
        
        # Obtener analizador
        analyzer = get_analyzer()
        
        # Usar conceptos predefinidos si no se especificaron
        predefined = request.predefined_concepts if request.predefined_concepts \
                     else get_generative_ai_concepts()
        
        # Extraer keywords
        keywords = analyzer.extract_keywords(
            request.abstracts,
            max_keywords=request.max_keywords,
            method=request.extraction_method
        )
        
        # Calcular precisión
        metrics = analyzer.calculate_precision(
            keywords,
            predefined,
            threshold=request.precision_threshold
        )
        
        # Convertir a formato de respuesta
        response = PrecisionMetricsResponse(**metrics)
        
        logger.info(f"Precision: {metrics['precision']:.2%}, "
                   f"Recall: {metrics['recall']:.2%}, "
                   f"F1: {metrics['f1_score']:.2%}")
        
        return response
    
    except Exception as e:
        logger.error(f"Error en analyze_precision: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error calculando precisión: {str(e)}"
        )


@router.post(
    "/full-report",
    response_model=Dict[str, Any],
    summary="Generar reporte completo",
    description="""
    Genera un reporte completo de análisis de frecuencias que incluye:
    
    1. **Estadísticas del corpus**:
       - Total de abstracts
       - Total de palabras
       - Promedio palabras por abstract
       - Palabras únicas
    
    2. **Análisis de conceptos predefinidos**:
       - Frecuencias de cada concepto
       - Distribución documental
       - Contextos de aparición
    
    3. **Keywords extraídos automáticamente**:
       - Top 15 keywords por TF-IDF
       - Scores y frecuencias
    
    4. **Métricas de precisión**:
       - Precision, Recall, F1-Score
       - Coincidencias exactas y parciales
    
    Ideal para:
    - Análisis bibliométrico completo
    - Reportes académicos
    - Validación de calidad de datos
    - Identificación de temas principales
    
    Ejemplo:
    ```json
    {
      "abstracts": ["Abstract 1...", "Abstract 2...", "Abstract 3..."],
      "predefined_concepts": null,
      "max_keywords": 15
    }
    ```
    """
)
async def generate_full_report(request: FullReportRequest):
    """
    Genera reporte completo de frecuencias.
    
    Args:
        request: Datos de la petición
    
    Returns:
        Reporte completo con todas las métricas
    """
    try:
        logger.info(f"Generando reporte completo para {len(request.abstracts)} abstracts")
        
        # Obtener analizador
        analyzer = get_analyzer()
        
        # Usar conceptos predefinidos si no se especificaron
        predefined = request.predefined_concepts if request.predefined_concepts \
                     else get_generative_ai_concepts()
        
        # Generar reporte
        report = analyzer.generate_frequency_report(
            request.abstracts,
            predefined,
            max_keywords=request.max_keywords
        )
        
        logger.info("Reporte completo generado exitosamente")
        
        return report
    
    except Exception as e:
        logger.error(f"Error en generate_full_report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generando reporte: {str(e)}"
        )


@router.get(
    "/predefined-concepts",
    response_model=Dict[str, Any],
    summary="Listar conceptos predefinidos",
    description="""
    Obtiene los conceptos predefinidos disponibles organizados por categorías.
    
    Categorías:
    - **Generative AI in Education** (15 conceptos principales)
    - **Education and Learning** (conceptos educativos)
    - **AI Technical Concepts** (conceptos técnicos de IA)
    
    Útil para:
    - Ver qué conceptos están disponibles
    - Seleccionar conceptos para análisis personalizado
    - Entender la taxonomía de conceptos
    """
)
async def list_predefined_concepts():
    """
    Lista todos los conceptos predefinidos disponibles.
    
    Returns:
        Diccionario con categorías y conceptos
    """
    return {
        "generative_ai_education": GENERATIVE_AI_EDUCATION_CONCEPTS,
        "education_related": EDUCATION_RELATED_CONCEPTS,
        "ai_technical": AI_TECHNICAL_CONCEPTS
    }


@router.get(
    "/extraction-methods",
    response_model=List[Dict[str, str]],
    summary="Listar métodos de extracción",
    description="""
    Obtiene información sobre los métodos de extracción de keywords disponibles.
    
    Métodos:
    - **TF-IDF**: Método estadístico basado en frecuencia y rareza de términos
    - **Frequency**: Basado en frecuencia simple de aparición
    - **Combined**: Combina TF-IDF y frecuencia para mejor precisión
    """
)
async def list_extraction_methods():
    """
    Lista los métodos de extracción disponibles.
    
    Returns:
        Lista de métodos con descripciones
    """
    return [
        {
            "method": "tfidf",
            "name": "TF-IDF (Term Frequency-Inverse Document Frequency)",
            "description": "Método estadístico que evalúa la importancia de un término "
                          "en un documento relativo a un corpus. Ideal para textos científicos.",
            "best_for": "Documentos largos, identificación de términos distintivos"
        },
        {
            "method": "frequency",
            "name": "Frequency-based",
            "description": "Extrae los términos más frecuentes, eliminando stopwords. "
                          "Simple pero efectivo.",
            "best_for": "Análisis rápidos, identificación de términos comunes"
        },
        {
            "method": "combined",
            "name": "Combined (TF-IDF + Frequency)",
            "description": "Combina TF-IDF y frecuencia para balancear términos "
                          "distintivos y comunes.",
            "best_for": "Análisis comprehensivo, mejor precisión general"
        }
    ]


@router.get(
    "/health",
    summary="Health check",
    description="Verifica que el servicio de análisis de frecuencias esté funcionando."
)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Estado del servicio
    """
    try:
        # Verificar que el analizador se pueda inicializar
        analyzer = get_analyzer()
        
        return {
            "status": "healthy",
            "service": "Frequency Analysis API",
            "analyzer_initialized": analyzer is not None,
            "stopwords_loaded": len(analyzer.stopwords) if analyzer else 0,
            "version": "1.0.0"
        }
    
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )
