"""
API Endpoints para Adquisición de Datos
========================================

Endpoints REST para automatización de descarga de datos científicos.

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Course: Análisis de Algoritmos (2025-2), Universidad del Quindío
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Path
from fastapi.responses import FileResponse
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
import logging
from pathlib import Path as FilePath

from app.services.data_acquisition.unified_downloader import UnifiedDownloader
from app.services.data_acquisition.base_scraper import ExportFormat

logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(
    prefix="/data",
    tags=["Data Acquisition - Requerimiento 1"]
)

# Instancia global del downloader
downloader = UnifiedDownloader(
    similarity_threshold=0.95,
    rate_limit=1.0,
    output_dir="data/downloads"
)


class DataSource(str, Enum):
    """Fuentes de datos disponibles."""
    CROSSREF = "crossref"
    ACM = "acm"
    SAGE = "sage"
    SCIENCEDIRECT = "sciencedirect"


class DownloadRequest(BaseModel):
    """Request para iniciar descarga de datos."""
    
    query: str = Field(
        ...,
        description="Cadena de búsqueda (ej: 'generative artificial intelligence')",
        min_length=3,
        max_length=500,
        examples=["generative artificial intelligence"]
    )
    
    sources: List[DataSource] = Field(
        ...,
        description="Lista de fuentes de datos a consultar",
        min_length=1,
        examples=[["crossref", "acm"]]
    )
    
    max_results_per_source: int = Field(
        default=100,
        description="Número máximo de resultados por fuente",
        ge=1,
        le=1000
    )
    
    start_year: Optional[int] = Field(
        None,
        description="Año de inicio para filtrar resultados",
        ge=1900,
        le=2100
    )
    
    end_year: Optional[int] = Field(
        None,
        description="Año final para filtrar resultados",
        ge=1900,
        le=2100
    )
    
    export_formats: List[ExportFormat] = Field(
        default=[ExportFormat.JSON, ExportFormat.BIBTEX],
        description="Formatos de exportación deseados"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "generative artificial intelligence",
                "sources": ["crossref"],
                "max_results_per_source": 100,
                "start_year": 2023,
                "end_year": 2024,
                "export_formats": ["json", "bibtex"]
            }
        }
    }


class DownloadResponse(BaseModel):
    """Response de inicio de descarga."""
    
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    job_id: str = Field(..., description="ID único del job de descarga")
    status: str = Field(..., description="Estado del job")
    message: str = Field(..., description="Mensaje descriptivo")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "job_id": "job_abc123def456",
                "status": "running",
                "message": "Descarga iniciada exitosamente"
            }
        }
    }


class JobStatusResponse(BaseModel):
    """Response con estado de un job."""
    
    job_id: str
    query: str
    sources: List[str]
    status: str
    progress: float
    current_source: Optional[str]
    total_downloaded: int
    total_unique: int
    total_duplicates: int
    started_at: Optional[str]
    completed_at: Optional[str]
    errors: List[str]


class PublicationSummary(BaseModel):
    """Resumen de una publicación."""
    
    id: str
    title: str
    authors: List[str]
    publication_year: Optional[int]
    journal: Optional[str]
    doi: Optional[str]
    source: str


class UnifiedDataResponse(BaseModel):
    """Response con datos unificados."""
    
    total_publications: int
    publications: List[PublicationSummary]
    sources: List[str]
    message: str


@router.post("/download", response_model=DownloadResponse, status_code=202)
async def start_download(
    request: DownloadRequest,
    background_tasks: BackgroundTasks
) -> DownloadResponse:
    """
    🚀 **Inicia descarga automática desde múltiples fuentes científicas.**
    
    Este endpoint implementa el **Requerimiento 1** del proyecto:
    - Automatiza la descarga de datos desde ACM, SAGE, ScienceDirect, CrossRef
    - Unifica formatos bibliográficos (BibTeX, RIS, CSV, JSON)
    - Elimina duplicados automáticamente
    - Genera reporte de publicaciones repetidas eliminadas
    
    **Flujo de trabajo:**
    1. Valida parámetros de entrada
    2. Crea job de descarga con ID único
    3. Inicia descarga asíncrona en background
    4. Retorna ID del job para consultar progreso
    
    **Parámetros:**
    - `query`: Cadena de búsqueda científica
    - `sources`: Lista de fuentes a consultar
    - `max_results_per_source`: Límite de resultados por fuente
    - `start_year`, `end_year`: Filtros temporales opcionales
    - `export_formats`: Formatos de exportación deseados
    
    **Respuesta:**
    - `job_id`: ID único para consultar estado del job
    - `status`: Estado inicial del job ("running")
    - `message`: Mensaje descriptivo
    
    **Ejemplo de uso:**
    ```python
    import requests
    
    response = requests.post('http://localhost:8000/api/v1/data/download', json={
        "query": "generative artificial intelligence",
        "sources": ["crossref"],
        "max_results_per_source": 50,
        "start_year": 2023
    })
    
    job_id = response.json()['job_id']
    print(f"Job iniciado: {job_id}")
    ```
    """
    try:
        logger.info(f"Nueva solicitud de descarga: query='{request.query}', sources={request.sources}")
        
        # Validar años
        if request.start_year and request.end_year:
            if request.start_year > request.end_year:
                raise HTTPException(
                    status_code=400,
                    detail="start_year debe ser menor o igual a end_year"
                )
        
        # Convertir sources a lista de strings
        sources = [source.value for source in request.sources]
        
        # Generar job_id único
        import uuid
        job_id = f"job_{uuid.uuid4().hex[:12]}"
        
        # Registrar job inmediatamente con estado inicial
        from app.services.data_acquisition.unified_downloader import DownloadJob
        job = DownloadJob(job_id, request.query, sources, request.max_results_per_source)
        job.status = "running"
        from datetime import datetime
        job.started_at = datetime.now()
        downloader.active_jobs[job_id] = job
        
        # Iniciar descarga en background con el job_id generado
        async def download_task():
            try:
                await downloader.download(
                    query=request.query,
                    sources=sources,
                    max_results_per_source=request.max_results_per_source,
                    start_year=request.start_year,
                    end_year=request.end_year,
                    export_formats=request.export_formats,
                    job_id=job_id  # Pasar el job_id generado
                )
            except Exception as e:
                logger.error(f"Error en download task: {e}")
                # Actualizar estado del job a failed
                if job_id in downloader.active_jobs:
                    downloader.active_jobs[job_id].status = "failed"
                    downloader.active_jobs[job_id].errors.append(str(e))
        
        # Agregar tarea a background
        background_tasks.add_task(download_task)
        
        return DownloadResponse(
            success=True,
            job_id=job_id,
            status="running",
            message=f"Descarga iniciada para query: '{request.query}'"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error iniciando descarga: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al iniciar descarga: {str(e)}"
        )


@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def get_download_status(
    job_id: str = Path(..., description="ID del job de descarga")
) -> JobStatusResponse:
    """
    📊 **Consulta el estado de una descarga en proceso.**
    
    Permite monitorear el progreso de un job de descarga iniciado previamente.
    
    **Información retornada:**
    - Estado actual del job (running, completed, failed)
    - Progreso en porcentaje
    - Fuente actual siendo procesada
    - Estadísticas de descarga
    - Errores si los hay
    
    **Ejemplo de uso:**
    ```python
    response = requests.get(f'http://localhost:8000/api/v1/data/status/{job_id}')
    status = response.json()
    print(f"Progreso: {status['progress']}%")
    print(f"Descargados: {status['total_downloaded']}")
    ```
    """
    try:
        status = downloader.get_job_status(job_id)
        
        if status is None:
            raise HTTPException(
                status_code=404,
                detail=f"Job {job_id} no encontrado"
            )
        
        return JobStatusResponse(**status)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo estado del job: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al obtener estado: {str(e)}"
        )


@router.get("/jobs", response_model=List[JobStatusResponse])
async def list_all_jobs() -> List[JobStatusResponse]:
    """
    📋 **Lista todos los jobs de descarga activos.**
    
    Retorna información de todos los jobs de descarga que han sido
    ejecutados en la sesión actual.
    
    **Utilidad:**
    - Monitoreo general del sistema
    - Historial de descargas
    - Debugging y auditoría
    """
    try:
        jobs = downloader.list_active_jobs()
        return [JobStatusResponse(**job) for job in jobs]
    
    except Exception as e:
        logger.error(f"Error listando jobs: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al listar jobs: {str(e)}"
        )


@router.get("/unified", response_model=UnifiedDataResponse)
async def get_unified_data(
    limit: int = Query(default=100, ge=1, le=1000, description="Límite de publicaciones a retornar"),
    offset: int = Query(default=0, ge=0, description="Offset para paginación"),
    source: Optional[str] = Query(None, description="Filtrar por fuente específica")
) -> UnifiedDataResponse:
    """
    📚 **Obtiene datos unificados sin duplicados.**
    
    Retorna las publicaciones únicas después del proceso de unificación
    y deduplicación.
    
    **Características:**
    - Paginación con limit y offset
    - Filtrado opcional por fuente
    - Formato estandarizado
    
    **Parámetros:**
    - `limit`: Número de publicaciones a retornar (1-1000)
    - `offset`: Punto de inicio para paginación
    - `source`: Filtro opcional por fuente de datos
    
    **Ejemplo de uso:**
    ```python
    # Obtener primeras 50 publicaciones
    response = requests.get('http://localhost:8000/api/v1/data/unified?limit=50&offset=0')
    
    # Filtrar solo publicaciones de CrossRef
    response = requests.get('http://localhost:8000/api/v1/data/unified?source=crossref')
    ```
    """
    try:
        # TODO: Implementar lectura desde archivo o base de datos
        # Por ahora retornamos ejemplo
        
        return UnifiedDataResponse(
            total_publications=0,
            publications=[],
            sources=[],
            message="Funcionalidad en desarrollo: leer desde archivos unificados"
        )
    
    except Exception as e:
        logger.error(f"Error obteniendo datos unificados: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )


@router.get("/duplicates/{job_id}")
async def get_duplicates_report(
    job_id: str = Path(..., description="ID del job")
):
    """
    🔍 **Obtiene el reporte de duplicados eliminados.**
    
    Retorna información detallada sobre todas las publicaciones duplicadas
    que fueron identificadas y eliminadas durante el proceso de unificación.
    
    **Información incluida:**
    - Total de duplicados encontrados
    - Duplicados por tipo (DOI, título, hash)
    - Lista detallada de cada duplicado
    - Publicación original vs duplicada
    - Razón de la deduplicación
    - Score de similitud
    
    **Ejemplo de respuesta:**
    ```json
    {
      "summary": {
        "total_duplicates_found": 15,
        "duplicates_by_doi": 8,
        "duplicates_by_title_similarity": 7,
        "duplicate_rate": "13.04%"
      },
      "duplicates": [
        {
          "original_title": "Generative AI in Education",
          "duplicate_title": "Generative AI in Education",
          "reason": "DOI idéntico",
          "similarity_score": 1.0
        }
      ]
    }
    ```
    """
    try:
        # Buscar archivo de reporte de duplicados
        output_dir = FilePath("data/downloads")
        
        # Buscar archivos que coincidan con el job_id
        duplicate_files = list(output_dir.glob(f"{job_id}_*_duplicates.json"))
        
        if not duplicate_files:
            raise HTTPException(
                status_code=404,
                detail=f"Reporte de duplicados no encontrado para job {job_id}"
            )
        
        # Retornar el archivo más reciente
        latest_file = max(duplicate_files, key=lambda p: p.stat().st_mtime)
        
        return FileResponse(
            path=str(latest_file),
            media_type="application/json",
            filename=latest_file.name
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo reporte de duplicados: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )


@router.get("/download/{job_id}/{format}")
async def download_results(
    job_id: str = Path(..., description="ID del job"),
    format: ExportFormat = Path(..., description="Formato de exportación")
):
    """
    💾 **Descarga los resultados en el formato especificado.**
    
    Permite descargar las publicaciones unificadas en diferentes formatos:
    - **JSON**: Formato estructurado con todos los metadatos
    - **BibTeX**: Para gestores bibliográficos (Zotero, Mendeley)
    - **RIS**: Formato estándar para referencias
    - **CSV**: Para análisis en Excel/Python
    
    **Parámetros:**
    - `job_id`: ID del job de descarga
    - `format`: Formato deseado (json, bibtex, ris, csv)
    
    **Ejemplo de uso:**
    ```python
    # Descargar en formato BibTeX
    response = requests.get(f'http://localhost:8000/api/v1/data/download/{job_id}/bibtex')
    
    with open('publications.bib', 'wb') as f:
        f.write(response.content)
    ```
    """
    try:
        output_dir = FilePath("data/downloads")
        
        # Mapear formato a extensión
        extension_map = {
            ExportFormat.JSON: 'json',
            ExportFormat.BIBTEX: 'bib',
            ExportFormat.RIS: 'ris',
            ExportFormat.CSV: 'csv'
        }
        
        extension = extension_map[format]
        
        # Buscar archivo
        result_files = list(output_dir.glob(f"{job_id}_*_unified.{extension}"))
        
        if not result_files:
            raise HTTPException(
                status_code=404,
                detail=f"Archivo no encontrado para job {job_id} en formato {format.value}"
            )
        
        # Retornar archivo más reciente
        latest_file = max(result_files, key=lambda p: p.stat().st_mtime)
        
        # Determinar media type
        media_types = {
            'json': 'application/json',
            'bib': 'application/x-bibtex',
            'ris': 'application/x-research-info-systems',
            'csv': 'text/csv'
        }
        
        return FileResponse(
            path=str(latest_file),
            media_type=media_types.get(extension, 'application/octet-stream'),
            filename=f"publications_{job_id}.{extension}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error descargando resultados: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )


@router.get("/sources")
async def list_available_sources():
    """
    📌 **Lista las fuentes de datos disponibles.**
    
    Retorna información sobre todas las fuentes de datos científicas
    que están configuradas y disponibles para consulta.
    
    **Información por fuente:**
    - Nombre y descripción
    - Estado (disponible/no disponible)
    - Cobertura temática
    - Limitaciones de API
    """
    return {
        "sources": [
            {
                "id": "crossref",
                "name": "CrossRef",
                "description": "API pública con millones de metadatos bibliográficos",
                "available": True,
                "requires_api_key": False,
                "rate_limit": "50 req/s (público)",
                "coverage": "Multidisciplinario"
            },
            {
                "id": "acm",
                "name": "ACM Digital Library",
                "description": "Publicaciones de ACM (Association for Computing Machinery)",
                "available": False,
                "requires_api_key": True,
                "rate_limit": "Depende de suscripción",
                "coverage": "Ciencias de la Computación"
            },
            {
                "id": "sage",
                "name": "SAGE Publications",
                "description": "Editorial académica con amplia cobertura",
                "available": False,
                "requires_api_key": True,
                "rate_limit": "Depende de suscripción",
                "coverage": "Ciencias Sociales, Humanidades"
            },
            {
                "id": "sciencedirect",
                "name": "ScienceDirect",
                "description": "Base de datos de Elsevier",
                "available": False,
                "requires_api_key": True,
                "rate_limit": "Depende de suscripción",
                "coverage": "Multidisciplinario (STM)"
            }
        ],
        "total_sources": 4,
        "available_sources": 1
    }


@router.delete("/jobs/{job_id}")
async def cancel_job(
    job_id: str = Path(..., description="ID del job a cancelar")
):
    """
    🛑 **Cancela un job de descarga en ejecución.**
    
    Intenta detener un job de descarga que esté actualmente en ejecución.
    
    **Nota:** Los jobs ya completados no pueden ser cancelados.
    """
    try:
        # TODO: Implementar lógica de cancelación
        return {
            "success": False,
            "message": "Funcionalidad de cancelación en desarrollo"
        }
    
    except Exception as e:
        logger.error(f"Error cancelando job: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )
