"""
Scraper para SAGE Journals
===========================

Implementa el scraper para SAGE Publications, una editorial académica
líder en ciencias sociales, humanidades y STM.

SAGE proporciona acceso a miles de revistas académicas revisadas por pares.

Website: https://journals.sagepub.com/

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Course: Análisis de Algoritmos (2025-2), Universidad del Quindío
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import json
import re

from .base_scraper import BaseScraper, ScraperStatus
from app.models.publication import Publication, Author

logger = logging.getLogger(__name__)


class SAGEScraper(BaseScraper):
    """
    Scraper para SAGE Journals.
    
    SAGE Publications es una editorial académica independiente que publica
    revistas de alta calidad en ciencias sociales, humanidades, medicina y STM.
    
    Notas:
    - Requiere acceso institucional para contenido completo
    - Web scraping de resultados de búsqueda
    - Rate limiting conservador
    
    Estrategia:
    1. Búsqueda a través de SAGE Journals Search
    2. Parsing de resultados HTML
    3. Extracción de metadatos de páginas individuales
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        rate_limit: float = 0.5,  # 1 petición cada 2 segundos
        timeout: int = 30
    ):
        """
        Inicializa el scraper de SAGE.
        
        Args:
            api_key: No utilizado actualmente
            rate_limit: Peticiones por segundo
            timeout: Timeout de peticiones en segundos
        """
        super().__init__(
            source_name="sage",
            base_url="https://journals.sagepub.com",
            api_key=api_key,
            rate_limit=rate_limit,
            timeout=timeout
        )
        
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Obtiene o crea una sesión aiohttp con headers apropiados."""
        if self.session is None or self.session.closed:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
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
            logger.info("Sesión de SAGE cerrada")
    
    async def search(
        self,
        query: str,
        max_results: int = 100,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        publication_type: Optional[str] = None
    ) -> List[Publication]:
        """
        Busca publicaciones en SAGE Journals.
        
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
        logger.info(f"Buscando en SAGE Journals: '{query}' (max: {max_results})")
        
        session = await self._get_session()
        publications: List[Publication] = []
        
        try:
            # Construir URL de búsqueda
            search_url = f"{self.base_url}/action/doSearch"
            
            # Parámetros de búsqueda
            params = {
                'AllField': query,
                'SeriesKey': '',  # Todas las series
                'pageSize': min(20, max_results),  # SAGE típicamente 20 por página
                'startPage': 0,
                'sortBy': 'relevancy'
            }
            
            # Filtros por año
            if start_year:
                params['AfterYear'] = start_year
            if end_year:
                params['BeforeYear'] = end_year
            
            page = 0
            while len(publications) < max_results:
                params['startPage'] = page
                
                # Respetar rate limit
                await self._respect_rate_limit()
                
                # Realizar búsqueda
                async with session.get(search_url, params=params) as response:
                    if response.status != 200:
                        logger.error(f"Error en SAGE: HTTP {response.status}")
                        break
                    
                    html = await response.text()
                    
                    # Parsear resultados
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Encontrar resultados de búsqueda
                    # SAGE usa diferentes selectores dependiendo de la versión del sitio
                    result_items = soup.find_all('div', class_='searchResultItem') or \
                                   soup.find_all('article', class_='search-result')
                    
                    if not result_items:
                        logger.info("No se encontraron más resultados en SAGE")
                        break
                    
                    # Procesar cada resultado
                    for item in result_items:
                        if len(publications) >= max_results:
                            break
                        
                        try:
                            pub = await self._parse_search_result(item, session)
                            if pub:
                                publications.append(pub)
                                logger.debug(f"SAGE: {len(publications)}/{max_results} - {pub.title[:50]}...")
                        except Exception as e:
                            logger.warning(f"Error procesando resultado de SAGE: {e}")
                            continue
                    
                    page += 1
                    
                    # Si no se encontraron resultados en esta página, terminar
                    if len(result_items) == 0:
                        break
            
            self.status = ScraperStatus.COMPLETED
            logger.info(f"SAGE: Búsqueda completada. {len(publications)} publicaciones encontradas")
            
            return publications
        
        except Exception as e:
            self.status = ScraperStatus.ERROR
            logger.error(f"Error en búsqueda de SAGE: {e}")
            raise
    
    async def _parse_search_result(
        self,
        item: BeautifulSoup,
        session: aiohttp.ClientSession
    ) -> Optional[Publication]:
        """
        Parsea un resultado de búsqueda de SAGE.
        
        Args:
            item: Elemento HTML del resultado
            session: Sesión aiohttp activa
        
        Returns:
            Publicación parseada o None si falla
        """
        try:
            # Extraer título
            title_elem = item.find('h4', class_='art_title') or \
                        item.find('h2', class_='search-result__title') or \
                        item.find('a', class_='ref-linked')
            
            if not title_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            
            # Extraer URL
            link_elem = title_elem if title_elem.name == 'a' else title_elem.find('a')
            url = None
            
            if link_elem and link_elem.has_attr('href'):
                url = link_elem['href']
                if not url.startswith('http'):
                    url = f"{self.base_url}{url}"
            
            # Extraer DOI de la URL o metadatos
            doi = None
            if url:
                doi_match = re.search(r'10\.\d{4,}/[\w\.\-/]+', url)
                if doi_match:
                    doi = doi_match.group(0)
            
            # Extraer autores
            authors_elem = item.find('div', class_='art_authors') or \
                          item.find('ul', class_='rlist--inline')
            authors = []
            
            if authors_elem:
                # Buscar todos los enlaces de autores
                author_links = authors_elem.find_all('a')
                for author_link in author_links:
                    author_name = author_link.get_text(strip=True)
                    if author_name:
                        authors.append(Author(name=author_name))
                
                # Si no hay enlaces, intentar extraer texto directo
                if not authors:
                    author_text = authors_elem.get_text(strip=True)
                    # Dividir por comas o "and"
                    author_names = re.split(r',\s*|\s+and\s+', author_text)
                    for name in author_names:
                        name = name.strip()
                        if name:
                            authors.append(Author(name=name))
            
            # Extraer año de publicación
            date_elem = item.find('div', class_='meta__epubDate') or \
                       item.find('span', class_='search-result__date')
            publication_date = None
            
            if date_elem:
                date_text = date_elem.get_text(strip=True)
                year_match = re.search(r'\b(19|20)\d{2}\b', date_text)
                if year_match:
                    try:
                        publication_date = datetime(int(year_match.group(0)), 1, 1).date()
                    except:
                        pass
            
            # Extraer journal
            journal_elem = item.find('div', class_='meta__journal') or \
                          item.find('span', class_='search-result__journal')
            journal = journal_elem.get_text(strip=True) if journal_elem else "SAGE Journal"
            
            # Extraer abstract (visible en la página de búsqueda o requiere visita)
            abstract_elem = item.find('div', class_='art_abstract') or \
                           item.find('div', class_='search-result__description')
            
            if abstract_elem:
                abstract = abstract_elem.get_text(strip=True)
            else:
                # Intentar obtener de la página individual
                abstract = await self._fetch_abstract(url, session) if url else ""
            
            # Crear publicación
            publication = Publication(
                title=title,
                abstract=abstract or "Abstract not available",
                authors=authors,
                doi=doi,
                url=url,
                publication_date=publication_date,
                journal=journal,
                source="sage"
            )
            
            return publication
        
        except Exception as e:
            logger.warning(f"Error parseando resultado de SAGE: {e}")
            return None
    
    async def _fetch_abstract(
        self,
        url: str,
        session: aiohttp.ClientSession
    ) -> str:
        """
        Obtiene el abstract de una publicación visitando su página.
        
        Args:
            url: URL de la publicación
            session: Sesión aiohttp activa
        
        Returns:
            Abstract de la publicación o cadena vacía
        """
        try:
            # Respetar rate limit
            await self._respect_rate_limit()
            
            async with session.get(url) as response:
                if response.status != 200:
                    return ""
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Buscar abstract (SAGE usa diferentes clases)
                abstract_elem = soup.find('div', class_='abstractSection') or \
                               soup.find('section', class_='abstract') or \
                               soup.find('div', {'id': 'abstract'})
                
                if abstract_elem:
                    # Remover elementos innecesarios
                    for tag in abstract_elem.find_all(['h2', 'h3', 'strong', 'label']):
                        tag.decompose()
                    
                    abstract = abstract_elem.get_text(strip=True)
                    return abstract
                
                return ""
        
        except Exception as e:
            logger.debug(f"No se pudo obtener abstract de {url}: {e}")
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
        logger.info(f"Descargando metadatos de SAGE: {publication_id}")
        
        try:
            # Construir URL
            url = f"{self.base_url}/doi/{publication_id}"
            
            session = await self._get_session()
            await self._respect_rate_limit()
            
            async with session.get(url) as response:
                if response.status != 200:
                    raise ValueError(f"No se pudo descargar publicación: HTTP {response.status}")
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extraer metadatos completos
                metadata = {
                    'doi': publication_id,
                    'url': url,
                    'source': 'sage',
                    # Agregar más campos según necesidad
                }
                
                self.status = ScraperStatus.COMPLETED
                return metadata
        
        except Exception as e:
            self.status = ScraperStatus.ERROR
            logger.error(f"Error descargando de SAGE: {e}")
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
    
    def parse_publication(self, raw_data: dict) -> Optional[Publication]:
        """
        Parsea datos crudos del scraper SAGE.
        
        Args:
            raw_data: Diccionario con datos crudos de SAGE Journals
        
        Returns:
            Objeto Publication parseado o None si falla
        """
        try:
            return self._parse_search_result(raw_data)
        except Exception as e:
            logger.error(f"Error parseando publicación SAGE: {e}")
            return None
    
    async def download_file(self, publication: Publication, file_format: str = "pdf") -> Optional[str]:
        """
        Descarga el archivo completo de una publicación SAGE.
        
        Nota: SAGE Journals requiere suscripción o pago para descargas.
        Este método retorna la URL de descarga pero no descarga el archivo.
        
        Args:
            publication: Publicación de la cual descargar el archivo
            file_format: Formato del archivo (solo pdf soportado)
        
        Returns:
            URL de descarga o None si no está disponible
        """
        if not publication.doi:
            logger.warning("No se puede descargar archivo sin DOI")
            return None
        
        # Construir URL de descarga (requiere suscripción)
        download_url = f"https://journals.sagepub.com/doi/pdf/{publication.doi}"
        logger.info(f"URL de descarga SAGE: {download_url}")
        logger.warning("Descarga directa requiere suscripción o pago")
        
        return download_url

