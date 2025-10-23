"""
Scraper para ScienceDirect (Elsevier)
======================================

Implementa el scraper para ScienceDirect API, la plataforma de Elsevier
que proporciona acceso a artículos científicos de alta calidad.

ScienceDirect cuenta con una API robusta que requiere API key institucional.

API Documentation: https://dev.elsevier.com/

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Course: Análisis de Algoritmos (2025-2), Universidad del Quindío
"""

import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import json
import re

from .base_scraper import BaseScraper, ScraperStatus
from app.models.publication import Publication, Author

logger = logging.getLogger(__name__)


class ScienceDirectScraper(BaseScraper):
    """
    Scraper para ScienceDirect API (Elsevier).
    
    ScienceDirect es la plataforma de publicaciones científicas de Elsevier,
    con cobertura en ciencia, tecnología y medicina.
    
    API Features:
    - Requiere API key institucional
    - Búsqueda avanzada con filtros
    - Metadatos completos
    - Acceso a abstracts
    
    Limitaciones:
    - Rate limit: depende del nivel de suscripción
    - Requiere autenticación
    - Contenido completo solo con suscripción
    
    Estrategia:
    1. Autenticación con API key
    2. Búsqueda usando Scopus Search API
    3. Extracción de metadatos vía Article Retrieval API
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        rate_limit: float = 0.3,  # ~3 peticiones cada 10 segundos (conservador)
        timeout: int = 30
    ):
        """
        Inicializa el scraper de ScienceDirect.
        
        Args:
            api_key: API key de Elsevier (REQUERIDO para producción)
            rate_limit: Peticiones por segundo
            timeout: Timeout de peticiones en segundos
        """
        super().__init__(
            source_name="sciencedirect",
            base_url="https://api.elsevier.com",
            api_key=api_key,
            rate_limit=rate_limit,
            timeout=timeout
        )
        
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Advertencia si no hay API key
        if not api_key:
            logger.warning(
                "ScienceDirectScraper inicializado sin API key. "
                "Las búsquedas fallarán en producción. "
                "Obten una API key en: https://dev.elsevier.com/"
            )
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Obtiene o crea una sesión aiohttp con headers apropiados."""
        if self.session is None or self.session.closed:
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'BibliometricAnalysis/1.0 (Universidad del Quindio)',
            }
            
            # Agregar API key si está disponible
            if self.api_key:
                headers['X-ELS-APIKey'] = self.api_key
            
            timeout_config = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(
                headers=headers,
                timeout=timeout_config
            )
        
        return self.session
    
    async def close(self):
        """Cierra la sesión HTTP."""
        if self.session and not self.session.closed:
            await self.session.close()
            logger.info("Sesión de ScienceDirect cerrada")
    
    async def search(
        self,
        query: str,
        max_results: int = 100,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        publication_type: Optional[str] = None
    ) -> List[Publication]:
        """
        Busca publicaciones en ScienceDirect.
        
        Args:
            query: Cadena de búsqueda
            max_results: Número máximo de resultados
            start_year: Año de inicio (filtro)
            end_year: Año final (filtro)
            publication_type: Tipo de publicación
        
        Returns:
            Lista de publicaciones encontradas
        """
        self.status = ScraperStatus.SEARCHING
        logger.info(f"Buscando en ScienceDirect: '{query}' (max: {max_results})")
        
        # Validar API key
        if not self.api_key:
            logger.error(
                "API key de ScienceDirect no configurada. "
                "Retornando datos de ejemplo para desarrollo."
            )
            return self._get_mock_data(query, max_results)
        
        session = await self._get_session()
        publications: List[Publication] = []
        
        try:
            # Usar Scopus Search API (más completo que ScienceDirect Search)
            search_url = f"{self.base_url}/content/search/scopus"
            
            # Construir query con filtros
            search_query = query
            
            # Agregar filtros de año
            if start_year and end_year:
                search_query += f" AND PUBYEAR > {start_year - 1} AND PUBYEAR < {end_year + 1}"
            elif start_year:
                search_query += f" AND PUBYEAR > {start_year - 1}"
            elif end_year:
                search_query += f" AND PUBYEAR < {end_year + 1}"
            
            # Parámetros de búsqueda
            count_per_request = min(25, max_results)  # Scopus max: 25
            start = 0
            
            while len(publications) < max_results:
                # Respetar rate limit
                await self._respect_rate_limit()
                
                params = {
                    'query': search_query,
                    'count': count_per_request,
                    'start': start,
                    'view': 'COMPLETE'  # Obtener metadatos completos
                }
                
                async with session.get(search_url, params=params) as response:
                    if response.status == 401:
                        logger.error("API key inválida o expirada")
                        break
                    elif response.status == 429:
                        logger.warning("Rate limit excedido. Esperando...")
                        await asyncio.sleep(5)
                        continue
                    elif response.status != 200:
                        logger.error(f"Error en ScienceDirect: HTTP {response.status}")
                        break
                    
                    data = await response.json()
                    
                    # Extraer resultados
                    search_results = data.get('search-results', {})
                    entries = search_results.get('entry', [])
                    
                    if not entries:
                        logger.info("No se encontraron más resultados en ScienceDirect")
                        break
                    
                    # Procesar cada resultado
                    for entry in entries:
                        if len(publications) >= max_results:
                            break
                        
                        try:
                            pub = await self._parse_scopus_entry(entry, session)
                            if pub:
                                publications.append(pub)
                                logger.debug(
                                    f"ScienceDirect: {len(publications)}/{max_results} - "
                                    f"{pub.title[:50]}..."
                                )
                        except Exception as e:
                            logger.warning(f"Error procesando resultado de ScienceDirect: {e}")
                            continue
                    
                    # Actualizar start para siguiente página
                    start += count_per_request
                    
                    # Verificar si hay más resultados
                    total_results = int(search_results.get('opensearch:totalResults', 0))
                    if start >= total_results:
                        break
            
            self.status = ScraperStatus.COMPLETED
            logger.info(
                f"ScienceDirect: Búsqueda completada. "
                f"{len(publications)} publicaciones encontradas"
            )
            
            return publications
        
        except Exception as e:
            self.status = ScraperStatus.ERROR
            logger.error(f"Error en búsqueda de ScienceDirect: {e}")
            raise
    
    async def _parse_scopus_entry(
        self,
        entry: Dict[str, Any],
        session: aiohttp.ClientSession
    ) -> Optional[Publication]:
        """
        Parsea un resultado de Scopus/ScienceDirect.
        
        Args:
            entry: Diccionario con datos del resultado
            session: Sesión aiohttp activa
        
        Returns:
            Publicación parseada o None si falla
        """
        try:
            # Extraer título
            title = entry.get('dc:title', '')
            if not title:
                return None
            
            # Extraer DOI
            doi = entry.get('prism:doi')
            
            # Extraer URL
            links = entry.get('link', [])
            url = None
            for link in links:
                if isinstance(link, dict) and link.get('@ref') == 'scopus':
                    url = link.get('@href')
                    break
            
            # Si no hay URL de Scopus, construir desde DOI
            if not url and doi:
                url = f"https://www.sciencedirect.com/science/article/pii/{doi}"
            
            # Extraer autores
            authors = []
            author_data = entry.get('author', [])
            
            if isinstance(author_data, list):
                for author in author_data:
                    author_name = author.get('authname', '')
                    affiliation = author.get('affiliation', {})
                    
                    if isinstance(affiliation, dict):
                        affiliation_name = affiliation.get('affilname', '')
                    else:
                        affiliation_name = None
                    
                    if author_name:
                        authors.append(Author(
                            name=author_name,
                            affiliation=affiliation_name
                        ))
            
            # Extraer año de publicación
            cover_date = entry.get('prism:coverDate', '')
            publication_date = None
            
            if cover_date:
                try:
                    # Formato: YYYY-MM-DD
                    publication_date = datetime.strptime(cover_date, '%Y-%m-%d').date()
                except:
                    # Intentar solo año
                    year_match = re.search(r'\b(19|20)\d{2}\b', cover_date)
                    if year_match:
                        publication_date = datetime(int(year_match.group(0)), 1, 1).date()
            
            # Extraer journal
            journal = entry.get('prism:publicationName', 'ScienceDirect Publication')
            
            # Extraer abstract (puede requerir petición adicional)
            abstract = entry.get('dc:description', '')
            
            # Si no hay abstract, intentar obtenerlo del artículo completo
            if not abstract and doi:
                abstract = await self._fetch_abstract(doi, session)
            
            # Extraer keywords
            keywords_str = entry.get('authkeywords', '')
            keywords = []
            if keywords_str:
                keywords = [kw.strip() for kw in keywords_str.split('|')]
            
            # Extraer número de citas
            citation_count = entry.get('citedby-count')
            if citation_count:
                try:
                    citation_count = int(citation_count)
                except:
                    citation_count = 0
            
            # Crear publicación
            publication = Publication(
                title=title,
                abstract=abstract or "Abstract not available",
                authors=authors,
                keywords=keywords,
                doi=doi,
                url=url,
                publication_date=publication_date,
                journal=journal,
                source="sciencedirect",
                citation_count=citation_count
            )
            
            return publication
        
        except Exception as e:
            logger.warning(f"Error parseando resultado de ScienceDirect: {e}")
            return None
    
    async def _fetch_abstract(
        self,
        doi: str,
        session: aiohttp.ClientSession
    ) -> str:
        """
        Obtiene el abstract de un artículo usando la API de Article Retrieval.
        
        Args:
            doi: DOI del artículo
            session: Sesión aiohttp activa
        
        Returns:
            Abstract del artículo o cadena vacía
        """
        try:
            # Respetar rate limit
            await self._respect_rate_limit()
            
            # Construir URL de Article Retrieval API
            article_url = f"{self.base_url}/content/article/doi/{doi}"
            
            params = {
                'view': 'FULL'
            }
            
            async with session.get(article_url, params=params) as response:
                if response.status != 200:
                    logger.debug(f"No se pudo obtener abstract para DOI {doi}")
                    return ""
                
                data = await response.json()
                
                # Extraer abstract del response
                core_data = data.get('full-text-retrieval-response', {}).get('coredata', {})
                abstract = core_data.get('dc:description', '')
                
                return abstract
        
        except Exception as e:
            logger.debug(f"Error obteniendo abstract para DOI {doi}: {e}")
            return ""
    
    async def download_metadata(
        self,
        publication_id: str
    ) -> Dict[str, Any]:
        """
        Descarga metadatos completos de una publicación por DOI.
        
        Args:
            publication_id: DOI de la publicación
        
        Returns:
            Diccionario con metadatos completos
        """
        self.status = ScraperStatus.DOWNLOADING
        logger.info(f"Descargando metadatos de ScienceDirect: {publication_id}")
        
        if not self.api_key:
            raise ValueError("API key requerida para descargar metadatos de ScienceDirect")
        
        try:
            session = await self._get_session()
            await self._respect_rate_limit()
            
            # Usar Article Retrieval API
            url = f"{self.base_url}/content/article/doi/{publication_id}"
            
            params = {
                'view': 'FULL'
            }
            
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    raise ValueError(
                        f"No se pudo descargar publicación: HTTP {response.status}"
                    )
                
                data = await response.json()
                
                # Extraer metadatos
                metadata = data.get('full-text-retrieval-response', {})
                
                self.status = ScraperStatus.COMPLETED
                return metadata
        
        except Exception as e:
            self.status = ScraperStatus.ERROR
            logger.error(f"Error descargando de ScienceDirect: {e}")
            raise
    
    def export_to_format(
        self,
        publications: List[Publication],
        format: str = 'json'
    ) -> str:
        """
        Exporta publicaciones al formato especificado.
        
        Args:
            publications: Lista de publicaciones
            format: Formato de exportación ('json', 'bibtex', 'ris', 'csv')
        
        Returns:
            Datos en el formato especificado
        """
        if format.lower() == 'json':
            return json.dumps(
                [pub.model_dump() for pub in publications],
                indent=2,
                default=str,
                ensure_ascii=False
            )
        elif format.lower() == 'bibtex':
            from .parsers.bibtex_parser import BibTeXParser
            parser = BibTeXParser()
            return parser.export_publications(publications)
        elif format.lower() == 'ris':
            from .parsers.ris_parser import RISParser
            parser = RISParser()
            return parser.export_publications(publications)
        elif format.lower() == 'csv':
            from .parsers.csv_parser import CSVParser
            parser = CSVParser()
            return parser.export_publications(publications)
        else:
            raise ValueError(f"Formato no soportado: {format}")
    
    def _get_mock_data(
        self,
        query: str,
        max_results: int
    ) -> List[Publication]:
        """
        Genera datos de ejemplo para desarrollo sin API key.
        
        Args:
            query: Query de búsqueda
            max_results: Número de resultados
        
        Returns:
            Lista de publicaciones de ejemplo
        """
        logger.info(
            f"Generando {min(5, max_results)} publicaciones de ejemplo "
            f"(ScienceDirect requiere API key para datos reales)"
        )
        
        mock_publications = []
        
        for i in range(min(5, max_results)):
            pub = Publication(
                title=f"[MOCK] Generative AI in Education - Study {i+1}",
                abstract=f"This is a mock publication for query '{query}'. "
                         f"In production, this would be real data from ScienceDirect API. "
                         f"Configure SCIENCEDIRECT_API_KEY environment variable.",
                authors=[
                    Author(name=f"Author {i+1}A", affiliation="Mock University"),
                    Author(name=f"Author {i+1}B", affiliation="Example Institute")
                ],
                keywords=["generative ai", "education", "machine learning"],
                doi=f"10.1016/j.example.2024.{i+1:03d}",
                url=f"https://www.sciencedirect.com/science/article/mock/{i+1}",
                publication_date=datetime(2024, 1, 1).date(),
                journal="Mock Journal of AI Research",
                source="sciencedirect",
                citation_count=10 + i
            )
            mock_publications.append(pub)
        
        return mock_publications
    
    def parse_publication(self, raw_data: dict) -> Optional[Publication]:
        """
        Parsea datos crudos del scraper ScienceDirect.
        
        Args:
            raw_data: Diccionario con datos crudos de ScienceDirect/Scopus API
        
        Returns:
            Objeto Publication parseado o None si falla
        """
        try:
            return self._parse_scopus_entry(raw_data)
        except Exception as e:
            logger.error(f"Error parseando publicación ScienceDirect: {e}")
            return None
    
    async def download_file(self, publication: Publication, file_format: str = "pdf") -> Optional[str]:
        """
        Descarga el archivo completo de una publicación ScienceDirect.
        
        Nota: ScienceDirect requiere API key con permisos de descarga.
        Este método retorna la URL de descarga pero requiere configuración adicional.
        
        Args:
            publication: Publicación de la cual descargar el archivo
            file_format: Formato del archivo (solo pdf soportado)
        
        Returns:
            URL de descarga o None si no está disponible
        """
        if not self.api_key:
            logger.warning("Download requiere API key de ScienceDirect")
            return None
        
        if not publication.doi:
            logger.warning("No se puede descargar archivo sin DOI")
            return None
        
        # Construir URL para descarga usando Article Retrieval API
        # Nota: Requiere permisos específicos en la API key
        pii = publication.doi.split('/')[-1] if '/' in publication.doi else publication.doi
        download_url = f"{self.base_url}/article/pii/{pii}"
        
        logger.info(f"URL de descarga ScienceDirect: {download_url}")
        logger.warning("Descarga directa requiere API key con permisos de descarga")
        
        return download_url

