"""
Descargador Unificado
=====================

Orquesta la descarga de publicaciones desde múltiples fuentes científicas,
unifica los formatos y elimina duplicados automáticamente.

Este módulo es el punto de entrada principal para el Requerimiento 1.

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Course: Análisis de Algoritmos (2025-2), Universidad del Quindío
"""

import asyncio
import logging
from typing import List, Dict, Optional, Set
from datetime import datetime
import json
from pathlib import Path

from .base_scraper import BaseScraper, ExportFormat
from .crossref_scraper import CrossRefScraper
from .deduplicator import Deduplicator, DuplicateReport
from app.models.publication import Publication

logger = logging.getLogger(__name__)


class DownloadJob:
    """
    Representa un trabajo de descarga.
    
    Mantiene el estado y progreso de una descarga en curso.
    """
    
    def __init__(
        self,
        job_id: str,
        query: str,
        sources: List[str],
        max_results_per_source: int
    ):
        self.job_id = job_id
        self.query = query
        self.sources = sources
        self.max_results_per_source = max_results_per_source
        
        self.status = "pending"
        self.progress = 0.0
        self.current_source: Optional[str] = None
        self.message = "Iniciando descarga..."
        
        self.publications_by_source: Dict[str, List[Publication]] = {}
        self.unified_publications: List[Publication] = []
        self.duplicate_report: Optional[DuplicateReport] = None
        
        self.total_downloaded = 0
        self.total_unique = 0
        self.total_duplicates = 0
        
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.errors: List[str] = []
    
    def to_dict(self) -> Dict:
        """Convierte el job a diccionario para serialización."""
        return {
            'job_id': self.job_id,
            'query': self.query,
            'sources': self.sources,
            'max_results_per_source': self.max_results_per_source,
            'status': self.status,
            'progress': self.progress,
            'current_source': self.current_source,
            'message': self.message,
            'total_downloaded': self.total_downloaded,
            'total_unique': self.total_unique,
            'total_duplicates': self.total_duplicates,
            'total_publications': self.total_unique,  # Alias para total_unique
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'errors': self.errors
        }


class UnifiedDownloader:
    """
    Descargador unificado que orquesta la descarga desde múltiples fuentes.
    
    Flujo de trabajo:
    1. Inicializar scrapers para cada fuente solicitada
    2. Realizar búsquedas en paralelo en todas las fuentes
    3. Recopilar resultados por fuente
    4. Unificar formatos a modelo Publication estándar
    5. Ejecutar deduplicación inteligente
    6. Generar reporte de duplicados
    7. Guardar resultados unificados
    
    Características:
    - Descarga asíncrona y paralela
    - Manejo robusto de errores
    - Progreso en tiempo real
    - Exportación a múltiples formatos
    - Sistema de caché (opcional)
    """
    
    def __init__(
        self,
        similarity_threshold: float = 0.95,
        rate_limit: float = 1.0,
        output_dir: str = "data/downloads"
    ):
        """
        Inicializa el descargador unificado.
        
        Args:
            similarity_threshold: Umbral para deduplicación
            rate_limit: Límite de peticiones por segundo
            output_dir: Directorio de salida para archivos
        """
        self.similarity_threshold = similarity_threshold
        self.rate_limit = rate_limit
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Scrapers disponibles
        self.available_scrapers = {
            'crossref': CrossRefScraper,
            # 'acm': ACMScraper,  # A implementar
            # 'sage': SAGEScraper,  # A implementar
            # 'sciencedirect': ScienceDirectScraper  # A implementar
        }
        
        # Jobs en ejecución
        self.active_jobs: Dict[str, DownloadJob] = {}
        
        logger.info(f"UnifiedDownloader inicializado con threshold={similarity_threshold}")
    
    def _generate_job_id(self) -> str:
        """Genera un ID único para un job."""
        import uuid
        return f"job_{uuid.uuid4().hex[:12]}"
    
    async def download(
        self,
        query: str,
        sources: List[str],
        max_results_per_source: int = 100,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        export_formats: Optional[List[ExportFormat]] = None,
        job_id: Optional[str] = None
    ) -> DownloadJob:
        """
        Descarga publicaciones desde múltiples fuentes de manera unificada.
        
        Args:
            query: Cadena de búsqueda
            sources: Lista de fuentes a consultar ['crossref', 'acm', 'sage']
            max_results_per_source: Máximo de resultados por fuente
            start_year: Año de inicio para filtrar
            end_year: Año final para filtrar
            export_formats: Formatos de exportación adicionales
            job_id: ID del job (opcional, se genera automáticamente si no se proporciona)
        
        Returns:
            DownloadJob con resultados y estadísticas
        """
        # Crear job
        if job_id is None:
            job_id = self._generate_job_id()
        
        # Si el job ya existe (fue registrado externamente), actualizarlo
        # Si no existe, crear uno nuevo
        if job_id in self.active_jobs:
            job = self.active_jobs[job_id]
            logger.info(f"Reanudando job existente {job_id}")
        else:
            job = DownloadJob(job_id, query, sources, max_results_per_source)
            job.started_at = datetime.now()
            job.status = "running"
            self.active_jobs[job_id] = job
            logger.info(f"Creando nuevo job {job_id}")
        
        logger.info(f"Iniciando job {job_id}: query='{query}', sources={sources}")
        
        try:
            # Validar fuentes
            valid_sources = [s for s in sources if s in self.available_scrapers]
            invalid_sources = [s for s in sources if s not in self.available_scrapers]
            
            if invalid_sources:
                warning = f"Fuentes no disponibles ignoradas: {invalid_sources}"
                logger.warning(warning)
                job.errors.append(warning)
            
            if not valid_sources:
                raise ValueError("No hay fuentes válidas disponibles")
            
            # Inicializar scrapers
            scrapers: Dict[str, BaseScraper] = {}
            for source in valid_sources:
                scraper_class = self.available_scrapers[source]
                scrapers[source] = scraper_class(rate_limit=self.rate_limit)
                logger.info(f"Scraper inicializado: {source}")
            
            # Calcular progreso por etapa
            total_steps = len(valid_sources) + 2  # Descargas + Unificación + Exportación
            progress_per_step = 100.0 / total_steps
            
            # Descargar de cada fuente (con actualización de progreso)
            for i, (source, scraper) in enumerate(scrapers.items(), 1):
                job.current_source = source
                job.progress = (i - 1) * progress_per_step
                job.message = f"Descargando de {source}..."
                logger.info(f"Progreso: {job.progress:.1f}% - Descargando de {source}")
                
                await self._download_from_source(
                    job, source, scraper, query,
                    max_results_per_source, start_year, end_year
                )
                
                # Actualizar progreso después de cada fuente
                job.progress = i * progress_per_step
                job.message = f"Completada descarga de {source}: {len(job.publications_by_source.get(source, []))} publicaciones"
                logger.info(f"Progreso: {job.progress:.1f}% - {source} completado")
            
                # Actualizar progreso después de cada fuente
                job.progress = i * progress_per_step
                logger.info(f"Progreso: {job.progress:.1f}% - {source} completado")
            
            # Cerrar sesiones de scrapers
            for scraper in scrapers.values():
                if hasattr(scraper, 'close'):
                    await scraper.close()
            
            # Unificar y deduplicar
            job.progress = len(valid_sources) * progress_per_step
            job.current_source = "Unificando y deduplicando"
            job.message = "Unificando resultados y eliminando duplicados..."
            logger.info(f"Progreso: {job.progress:.1f}% - Iniciando unificación")
            
            await self._unify_and_deduplicate(job)
            
            # Exportar resultados
            job.progress = (len(valid_sources) + 1) * progress_per_step
            job.current_source = "Exportando resultados"
            job.message = "Exportando resultados a múltiples formatos..."
            logger.info(f"Progreso: {job.progress:.1f}% - Exportando resultados")
            
            if export_formats:
                await self._export_results(job, export_formats)
            else:
                # Por defecto exportar JSON y BibTeX
                await self._export_results(
                    job,
                    [ExportFormat.JSON, ExportFormat.BIBTEX]
                )
            
            job.status = "completed"
            job.progress = 100.0
            job.message = f"Descarga completada: {job.total_unique} publicaciones únicas de {job.total_downloaded} descargadas"
            job.completed_at = datetime.now()
            
            duration = (job.completed_at - job.started_at).total_seconds()
            
            logger.info(f"""
            Job {job_id} completado exitosamente:
            - Duración: {duration:.2f} segundos
            - Total descargados: {job.total_downloaded}
            - Únicos: {job.total_unique}
            - Duplicados: {job.total_duplicates}
            - Tasa de duplicación: {(job.total_duplicates / job.total_downloaded * 100):.2f}%
            """)
        
        except Exception as e:
            error_msg = f"Error en job {job_id}: {e}"
            logger.error(error_msg)
            job.errors.append(error_msg)
            job.status = "failed"
            job.completed_at = datetime.now()
            raise
        
        return job
    
    async def _download_from_source(
        self,
        job: DownloadJob,
        source: str,
        scraper: BaseScraper,
        query: str,
        max_results: int,
        start_year: Optional[int],
        end_year: Optional[int]
    ):
        """Descarga publicaciones de una fuente específica."""
        try:
            job.current_source = source
            logger.info(f"Descargando de {source}...")
            
            publications = await scraper.search(
                query=query,
                max_results=max_results,
                start_year=start_year,
                end_year=end_year
            )
            
            job.publications_by_source[source] = publications
            job.total_downloaded += len(publications)
            
            logger.info(f"Descarga de {source} completada: {len(publications)} publicaciones")
        
        except Exception as e:
            error_msg = f"Error descargando de {source}: {e}"
            logger.error(error_msg)
            job.errors.append(error_msg)
            job.publications_by_source[source] = []
    
    async def _unify_and_deduplicate(self, job: DownloadJob):
        """Unifica y deduplica publicaciones."""
        logger.info("Iniciando unificación y deduplicación...")
        
        # Recopilar todas las publicaciones
        all_publications = []
        for source, pubs in job.publications_by_source.items():
            all_publications.extend(pubs)
            logger.info(f"Fuente {source}: {len(pubs)} publicaciones")
        
        if not all_publications:
            logger.warning("No hay publicaciones para deduplicar")
            return
        
        # Ejecutar deduplicación
        deduplicator = Deduplicator(
            similarity_threshold=self.similarity_threshold,
            use_doi_comparison=True,
            use_title_hash=True,
            use_fuzzy_matching=True,
            use_author_comparison=False
        )
        
        unique_publications, duplicate_report = deduplicator.deduplicate(all_publications)
        
        job.unified_publications = unique_publications
        job.duplicate_report = duplicate_report
        job.total_unique = len(unique_publications)
        job.total_duplicates = duplicate_report.total_duplicates
        
        logger.info(f"""
        Unificación completada:
        - Total descargados: {len(all_publications)}
        - Únicos: {len(unique_publications)}
        - Duplicados: {duplicate_report.total_duplicates}
        """)
    
    async def _export_results(
        self,
        job: DownloadJob,
        formats: List[ExportFormat]
    ):
        """Exporta resultados a archivos."""
        logger.info(f"Exportando resultados en formatos: {formats}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{job.job_id}_{timestamp}"
        
        for fmt in formats:
            try:
                # Crear scraper temporal para usar método de exportación
                scraper = CrossRefScraper()
                content = scraper.export_to_format(
                    job.unified_publications,
                    fmt
                )
                
                # Determinar extensión
                extension_map = {
                    ExportFormat.JSON: 'json',
                    ExportFormat.BIBTEX: 'bib',
                    ExportFormat.RIS: 'ris',
                    ExportFormat.CSV: 'csv'
                }
                
                extension = extension_map.get(fmt, 'txt')
                filename = self.output_dir / f"{base_filename}_unified.{extension}"
                
                # Guardar archivo
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                logger.info(f"Exportado a {fmt.value}: {filename}")
            
            except Exception as e:
                logger.error(f"Error exportando a {fmt.value}: {e}")
                job.errors.append(f"Error exportando a {fmt.value}: {e}")
        
        # Guardar reporte de duplicados
        if job.duplicate_report:
            duplicates_file = self.output_dir / f"{base_filename}_duplicates.json"
            job.duplicate_report.save_to_file(str(duplicates_file))
            logger.info(f"Reporte de duplicados guardado: {duplicates_file}")
        
        # Guardar resumen del job
        job_summary_file = self.output_dir / f"{base_filename}_summary.json"
        with open(job_summary_file, 'w', encoding='utf-8') as f:
            json.dump(job.to_dict(), f, indent=2, ensure_ascii=False)
        
        logger.info(f"Resumen del job guardado: {job_summary_file}")
    
    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """
        Obtiene el estado de un job.
        
        Args:
            job_id: ID del job
        
        Returns:
            Diccionario con estado o None si no existe
        """
        job = self.active_jobs.get(job_id)
        return job.to_dict() if job else None
    
    def list_active_jobs(self) -> List[Dict]:
        """Lista todos los jobs activos."""
        return [job.to_dict() for job in self.active_jobs.values()]


# Ejemplo de uso
async def main():
    """Función de ejemplo para probar el descargador unificado."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    downloader = UnifiedDownloader(
        similarity_threshold=0.95,
        rate_limit=1.0,
        output_dir="data/downloads"
    )
    
    # Descargar publicaciones
    job = await downloader.download(
        query="generative artificial intelligence",
        sources=['crossref'],
        max_results_per_source=50,
        start_year=2023
    )
    
    print(f"\n{'='*80}")
    print(f"DESCARGA UNIFICADA COMPLETADA")
    print(f"{'='*80}")
    print(f"Job ID: {job.job_id}")
    print(f"Query: '{job.query}'")
    print(f"Fuentes: {', '.join(job.sources)}")
    print(f"{'='*80}")
    print(f"Total descargados: {job.total_downloaded}")
    print(f"Publicaciones únicas: {job.total_unique}")
    print(f"Duplicados eliminados: {job.total_duplicates}")
    print(f"Tasa de duplicación: {(job.total_duplicates / job.total_downloaded * 100 if job.total_downloaded > 0 else 0):.2f}%")
    print(f"{'='*80}")
    print(f"Duración: {(job.completed_at - job.started_at).total_seconds():.2f} segundos")
    print(f"Archivos guardados en: {downloader.output_dir}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    asyncio.run(main())
