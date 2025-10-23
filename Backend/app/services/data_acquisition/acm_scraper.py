"""
Scraper para ACM Digital Library
=================================

Implementa el scraper para ACM Digital Library usando web scraping y su API.

ACM (Association for Computing Machinery) es una de las principales bibliotecas
digitales en ciencias de la computación.

API Documentation: https://dl.acm.org/

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


class ACMScraper(BaseScraper):
    """
    Scraper para ACM Digital Library.
    
    ACM proporciona acceso a publicaciones en ciencias de la computación,
    ingeniería y tecnologías relacionadas.
    
    Notas:
    - Requiere acceso institucional para contenido completo
    - API limitada, principalmente se usa web scraping
    - Rate limiting estricto
    
    Estrategia:
    1. Búsqueda a través de la interfaz web de ACM
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
        Inicializa el scraper de ACM.
        
        Args:
            api_key: No utilizado actualmente (ACM no tiene API pública robusta)
            rate_limit: Peticiones por segundo (conservador para evitar bloqueos)
            timeout: Timeout de peticiones en segundos
        """
        super().__init__(
            source_name="acm",
            base_url="https://dl.acm.org",
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
            logger.info("Sesión de ACM cerrada")
    
    async def search(
        self,
        query: str,
        max_results: int = 100,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        publication_type: Optional[str] = None
    ) -> List[Publication]:
        """
        Busca publicaciones en ACM Digital Library.
        
        Args:
            query: Cadena de búsqueda
            max_results: Número máximo de resultados
            start_year: Año de inicio (filtro)
            end_year: Año final (filtro)
            publication_type: Tipo de publicación (ej: 'journal', 'conference')
        
        Returns:
            Lista de publicaciones encontradas
        """
        self.status = ScraperStatus.SEARCHING
        logger.info(f"Buscando en ACM Digital Library: '{query}' (max: {max_results})")
        
        session = await self._get_session()
        publications: List[Publication] = []
        
        try:
            # Construir URL de búsqueda
            search_url = f"{self.base_url}/action/doSearch"
            
            # Parámetros de búsqueda
            params = {
                'AllField': query,
                'pageSize': min(50, max_results),  # ACM max: 50 por página
                'startPage': 0
            }
            
            # Filtros por año
            if start_year and end_year:
                params['AfterYear'] = start_year
                params['BeforeYear'] = end_year
            
            page = 0
            while len(publications) < max_results:
                params['startPage'] = page
                
                # Respetar rate limit
                await self._respect_rate_limit()
                
                # Realizar búsqueda
                async with session.get(search_url, params=params) as response:
                    if response.status != 200:
                        logger.error(f"Error en ACM: HTTP {response.status}")
                        break
                    
                    html = await response.text()
                    
                    # Parsear resultados
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Encontrar resultados de búsqueda
                    result_items = soup.find_all('div', class_='issue-item')
                    
                    if not result_items:
                        logger.info("No se encontraron más resultados en ACM")
                        break
                    
                    # Procesar cada resultado
                    for item in result_items:
                        if len(publications) >= max_results:
                            break
                        
                        try:
                            pub = await self._parse_search_result(item, session)
                            if pub:
                                publications.append(pub)
                                logger.debug(f"ACM: {len(publications)}/{max_results} - {pub.title[:50]}...")
                        except Exception as e:
                            logger.warning(f"Error procesando resultado de ACM: {e}")
                            continue
                    
                    page += 1
                    
                    # Si no se encontraron resultados en esta página, terminar
                    if len(result_items) == 0:
                        break
            
            self.status = ScraperStatus.COMPLETED
            logger.info(f"ACM: Búsqueda completada. {len(publications)} publicaciones encontradas")
            
            return publications
        
        except Exception as e:
            self.status = ScraperStatus.ERROR
            logger.error(f"Error en búsqueda de ACM: {e}")
            raise
    
    async def _parse_search_result(
        self,
        item: BeautifulSoup,
        session: aiohttp.ClientSession
    ) -> Optional[Publication]:
        """
        Parsea un resultado de búsqueda de ACM.
        
        Args:
            item: Elemento HTML del resultado
            session: Sesión aiohttp activa
        
        Returns:
            Publicación parseada o None si falla
        """
        try:
            # Extraer título
            title_elem = item.find('h5', class_='issue-item__title')
            if not title_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            
            # Extraer DOI y URL
            doi_elem = item.find('a', class_='issue-item__doi')
            doi = None
            url = None
            
            if doi_elem and doi_elem.has_attr('href'):
                url = doi_elem['href']
                if not url.startswith('http'):
                    url = f"{self.base_url}{url}"
                
                # Extraer DOI de la URL
                doi_match = re.search(r'10\.\d{4,}/[\w\.\-/]+', url)
                if doi_match:
                    doi = doi_match.group(0)
            
            # Extraer autores
            authors_elem = item.find_all('li', class_='loa__item')
            authors = []
            
            for author_elem in authors_elem:
                author_name = author_elem.get_text(strip=True)
                if author_name:
                    authors.append(Author(name=author_name))
            
            # Extraer año de publicación
            date_elem = item.find('span', class_='dot-separator')
            publication_date = None
            
            if date_elem:
                date_text = date_elem.get_text(strip=True)
                year_match = re.search(r'\b(19|20)\d{2}\b', date_text)
                if year_match:
                    try:
                        publication_date = datetime(int(year_match.group(0)), 1, 1).date()
                    except:
                        pass
            
            # Extraer abstract (requiere visitar página individual)
            abstract = await self._fetch_abstract(url, session) if url else ""
            
            # Extraer tipo de publicación
            pub_type_elem = item.find('span', class_='issue-item__detail')
            journal = pub_type_elem.get_text(strip=True) if pub_type_elem else "ACM Publication"
            
            # Crear publicación
            publication = Publication(
                title=title,
                abstract=abstract or "Abstract not available",
                authors=authors,
                doi=doi,
                url=url,
                publication_date=publication_date,
                journal=journal,
                source="acm"
            )
            
            return publication
        
        except Exception as e:
            logger.warning(f"Error parseando resultado de ACM: {e}")
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
                
                # Buscar abstract
                abstract_elem = soup.find('div', class_='abstractSection')
                
                if abstract_elem:
                    # Remover elementos innecesarios
                    for tag in abstract_elem.find_all(['h2', 'h3', 'strong']):
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
        logger.info(f"Descargando metadatos de ACM: {publication_id}")
        
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
                
                # Extraer metadatos (implementación similar a _parse_search_result)
                metadata = {
                    'doi': publication_id,
                    'url': url,
                    'source': 'acm',
                    # Agregar más campos según necesidad
                }
                
                self.status = ScraperStatus.COMPLETED
                return metadata
        
        except Exception as e:
            self.status = ScraperStatus.ERROR
            logger.error(f"Error descargando de ACM: {e}")
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
            # Delegar a BibTeXParser
            from .parsers.bibtex_parser import BibTeXParser
            parser = BibTeXParser()
            return parser.export_publications(publications)
        elif format.lower() == 'ris':
            # Delegar a RISParser
            from .parsers.ris_parser import RISParser
            parser = RISParser()
            return parser.export_publications(publications)
        elif format.lower() == 'csv':
            # Delegar a CSVParser
            from .parsers.csv_parser import CSVParser
            parser = CSVParser()
            return parser.export_publications(publications)
        else:
            raise ValueError(f"Formato no soportado: {format}")
    
    def parse_publication(self, raw_data: dict) -> Optional[Publication]:
        """
        Parsea datos crudos del scraper ACM.
        
        Args:
            raw_data: Diccionario con datos crudos de ACM Digital Library
        
        Returns:
            Objeto Publication parseado o None si falla
        """
        try:
            return self._parse_search_result(raw_data)
        except Exception as e:
            logger.error(f"Error parseando publicación ACM: {e}")
            return None
    
    async def download_file(self, publication: Publication, file_format: str = "pdf") -> Optional[str]:
        """
        Descarga el archivo completo de una publicación ACM.
        
        Nota: ACM Digital Library requiere autenticación institucional para descargas.
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
        
        # Construir URL de descarga (requiere autenticación)
        download_url = f"https://dl.acm.org/doi/pdf/{publication.doi}"
        logger.info(f"URL de descarga ACM: {download_url}")
        logger.warning("Descarga directa requiere autenticación institucional")
        
        return download_url
