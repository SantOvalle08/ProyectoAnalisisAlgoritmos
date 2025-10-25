"""
API REST para Algoritmos de Similitud de Textos
================================================

Endpoints para comparar la similitud entre abstracts de publicaciones
utilizando 6 algoritmos diferentes (4 clásicos + 2 con IA).

Requerimiento 2: Algoritmos de Similitud de Texto

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Date: Octubre 2025
University: Universidad del Quindío - Análisis de Algoritmos
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Dict, Any, List, Optional, Literal
from enum import Enum
import logging

from app.services.ml_analysis.similarity import (
    LevenshteinSimilarity,
    TFIDFCosineSimilarity,
    JaccardSimilarity,
    NGramSimilarity,
    BERTEmbeddingsSimilarity,
    SentenceBERTSimilarity
)

# Configurar logging
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(prefix="/similarity", tags=["Similarity Analysis - Requerimiento 2"])


# ============================================================================
# MODELOS PYDANTIC
# ============================================================================

class AlgorithmType(str, Enum):
    """Tipos de algoritmos disponibles."""
    LEVENSHTEIN = "levenshtein"
    TFIDF_COSINE = "tfidf_cosine"
    JACCARD = "jaccard"
    NGRAM = "ngram"
    BERT = "bert"
    SENTENCE_BERT = "sentence_bert"
    ALL = "all"  # Ejecutar todos los algoritmos


class CompareRequest(BaseModel):
    """Request para comparar dos textos."""
    text1: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Primer texto a comparar (ej: abstract de publicación 1)"
    )
    text2: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Segundo texto a comparar (ej: abstract de publicación 2)"
    )
    algorithm: AlgorithmType = Field(
        default=AlgorithmType.SENTENCE_BERT,
        description="Algoritmo a utilizar para la comparación"
    )
    
    # Parámetros opcionales para algoritmos específicos
    ngram_n: Optional[int] = Field(
        default=3,
        ge=1,
        le=10,
        description="Tamaño de n-gramas (solo para algoritmo ngram)"
    )
    ngram_type: Optional[Literal['char', 'word']] = Field(
        default='char',
        description="Tipo de n-gramas: 'char' o 'word'"
    )
    jaccard_use_char_ngrams: Optional[bool] = Field(
        default=False,
        description="Usar n-gramas de caracteres en Jaccard (default: tokens)"
    )
    bert_pooling: Optional[Literal['cls', 'mean']] = Field(
        default='mean',
        description="Estrategia de pooling para BERT"
    )
    tfidf_max_features: Optional[int] = Field(
        default=5000,
        ge=100,
        le=50000,
        description="Número máximo de features para TF-IDF"
    )
    
    @field_validator('text1', 'text2')
    @classmethod
    def validate_text_not_empty(cls, v):
        """Valida que los textos no estén vacíos o solo con espacios."""
        if not v or not v.strip():
            raise ValueError("El texto no puede estar vacío")
        return v.strip()


class AnalyzeRequest(BaseModel):
    """Request para análisis detallado paso a paso."""
    text1: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Primer texto a analizar"
    )
    text2: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Segundo texto a analizar"
    )
    algorithm: AlgorithmType = Field(
        ...,
        description="Algoritmo a utilizar (no puede ser 'all')"
    )
    
    # Mismos parámetros opcionales que CompareRequest
    ngram_n: Optional[int] = Field(default=3, ge=1, le=10)
    ngram_type: Optional[Literal['char', 'word']] = Field(default='char')
    jaccard_use_char_ngrams: Optional[bool] = Field(default=False)
    bert_pooling: Optional[Literal['cls', 'mean']] = Field(default='mean')
    tfidf_max_features: Optional[int] = Field(default=5000, ge=100, le=50000)
    
    @field_validator('algorithm')
    @classmethod
    def validate_algorithm_not_all(cls, v):
        """Valida que no se use 'all' para análisis detallado."""
        if v == AlgorithmType.ALL:
            raise ValueError("Para análisis detallado, especifica un algoritmo (no 'all')")
        return v


class BatchCompareRequest(BaseModel):
    """Request para comparar múltiples pares de textos."""
    pairs: List[Dict[str, str]] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Lista de pares de textos a comparar"
    )
    algorithm: AlgorithmType = Field(
        default=AlgorithmType.SENTENCE_BERT,
        description="Algoritmo a utilizar"
    )
    
    @field_validator('pairs')
    @classmethod
    def validate_pairs_format(cls, v):
        """Valida formato de los pares."""
        for i, pair in enumerate(v):
            if 'text1' not in pair or 'text2' not in pair:
                raise ValueError(f"Par {i}: debe contener 'text1' y 'text2'")
            if not pair['text1'].strip() or not pair['text2'].strip():
                raise ValueError(f"Par {i}: los textos no pueden estar vacíos")
        return v


class SimilarityResult(BaseModel):
    """Resultado de comparación de similitud."""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "algorithm": "Sentence-BERT Similarity",
            "algorithm_type": "AI-Based",
            "similarity": 0.85,
            "similarity_percentage": "85.00%",
            "execution_time_seconds": 0.023
        }
    })
    
    algorithm: str
    algorithm_type: str
    similarity: float = Field(ge=0.0, le=1.0, description="Similitud entre 0 y 1")
    similarity_percentage: str
    execution_time_seconds: Optional[float] = None


class AlgorithmInfo(BaseModel):
    """Información sobre un algoritmo de similitud."""
    id: str
    name: str
    type: str
    description: str
    complexity: str
    best_use_cases: List[str]
    parameters: Dict[str, Any]


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def get_algorithm_instance(algorithm: AlgorithmType, **kwargs):
    """
    Instancia el algoritmo especificado con sus parámetros.
    
    Args:
        algorithm: Tipo de algoritmo
        **kwargs: Parámetros específicos del algoritmo
    
    Returns:
        Instancia del algoritmo de similitud
    """
    try:
        if algorithm == AlgorithmType.LEVENSHTEIN:
            return LevenshteinSimilarity()
        
        elif algorithm == AlgorithmType.TFIDF_COSINE:
            max_features = kwargs.get('tfidf_max_features', 5000)
            return TFIDFCosineSimilarity(max_features=max_features)
        
        elif algorithm == AlgorithmType.JACCARD:
            use_char_ngrams = kwargs.get('jaccard_use_char_ngrams', False)
            return JaccardSimilarity(
                use_char_ngrams=use_char_ngrams,
                remove_stopwords=True
            )
        
        elif algorithm == AlgorithmType.NGRAM:
            n = kwargs.get('ngram_n', 3)
            ngram_type = kwargs.get('ngram_type', 'char')
            return NGramSimilarity(
                n=n,
                ngram_type=ngram_type,
                similarity_metric='dice'
            )
        
        elif algorithm == AlgorithmType.BERT:
            pooling = kwargs.get('bert_pooling', 'mean')
            return BERTEmbeddingsSimilarity(
                model_name='bert-base-uncased',
                pooling_strategy=pooling
            )
        
        elif algorithm == AlgorithmType.SENTENCE_BERT:
            return SentenceBERTSimilarity(
                model_name='all-MiniLM-L6-v2'
            )
        
        else:
            raise ValueError(f"Algoritmo no soportado: {algorithm}")
    
    except Exception as e:
        logger.error(f"Error instanciando algoritmo {algorithm}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error inicializando algoritmo: {str(e)}"
        )


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post(
    "/compare",
    response_model=SimilarityResult,
    summary="Comparar dos textos",
    description="""
    Calcula la similitud entre dos textos usando el algoritmo especificado.
    
    **Algoritmos disponibles:**
    - `levenshtein`: Distancia de edición (bueno para textos cortos)
    - `tfidf_cosine`: TF-IDF + Coseno (bueno para documentos)
    - `jaccard`: Coeficiente de Jaccard (conjuntos de tokens)
    - `ngram`: Similitud por n-gramas (secuencias contiguas)
    - `bert`: BERT embeddings (mejor para semántica)
    - `sentence_bert`: Sentence-BERT (rápido + semántica)
    
    **Ejemplo de uso:**
    ```json
    {
      "text1": "Generative AI in education enables personalized learning",
      "text2": "AI-powered educational tools create customized content",
      "algorithm": "sentence_bert"
    }
    ```
    """
)
async def compare_texts(request: CompareRequest):
    """
    Compara dos textos y retorna la similitud.
    
    Args:
        request: Datos de la petición
    
    Returns:
        Resultado de similitud
    """
    import time
    
    try:
        logger.info(f"Comparing texts with algorithm: {request.algorithm}")
        
        start_time = time.time()
        
        # Instanciar algoritmo
        algo = get_algorithm_instance(
            request.algorithm,
            ngram_n=request.ngram_n,
            ngram_type=request.ngram_type,
            jaccard_use_char_ngrams=request.jaccard_use_char_ngrams,
            bert_pooling=request.bert_pooling,
            tfidf_max_features=request.tfidf_max_features
        )
        
        # Calcular similitud
        similarity = algo.calculate_similarity(request.text1, request.text2)
        
        execution_time = time.time() - start_time
        
        logger.info(f"Similarity: {similarity:.4f}, Time: {execution_time:.2f}s")
        
        return SimilarityResult(
            algorithm=algo.name,
            algorithm_type=algo.algorithm_type.value,
            similarity=similarity,
            similarity_percentage=f"{similarity * 100:.2f}%",
            execution_time_seconds=round(execution_time, 4)
        )
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error in compare_texts: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error calculando similitud: {str(e)}"
        )


@router.post(
    "/compare-all",
    response_model=Dict[str, SimilarityResult],
    summary="Comparar con todos los algoritmos",
    description="""
    Compara dos textos usando TODOS los 6 algoritmos disponibles.
    Útil para comparar rendimiento y resultados entre diferentes enfoques.
    
    **Ejemplo de uso:**
    ```json
    {
      "text1": "Generative AI in education",
      "text2": "AI-powered educational tools"
    }
    ```
    
    **Ejemplo de respuesta:**
    ```json
    {
      "levenshtein": {"similarity": 0.38, ...},
      "tfidf_cosine": {"similarity": 0.62, ...},
      "jaccard": {"similarity": 0.50, ...},
      "ngram": {"similarity": 0.67, ...},
      "bert": {"similarity": 0.96, ...},
      "sentence_bert": {"similarity": 0.89, ...}
    }
    ```
    """
)
async def compare_all_algorithms(request: CompareRequest):
    """
    Compara dos textos con todos los algoritmos disponibles.
    
    Args:
        request: Datos de la petición (text1 y text2)
    
    Returns:
        Diccionario con resultados de cada algoritmo
    """
    text1 = request.text1
    text2 = request.text2
    import time
    
    try:
        logger.info("Comparing texts with ALL algorithms")
        
        results = {}
        
        # Lista de todos los algoritmos (excepto 'all')
        algorithms = [
            AlgorithmType.LEVENSHTEIN,
            AlgorithmType.TFIDF_COSINE,
            AlgorithmType.JACCARD,
            AlgorithmType.NGRAM,
            AlgorithmType.BERT,
            AlgorithmType.SENTENCE_BERT
        ]
        
        for algorithm in algorithms:
            try:
                start_time = time.time()
                
                algo = get_algorithm_instance(algorithm)
                similarity = algo.calculate_similarity(text1, text2)
                
                execution_time = time.time() - start_time
                
                results[algorithm.value] = SimilarityResult(
                    algorithm=algo.name,
                    algorithm_type=algo.algorithm_type.value,
                    similarity=similarity,
                    similarity_percentage=f"{similarity * 100:.2f}%",
                    execution_time_seconds=round(execution_time, 4)
                )
                
            except Exception as e:
                logger.error(f"Error with algorithm {algorithm}: {str(e)}")
                # Continuar con los demás algoritmos
                results[algorithm.value] = {
                    "error": str(e),
                    "algorithm": algorithm.value
                }
        
        return results
    
    except Exception as e:
        logger.error(f"Error in compare_all_algorithms: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error en comparación múltiple: {str(e)}"
        )


@router.post(
    "/analyze",
    response_model=Dict[str, Any],
    summary="Análisis detallado paso a paso",
    description="""
    Realiza un análisis completo paso a paso del cálculo de similitud,
    incluyendo explicaciones matemáticas, estadísticas y visualizaciones.
    
    **Ideal para:**
    - Entender cómo funciona cada algoritmo
    - Debugging y validación
    - Reportes académicos
    - Visualización de resultados intermedios
    """
)
async def analyze_step_by_step(request: AnalyzeRequest):
    """
    Análisis detallado del cálculo de similitud.
    
    Args:
        request: Datos de la petición
    
    Returns:
        Análisis completo con explicaciones
    """
    try:
        logger.info(f"Detailed analysis with algorithm: {request.algorithm}")
        
        # Instanciar algoritmo
        algo = get_algorithm_instance(
            request.algorithm,
            ngram_n=request.ngram_n,
            ngram_type=request.ngram_type,
            jaccard_use_char_ngrams=request.jaccard_use_char_ngrams,
            bert_pooling=request.bert_pooling,
            tfidf_max_features=request.tfidf_max_features
        )
        
        # Ejecutar análisis detallado
        analysis = algo.analyze_step_by_step(request.text1, request.text2)
        
        logger.info("Analysis completed successfully")
        
        return analysis
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error in analyze_step_by_step: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error en análisis detallado: {str(e)}"
        )


@router.post(
    "/batch",
    response_model=List[SimilarityResult],
    summary="Comparación por lotes",
    description="""
    Compara múltiples pares de textos en una sola petición.
    
    **Límite:** Máximo 100 pares por petición.
    
    **Ejemplo:**
    ```json
    {
      "pairs": [
        {"text1": "...", "text2": "..."},
        {"text1": "...", "text2": "..."}
      ],
      "algorithm": "sentence_bert"
    }
    ```
    """
)
async def batch_compare(request: BatchCompareRequest):
    """
    Compara múltiples pares de textos.
    
    Args:
        request: Lista de pares y algoritmo
    
    Returns:
        Lista de resultados
    """
    import time
    
    try:
        logger.info(f"Batch comparison: {len(request.pairs)} pairs")
        
        # Instanciar algoritmo una sola vez
        algo = get_algorithm_instance(request.algorithm)
        
        results = []
        
        for i, pair in enumerate(request.pairs):
            try:
                start_time = time.time()
                
                similarity = algo.calculate_similarity(
                    pair['text1'],
                    pair['text2']
                )
                
                execution_time = time.time() - start_time
                
                results.append(SimilarityResult(
                    algorithm=algo.name,
                    algorithm_type=algo.algorithm_type.value,
                    similarity=similarity,
                    similarity_percentage=f"{similarity * 100:.2f}%",
                    execution_time_seconds=round(execution_time, 4)
                ))
                
            except Exception as e:
                logger.error(f"Error processing pair {i}: {str(e)}")
                # Agregar resultado con error
                results.append({
                    "error": str(e),
                    "pair_index": i
                })
        
        logger.info(f"Batch comparison completed: {len(results)} results")
        
        return results
    
    except Exception as e:
        logger.error(f"Error in batch_compare: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error en comparación por lotes: {str(e)}"
        )


@router.get(
    "/algorithms",
    response_model=List[AlgorithmInfo],
    summary="Listar algoritmos disponibles",
    description="""
    Obtiene información detallada sobre todos los algoritmos de similitud disponibles.
    
    **Incluye:**
    - Nombre y descripción
    - Complejidad computacional
    - Casos de uso recomendados
    - Parámetros configurables
    """
)
async def list_algorithms():
    """
    Lista todos los algoritmos disponibles con su información.
    
    Returns:
        Lista de información de algoritmos
    """
    algorithms = [
        AlgorithmInfo(
            id="levenshtein",
            name="Levenshtein Distance",
            type="Classical - Edit Distance",
            description="Calcula la distancia de edición mínima entre dos textos. "
                        "Mide cuántas operaciones (inserción, eliminación, sustitución) "
                        "se necesitan para transformar un texto en otro.",
            complexity="O(m × n) tiempo, O(m × n) espacio con matriz DP completa",
            best_use_cases=[
                "Detección de errores tipográficos",
                "Textos cortos (títulos, nombres)",
                "Corrección ortográfica",
                "Comparación character-level"
            ],
            parameters={}
        ),
        AlgorithmInfo(
            id="tfidf_cosine",
            name="TF-IDF + Cosine Similarity",
            type="Classical - Statistical",
            description="Vectoriza textos usando TF-IDF (Term Frequency-Inverse Document Frequency) "
                        "y calcula similitud del coseno entre vectores. Captura importancia "
                        "estadística de términos.",
            complexity="O(n + d) donde n=tokens, d=dimensión vocabulario",
            best_use_cases=[
                "Documentos largos",
                "Búsqueda de información",
                "Detección de plagio",
                "Recuperación de documentos similares"
            ],
            parameters={
                "tfidf_max_features": {
                    "type": "int",
                    "default": 5000,
                    "range": "100-50000",
                    "description": "Máximo número de términos en vocabulario"
                }
            }
        ),
        AlgorithmInfo(
            id="jaccard",
            name="Jaccard Coefficient",
            type="Classical - Set-based",
            description="Mide similitud como intersección dividida por unión de conjuntos "
                        "de tokens o n-gramas. Simple pero efectivo para textos con "
                        "vocabulario común.",
            complexity="O(n + m) donde n, m son tamaños de conjuntos",
            best_use_cases=[
                "Comparación de palabras clave",
                "Detección de duplicados aproximados",
                "Análisis de co-ocurrencia",
                "Textos con vocabulario limitado"
            ],
            parameters={
                "jaccard_use_char_ngrams": {
                    "type": "bool",
                    "default": False,
                    "description": "Usar n-gramas de caracteres en vez de tokens"
                }
            }
        ),
        AlgorithmInfo(
            id="ngram",
            name="N-gram Similarity",
            type="Classical - Sequence-based",
            description="Compara textos mediante n-gramas (secuencias contiguas de n elementos). "
                        "Soporta 3 métricas: Dice, Jaccard y Coseno. Captura estructura local.",
            complexity="O(n) para extracción + O(k) para comparación",
            best_use_cases=[
                "Detección de plagio",
                "Textos con estructura similar",
                "Análisis de patrones locales",
                "Balance entre precisión y eficiencia"
            ],
            parameters={
                "ngram_n": {
                    "type": "int",
                    "default": 3,
                    "range": "1-10",
                    "description": "Tamaño de n-gramas"
                },
                "ngram_type": {
                    "type": "str",
                    "default": "char",
                    "options": ["char", "word"],
                    "description": "Tipo de n-gramas"
                }
            }
        ),
        AlgorithmInfo(
            id="bert",
            name="BERT Embeddings + Cosine",
            type="AI-based - Transformer",
            description="Usa BERT (Bidirectional Encoder Representations from Transformers) "
                        "para generar embeddings contextuales densos de 768 dimensiones. "
                        "Captura significado semántico profundo mediante atención multi-cabeza.",
            complexity="O(n²) por atención self-attention, ~400MB modelo",
            best_use_cases=[
                "Similitud semántica profunda",
                "Textos con contexto complejo",
                "Análisis académico/científico",
                "Alta precisión (sacrificando velocidad)"
            ],
            parameters={
                "bert_pooling": {
                    "type": "str",
                    "default": "mean",
                    "options": ["cls", "mean"],
                    "description": "Estrategia de pooling: 'cls' usa token [CLS], 'mean' promedia"
                }
            }
        ),
        AlgorithmInfo(
            id="sentence_bert",
            name="Sentence-BERT",
            type="AI-based - Optimized Transformer",
            description="Versión optimizada de BERT específicamente entrenada para similitud "
                        "de oraciones usando redes siamesas. 5-10x más rápido que BERT con "
                        "calidad similar. Embeddings de 384 dimensiones pre-normalizados.",
            complexity="O(n) por texto, ~80MB modelo",
            best_use_cases=[
                "Similitud semántica a escala",
                "Búsqueda en tiempo real",
                "Comparación de abstracts",
                "Balance óptimo: precisión + velocidad"
            ],
            parameters={}
        )
    ]
    
    return algorithms


@router.get(
    "/health",
    summary="Health check",
    description="Verifica que el servicio de similitud esté funcionando correctamente."
)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Estado del servicio
    """
    return {
        "status": "healthy",
        "service": "Similarity Analysis API",
        "algorithms_available": 6,
        "version": "1.0.0"
    }
