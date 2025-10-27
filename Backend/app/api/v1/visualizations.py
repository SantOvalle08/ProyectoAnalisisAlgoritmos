"""
API REST para Visualizaciones Bibliométricas
============================================

Endpoints para generación de visualizaciones interactivas de análisis
bibliométrico.

Requerimiento 5: Visualizaciones

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Date: Octubre 2025
University: Universidad del Quindío - Análisis de Algoritmos
"""

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
import tempfile
import os

from app.services.visualization import (
    WordCloudGenerator,
    GeographicHeatmap,
    TimelineChart,
    PDFExporter
)

# Configurar logging
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(prefix="/visualizations", tags=["Visualizations"])


# ============================================================================
# MODELOS PYDANTIC
# ============================================================================

class PublicationInput(BaseModel):
    """Publicación para visualización."""
    abstract: Optional[str] = None
    keywords: Optional[List[str]] = None
    authors: Optional[List[Dict[str, Any]]] = None
    year: Optional[int] = None
    journal: Optional[str] = None


class WordCloudRequest(BaseModel):
    """Request para nube de palabras."""
    publications: List[PublicationInput] = Field(
        ...,
        min_length=1,
        description="Lista de publicaciones a analizar"
    )
    include_keywords: bool = Field(
        default=True,
        description="Incluir keywords en el análisis"
    )
    use_tfidf: bool = Field(
        default=True,
        description="Usar TF-IDF para ponderación"
    )
    max_words: int = Field(
        default=100,
        ge=10,
        le=200,
        description="Número máximo de palabras"
    )
    title: Optional[str] = Field(
        default=None,
        description="Título de la visualización"
    )


class HeatmapRequest(BaseModel):
    """Request para mapa de calor geográfico."""
    publications: List[PublicationInput] = Field(
        ...,
        min_length=1,
        description="Lista de publicaciones a analizar"
    )
    map_type: str = Field(
        default="choropleth",
        description="Tipo de visualización: 'choropleth' o 'bar'"
    )
    title: Optional[str] = Field(
        default=None,
        description="Título del mapa"
    )
    top_n: int = Field(
        default=15,
        ge=5,
        le=30,
        description="Para gráfico de barras, número de países"
    )


class TimelineRequest(BaseModel):
    """Request para línea temporal."""
    publications: List[PublicationInput] = Field(
        ...,
        min_length=1,
        description="Lista de publicaciones a analizar"
    )
    group_by_journal: bool = Field(
        default=True,
        description="Agrupar por revista/conferencia"
    )
    top_n_journals: int = Field(
        default=10,
        ge=3,
        le=20,
        description="Número de revistas principales"
    )
    title: Optional[str] = Field(
        default=None,
        description="Título del gráfico"
    )


class PDFExportRequest(BaseModel):
    """Request para exportación a PDF."""
    publications: List[PublicationInput] = Field(
        ...,
        min_length=1,
        description="Lista de publicaciones a analizar"
    )
    include_wordcloud: bool = Field(default=True)
    include_heatmap: bool = Field(default=False)  # Requiere conversión HTML
    include_timeline: bool = Field(default=False)  # Requiere conversión HTML
    title: str = Field(
        default="Análisis Bibliométrico",
        description="Título del documento"
    )


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post(
    "/wordcloud",
    summary="Generar nube de palabras",
    description="""
    Genera una nube de palabras dinámica a partir de abstracts y keywords.
    
    **Proceso:**
    1. Extrae términos de abstracts y keywords
    2. Filtra stopwords (inglés, español, técnicas)
    3. Pondera términos usando TF-IDF (opcional)
    4. Genera visualización con matplotlib/wordcloud
    5. Retorna imagen en base64
    
    **Características:**
    - Actualización dinámica con nuevas publicaciones
    - Ponderación inteligente con TF-IDF
    - Filtrado automático de términos irrelevantes
    - Top 20 términos principales incluidos
    
    Ejemplo:
    ```json
    {
      "publications": [
        {
          "abstract": "Machine learning algorithms...",
          "keywords": ["AI", "education", "learning"]
        }
      ],
      "max_words": 100,
      "use_tfidf": true
    }
    ```
    """
)
async def generate_wordcloud(request: WordCloudRequest):
    """
    Genera nube de palabras.
    
    Args:
        request: Datos de la petición
    
    Returns:
        Diccionario con imagen base64 y estadísticas
    """
    try:
        logger.info(
            f"Generando wordcloud: {len(request.publications)} publicaciones"
        )
        
        # Crear generador
        generator = WordCloudGenerator(
            max_words=request.max_words,
            colormap='viridis'
        )
        
        # Convertir publicaciones a diccionarios
        publications = [pub.dict() for pub in request.publications]
        
        # Generar wordcloud
        result = generator.generate_from_publications(
            publications=publications,
            include_keywords=request.include_keywords,
            use_tfidf=request.use_tfidf,
            title=request.title
        )
        
        logger.info(
            f"Wordcloud generado: {result['total_terms']} términos únicos"
        )
        
        return result
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error generando wordcloud: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generando nube de palabras: {str(e)}"
        )


@router.post(
    "/heatmap",
    summary="Generar mapa de calor geográfico",
    description="""
    Genera mapa de calor mostrando distribución geográfica de publicaciones
    según el país del primer autor.
    
    **Proceso:**
    1. Extrae afiliación del primer autor de cada publicación
    2. Identifica país mediante búsqueda en afiliación
    3. Cuenta publicaciones por país
    4. Genera visualización interactiva con plotly
    
    **Tipos de visualización:**
    - **choropleth**: Mapa mundial coloreado por frecuencia
    - **bar**: Gráfico de barras con top N países
    
    **Países soportados:** 60+ países con códigos ISO
    
    Ejemplo:
    ```json
    {
      "publications": [
        {
          "authors": [
            {"affiliation": "University of X, United States"}
          ]
        }
      ],
      "map_type": "choropleth"
    }
    ```
    """
)
async def generate_heatmap(request: HeatmapRequest):
    """
    Genera mapa de calor geográfico.
    
    Args:
        request: Datos de la petición
    
    Returns:
        HTML interactivo del mapa
    """
    try:
        logger.info(
            f"Generando mapa de calor: {len(request.publications)} publicaciones"
        )
        
        # Crear generador
        generator = GeographicHeatmap(colorscale='Viridis')
        
        # Convertir publicaciones
        publications = [pub.dict() for pub in request.publications]
        
        # Generar mapa
        result = generator.generate_from_publications(
            publications=publications,
            map_type=request.map_type,
            title=request.title,
            top_n=request.top_n
        )
        
        logger.info(
            f"Mapa generado: {result['num_countries']} países"
        )
        
        # Retornar JSON con HTML y metadatos
        return {
            "html": result['html'],
            "country_distribution": result['country_distribution'],
            "num_publications": result['num_publications'],
            "num_countries": result['num_countries']
        }
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error generando mapa: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generando mapa de calor: {str(e)}"
        )


@router.post(
    "/timeline",
    summary="Generar línea temporal",
    description="""
    Genera gráfico de línea temporal mostrando evolución de publicaciones
    por año y opcionalmente por revista/conferencia.
    
    **Proceso:**
    1. Extrae año de publicación de cada artículo
    2. Extrae nombre de revista/conferencia (opcional)
    3. Agrupa y cuenta publicaciones
    4. Identifica top N revistas principales
    5. Genera visualización interactiva con plotly
    
    **Modos de agrupación:**
    - **Por año solamente**: Serie única mostrando total por año
    - **Por año y revista**: Múltiples series, una por revista principal
    
    Ejemplo:
    ```json
    {
      "publications": [
        {
          "year": 2023,
          "journal": "Journal of AI"
        }
      ],
      "group_by_journal": true,
      "top_n_journals": 10
    }
    ```
    """
)
async def generate_timeline(request: TimelineRequest):
    """
    Genera línea temporal.
    
    Args:
        request: Datos de la petición
    
    Returns:
        HTML interactivo del gráfico
    """
    try:
        logger.info(
            f"Generando timeline: {len(request.publications)} publicaciones"
        )
        
        # Crear generador
        generator = TimelineChart(colorscale='Set2')
        
        # Convertir publicaciones
        publications = [pub.dict() for pub in request.publications]
        
        # Generar timeline
        result = generator.generate_from_publications(
            publications=publications,
            group_by_journal=request.group_by_journal,
            top_n_journals=request.top_n_journals,
            title=request.title
        )
        
        logger.info(
            f"Timeline generado: {result['year_range']}"
        )
        
        # Retornar JSON con HTML y metadatos
        return {
            "html": result['html'],
            "yearly_distribution": result['yearly_distribution'],
            "num_publications": result['num_publications'],
            "year_range": result['year_range']
        }
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error generando timeline: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generando línea temporal: {str(e)}"
        )


@router.post(
    "/export-pdf",
    summary="Exportar visualizaciones a PDF",
    description="""
    Exporta visualizaciones a un documento PDF profesional.
    
    **Incluye:**
    - Portada con metadatos
    - Nube de palabras (PNG de alta calidad)
    - Términos principales
    - Estadísticas del análisis
    
    **Nota:** Los mapas de calor y líneas temporales son visualizaciones
    HTML interactivas que requieren conversión adicional para incluirse
    en PDF (no implementado en versión actual).
    
    Ejemplo:
    ```json
    {
      "publications": [...],
      "include_wordcloud": true,
      "title": "Análisis Bibliométrico de IA Generativa"
    }
    ```
    """
)
async def export_pdf(request: PDFExportRequest):
    """
    Exporta visualizaciones a PDF.
    
    Args:
        request: Datos de la petición
    
    Returns:
        Archivo PDF
    """
    try:
        logger.info(
            f"Generando PDF: {len(request.publications)} publicaciones"
        )
        
        # Preparar visualizaciones
        visualizations = {}
        metadata = {
            'num_publications': len(request.publications),
        }
        
        # Convertir publicaciones
        publications = [pub.dict() for pub in request.publications]
        
        # WordCloud
        if request.include_wordcloud:
            wc_generator = WordCloudGenerator(max_words=100)
            wordcloud_data = wc_generator.generate_from_publications(
                publications=publications,
                include_keywords=True,
                use_tfidf=True
            )
            visualizations['wordcloud'] = wordcloud_data
            
            # Agregar a metadata
            metadata['total_terms'] = wordcloud_data.get('total_terms')
        
        # Extraer rango de años para metadata
        years = []
        for pub in publications:
            if 'year' in pub and pub['year']:
                years.append(pub['year'])
        
        if years:
            metadata['year_min'] = min(years)
            metadata['year_max'] = max(years)
        
        # Generar PDF
        exporter = PDFExporter(title=request.title)
        pdf_bytes = exporter.export_visualizations(
            visualizations=visualizations,
            metadata=metadata
        )
        
        logger.info("PDF generado exitosamente")
        
        # Retornar como respuesta
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=analisis_bibliometrico.pdf"
            }
        )
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error generando PDF: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error exportando a PDF: {str(e)}"
        )


@router.get(
    "/health",
    summary="Health check de visualizaciones",
    description="Verifica que el sistema de visualizaciones esté operativo."
)
async def health_check():
    """
    Health check del sistema de visualizaciones.
    
    Returns:
        Estado del sistema
    """
    return {
        "status": "healthy",
        "modules": {
            "wordcloud": "operational",
            "heatmap": "operational",
            "timeline": "operational",
            "pdf_export": "operational"
        }
    }
