"""
API REST para Clustering Jerárquico
====================================

Endpoints para agrupamiento jerárquico de publicaciones científicas.

Requerimiento 4: Clustering Jerárquico

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Date: Octubre 2025
University: Universidad del Quindío - Análisis de Algoritmos
"""

from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from enum import Enum
import logging

from app.services.ml_analysis.clustering import (
    HierarchicalClustering,
    LinkageMethod,
    ClusteringResult
)

# Configurar logging
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(prefix="/clustering", tags=["Clustering"])


# ============================================================================
# MODELOS PYDANTIC
# ============================================================================

class ClusteringRequest(BaseModel):
    """Request para clustering jerárquico."""
    abstracts: List[str] = Field(
        ...,
        min_items=2,
        max_items=1000,
        description="Lista de abstracts a agrupar (mínimo 2)"
    )
    method: LinkageMethod = Field(
        default=LinkageMethod.WARD,
        description="Método de linkage: ward, average, o complete"
    )
    num_clusters: Optional[int] = Field(
        default=None,
        ge=2,
        description="Número de clusters (opcional, para cortar árbol)"
    )
    labels: Optional[List[str]] = Field(
        default=None,
        description="Etiquetas opcionales para documentos"
    )
    generate_dendrogram: bool = Field(
        default=True,
        description="Generar dendrograma visual"
    )
    
    @validator('labels')
    def validate_labels(cls, v, values):
        """Valida que las etiquetas coincidan con el número de abstracts."""
        if v is not None and 'abstracts' in values:
            if len(v) != len(values['abstracts']):
                raise ValueError(
                    f"Número de etiquetas ({len(v)}) no coincide con "
                    f"número de abstracts ({len(values['abstracts'])})"
                )
        return v


class CompareMethodsRequest(BaseModel):
    """Request para comparar múltiples métodos de clustering."""
    abstracts: List[str] = Field(
        ...,
        min_items=2,
        max_items=1000,
        description="Lista de abstracts a agrupar"
    )
    num_clusters: Optional[int] = Field(
        default=None,
        ge=2,
        description="Número de clusters para evaluación"
    )
    labels: Optional[List[str]] = Field(
        default=None,
        description="Etiquetas opcionales para documentos"
    )


class ClusteringResponse(BaseModel):
    """Response de clustering jerárquico."""
    method: str
    num_documents: int
    num_features: int
    cophenetic_correlation: float
    cluster_labels: Optional[List[int]] = None
    silhouette_score: Optional[float] = None
    davies_bouldin_score: Optional[float] = None
    calinski_harabasz_score: Optional[float] = None
    dendrogram_base64: Optional[str] = None


class ComparisonResponse(BaseModel):
    """Response de comparación de métodos."""
    methods: Dict[str, ClusteringResponse]
    best_method: str
    comparison_summary: Dict[str, Any]


# ============================================================================
# INSTANCIA GLOBAL
# ============================================================================

# Instancia global del clustering (inicializado una sola vez)
_clustering: Optional[HierarchicalClustering] = None


def get_clustering() -> HierarchicalClustering:
    """
    Obtiene o crea la instancia del clustering.
    
    Returns:
        Instancia de HierarchicalClustering
    """
    global _clustering
    
    if _clustering is None:
        logger.info("Inicializando HierarchicalClustering global...")
        _clustering = HierarchicalClustering(
            max_features=1000,
            ngram_range=(1, 3),
            min_df=1,
            max_df=0.95,
            use_idf=True
        )
        logger.info("HierarchicalClustering inicializado correctamente")
    
    return _clustering


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post(
    "/hierarchical",
    response_model=ClusteringResponse,
    summary="Ejecutar clustering jerárquico",
    description="""
    Ejecuta clustering jerárquico sobre abstracts científicos.
    
    **Proceso completo (4 pasos del Requerimiento 4):**
    
    1. **Preprocesamiento**: Convierte abstracts a vectores TF-IDF
       - Tokenización y limpieza de texto
       - Eliminación de stopwords
       - Vectorización con TF-IDF (n-gramas 1-3)
    
    2. **Cálculo de similitud**: Matriz de distancias coseno
       - Mide similitud semántica entre abstracts
       - Distancia coseno = 1 - similitud coseno
    
    3. **Clustering**: Aplica algoritmo jerárquico seleccionado
       - **Ward**: Minimiza varianza intra-cluster
       - **Average**: Promedio de distancias entre pares
       - **Complete**: Máxima distancia entre elementos
    
    4. **Dendrograma**: Genera visualización del árbol
       - Representación gráfica de la jerarquía
       - Imagen en formato base64
    
    **Métricas de coherencia:**
    - Correlación cofenética (0-1, mayor es mejor)
    - Silhouette Score (-1 a 1, mayor es mejor)
    - Davies-Bouldin Index (menor es mejor)
    - Calinski-Harabasz Index (mayor es mejor)
    
    Ejemplo:
    ```json
    {
      "abstracts": [
        "Machine learning enables personalized education...",
        "Generative AI models create customized content...",
        "Privacy concerns in educational AI systems..."
      ],
      "method": "ward",
      "num_clusters": 2,
      "generate_dendrogram": true
    }
    ```
    """
)
async def hierarchical_clustering(request: ClusteringRequest):
    """
    Ejecuta clustering jerárquico.
    
    Args:
        request: Datos de la petición
    
    Returns:
        Resultado del clustering con dendrograma
    """
    try:
        logger.info(
            f"Ejecutando clustering jerárquico: "
            f"método={request.method.value}, "
            f"documentos={len(request.abstracts)}, "
            f"clusters={request.num_clusters}"
        )
        
        # Obtener instancia de clustering
        clustering = get_clustering()
        
        # Ejecutar clustering
        result = clustering.cluster_texts(
            texts=request.abstracts,
            method=request.method,
            num_clusters=request.num_clusters,
            labels=request.labels,
            generate_plot=request.generate_dendrogram
        )
        
        # Construir respuesta
        response = ClusteringResponse(
            method=result.method,
            num_documents=result.num_documents,
            num_features=result.num_features,
            cophenetic_correlation=result.cophenetic_correlation,
            cluster_labels=result.cluster_labels.tolist() if result.cluster_labels is not None else None,
            silhouette_score=result.silhouette_score,
            davies_bouldin_score=result.davies_bouldin_score,
            calinski_harabasz_score=result.calinski_harabasz_score,
            dendrogram_base64=result.dendrogram_data.get('image_base64') if result.dendrogram_data else None
        )
        
        logger.info(
            f"Clustering completado: "
            f"correlación={result.cophenetic_correlation:.4f}, "
            f"features={result.num_features}"
        )
        
        return response
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error en hierarchical_clustering: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error ejecutando clustering: {str(e)}"
        )


@router.post(
    "/compare-methods",
    response_model=ComparisonResponse,
    summary="Comparar métodos de clustering",
    description="""
    Compara los 3 métodos de linkage para determinar cuál produce
    agrupamientos más coherentes.
    
    **Métodos comparados:**
    1. Ward Linkage
    2. Average Linkage (UPGMA)
    3. Complete Linkage
    
    **Criterios de comparación:**
    - Correlación cofenética (mayor es mejor)
    - Silhouette Score (mayor es mejor)
    - Davies-Bouldin Index (menor es mejor)
    - Calinski-Harabasz Index (mayor es mejor)
    
    **Recomendación automática:**
    El sistema calcula un score ponderado para cada método:
    - Correlación cofenética: peso 40%
    - Silhouette: peso 30%
    - Davies-Bouldin (invertido): peso 15%
    - Calinski-Harabasz (normalizado): peso 15%
    
    Retorna el método con el score más alto como "best_method".
    
    Ejemplo:
    ```json
    {
      "abstracts": ["Abstract 1...", "Abstract 2...", "Abstract 3..."],
      "num_clusters": 2
    }
    ```
    """
)
async def compare_clustering_methods(request: CompareMethodsRequest):
    """
    Compara los 3 métodos de clustering.
    
    Args:
        request: Datos de la petición
    
    Returns:
        Comparación de métodos con recomendación
    """
    try:
        logger.info(
            f"Comparando métodos de clustering: "
            f"documentos={len(request.abstracts)}, "
            f"clusters={request.num_clusters}"
        )
        
        # Obtener instancia de clustering
        clustering = get_clustering()
        
        # Comparar métodos
        results = clustering.compare_methods(
            texts=request.abstracts,
            num_clusters=request.num_clusters,
            labels=request.labels
        )
        
        # Construir respuestas individuales
        method_responses = {}
        for method_name, result in results.items():
            method_responses[method_name] = ClusteringResponse(
                method=result.method,
                num_documents=result.num_documents,
                num_features=result.num_features,
                cophenetic_correlation=result.cophenetic_correlation,
                cluster_labels=result.cluster_labels.tolist() if result.cluster_labels is not None else None,
                silhouette_score=result.silhouette_score,
                davies_bouldin_score=result.davies_bouldin_score,
                calinski_harabasz_score=result.calinski_harabasz_score,
                dendrogram_base64=result.dendrogram_data.get('image_base64') if result.dendrogram_data else None
            )
        
        # Determinar mejor método
        best_method = clustering._determine_best_method(results)
        
        # Construir resumen de comparación
        comparison_summary = {
            "cophenetic_correlations": {
                method: result.cophenetic_correlation
                for method, result in results.items()
            },
            "silhouette_scores": {
                method: result.silhouette_score
                for method, result in results.items()
                if result.silhouette_score is not None
            },
            "davies_bouldin_scores": {
                method: result.davies_bouldin_score
                for method, result in results.items()
                if result.davies_bouldin_score is not None
            }
        }
        
        # Respuesta final
        response = ComparisonResponse(
            methods=method_responses,
            best_method=best_method,
            comparison_summary=comparison_summary
        )
        
        logger.info(f"Comparación completada: mejor método={best_method}")
        
        return response
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error en compare_clustering_methods: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error comparando métodos: {str(e)}"
        )


@router.get(
    "/methods",
    response_model=List[Dict[str, str]],
    summary="Listar métodos de linkage",
    description="""
    Obtiene información sobre los métodos de linkage disponibles.
    
    **Métodos disponibles:**
    
    1. **Ward Linkage**
       - Minimiza la suma de cuadrados dentro de clusters
       - Produce clusters balanceados y compactos
       - Recomendado para clusters de tamaño similar
    
    2. **Average Linkage (UPGMA)**
       - Promedio de todas las distancias entre pares
       - Menos sensible a outliers que Complete
       - Balance entre Ward y Complete
    
    3. **Complete Linkage**
       - Máxima distancia entre cualquier par de elementos
       - Evita cadenas largas de elementos
       - Produce clusters muy compactos
    """
)
async def list_linkage_methods():
    """
    Lista todos los métodos de linkage disponibles.
    
    Returns:
        Lista de métodos con descripciones
    """
    return [
        {
            "method": "ward",
            "name": "Ward Linkage",
            "description": "Minimiza la varianza intra-cluster. Produce clusters balanceados y compactos.",
            "formula": "d(A,B) = sqrt(|A||B| / (|A| + |B|)) * ||mean(A) - mean(B)||",
            "use_case": "Recomendado cuando se espera que los clusters tengan tamaños similares."
        },
        {
            "method": "average",
            "name": "Average Linkage (UPGMA)",
            "description": "Promedio de distancias entre todos los pares de elementos.",
            "formula": "d(A,B) = (1 / |A||B|) * Σ Σ d(a,b) para a∈A, b∈B",
            "use_case": "Balance entre Ward y Complete. Menos sensible a outliers."
        },
        {
            "method": "complete",
            "name": "Complete Linkage",
            "description": "Máxima distancia entre cualquier par de elementos de diferentes clusters.",
            "formula": "d(A,B) = max{d(a,b) : a∈A, b∈B}",
            "use_case": "Produce clusters muy compactos. Evita cadenas largas de elementos."
        }
    ]


@router.get(
    "/health",
    summary="Health check del clustering",
    description="Verifica que el sistema de clustering esté operativo."
)
async def health_check():
    """
    Verifica el estado del sistema de clustering.
    
    Returns:
        Estado del sistema
    """
    try:
        clustering = get_clustering()
        return {
            "status": "healthy",
            "clustering_initialized": clustering is not None,
            "max_features": clustering.max_features,
            "ngram_range": clustering.ngram_range
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Clustering no disponible: {str(e)}"
        )
