"""
Scraper para CrossRef API
==========================

Implementa el scraper para la API de CrossRef, una fuente abierta y gratuita
de metadatos bibliográficos que indexa millones de publicaciones científicas.

CrossRef proporciona una API REST pública sin necesidad de autenticación para
búsquedas básicas.

API Documentation: https://api.crossref.org/swagger-ui/index.html

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Course: Análisis de Algoritmos (2025-2), Universidad del Quindío
"""

import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from .base_scraper import BaseScraper, ScraperStatus
from app.models.publication import Publication, Author

logger = logging.getLogger(__name__)


class CrossRefScraper(BaseScraper):
    """
    Scraper para la API de CrossRef.
    
    CrossRef es una organización sin fines de lucro que proporciona
    servicios de registro de DOI y metadatos bibliográficos.
    
    Ventajas:
    - API gratuita y sin autenticación requerida
    - Cobertura amplia de revistas científicas
    - Metadatos de alta calidad
    - Soporta filtros avanzados
    
    Rate Limit:
    - API pública: ~50 peticiones por segundo (recomendado: 1 por segundo)
    - Con API token: Mayor límite (requiere registro)
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        rate_limit: float = 1.0,
        timeout: int = 30,
        user_agent: str = "BibliometricAnalysis/1.0 (Universidad del Quindio)"
    ):
        """
        Inicializa el scraper de CrossRef.
        
        Args:
            api_key: Token de API (opcional, mejora rate limits)
            rate_limit: Peticiones por segundo
            timeout: Timeout de peticiones en segundos
            user_agent: User-Agent para identificación cortés
        """
        super().__init__(
            source_name="crossref",
            base_url="https://api.crossref.org",
            api_key=api_key,
            rate_limit=rate_limit,
            timeout=timeout
        )
        
        self.user_agent = user_agent
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Obtiene o crea una sesión aiohttp."""
        if self.session is None or self.session.closed:
            headers = {
                'User-Agent': self.user_agent
            }
            
            # Agregar API key si está disponible
            if self.api_key:
                headers['Crossref-Plus-API-Token'] = f'Bearer {self.api_key}'
            
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
            logger.info("Sesión de CrossRef cerrada")
    
    async def search(
        self,
        query: str,
        max_results: int = 100,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        publication_type: Optional[str] = None
    ) -> List[Publication]:
        """
        Busca publicaciones en CrossRef.
        
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
        logger.info(f"Buscando en CrossRef: '{query}' (max: {max_results})")
        
        session = await self._get_session()
        publications: List[Publication] = []
        
        # Configurar parámetros de búsqueda
        rows_per_page = min(100, max_results)  # CrossRef max: 1000
        offset = 0
        
        try:
            while len(publications) < max_results:
                # Construir URL de búsqueda
                url = f"{self.base_url}/works"
                params = {
                    'query': query,
                    'rows': rows_per_page,
                    'offset': offset,
                    'select': 'DOI,title,abstract,author,published-print,published-online,container-title,type,URL,is-referenced-by-count,publisher,volume,issue,page,ISSN,subject'
                }
                
                # Agregar filtros opcionales
                filters = []
                if start_year:
                    filters.append(f'from-pub-date:{start_year}')
                if end_year:
                    filters.append(f'until-pub-date:{end_year}')
                if publication_type:
                    filters.append(f'type:{publication_type}')
                
                if filters:
                    params['filter'] = ','.join(filters)
                
                # Realizar petición
                logger.debug(f"GET {url} con offset={offset}")
                
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        error_msg = f"Error en CrossRef API: HTTP {response.status}"
                        logger.error(error_msg)
                        self.errors.append(error_msg)
                        break
                    
                    data = await response.json()
                    
                    # Verificar si hay resultados
                    items = data.get('message', {}).get('items', [])
                    
                    if not items:
                        logger.info("No hay más resultados disponibles")
                        break
                    
                    # Actualizar total de resultados
                    self.total_results = data.get('message', {}).get('total-results', 0)
                    
                    # Parsear cada publicación
                    for item in items:
                        try:
                            publication = self.parse_publication(item)
                            if publication:
                                publications.append(publication)
                                self.downloaded_count += 1
                                
                                if len(publications) >= max_results:
                                    break
                        
                        except Exception as e:
                            error_msg = f"Error parseando publicación: {e}"
                            logger.warning(error_msg)
                            self.errors.append(error_msg)
                    
                    # Incrementar offset para siguiente página
                    offset += rows_per_page
                    
                    # Rate limiting
                    await asyncio.sleep(self.rate_limit)
                    
                    # Si obtuvimos menos resultados de los solicitados, no hay más páginas
                    if len(items) < rows_per_page:
                        break
        
        except Exception as e:
            error_msg = f"Error en búsqueda de CrossRef: {e}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            self.status = ScraperStatus.ERROR
            raise
        
        self.status = ScraperStatus.COMPLETED
        logger.info(f"Búsqueda completada: {len(publications)} publicaciones descargadas")
        
        return publications
    
    def parse_publication(self, raw_data: Dict[str, Any]) -> Optional[Publication]:
        """
        Parsea datos crudos de CrossRef a objeto Publication.
        
        Args:
            raw_data: Diccionario con datos de CrossRef API
        
        Returns:
            Objeto Publication o None si falla
        """
        try:
            # Extraer título
            title_list = raw_data.get('title', [])
            title = title_list[0] if title_list else None
            
            if not title:
                logger.warning("Publicación sin título, omitiendo")
                return None
            
            # Extraer abstract
            abstract = raw_data.get('abstract', '')
            
            # Si no hay abstract, usar el título como abstract (mínimo requerido)
            if not abstract or len(abstract) < 50:
                # Intentar construir abstract a partir de otros campos
                subtitle = raw_data.get('subtitle', [])
                short_title = raw_data.get('short-title', [])
                
                abstract_parts = [title]
                if subtitle:
                    abstract_parts.append(subtitle[0])
                if short_title:
                    abstract_parts.append(short_title[0])
                
                abstract = " - ".join(abstract_parts)
                
                # Si aún es muy corto, rellenar con información del journal
                if len(abstract) < 50:
                    container_title = raw_data.get('container-title', [])
                    if container_title:
                        abstract += f" - Published in {container_title[0]}"
            
            # Extraer autores
            authors = []
            for author_data in raw_data.get('author', []):
                author_name = f"{author_data.get('given', '')} {author_data.get('family', '')}".strip()
                
                if author_name:
                    # Extraer ORCID y limpiar URLs
                    orcid = None
                    if 'ORCID' in author_data:
                        orcid_raw = author_data['ORCID']
                        # Remover todas las variantes de URL
                        orcid = orcid_raw.replace('https://orcid.org/', '') \
                                        .replace('http://orcid.org/', '') \
                                        .strip()
                    
                    author = Author(
                        name=author_name,
                        affiliation=self._extract_affiliation(author_data),
                        orcid=orcid
                    )
                    authors.append(author)
            
            # Extraer DOI
            doi = raw_data.get('DOI')
            
            # Extraer fecha de publicación
            publication_date = None
            publication_year = None
            
            # Intentar con múltiples fuentes de fecha en orden de prioridad
            date_sources = [
                raw_data.get('published-print'),
                raw_data.get('published-online'),
                raw_data.get('published'),
                raw_data.get('issued'),
                raw_data.get('created')
            ]
            
            for pub_date in date_sources:
                if pub_date and 'date-parts' in pub_date:
                    date_parts = pub_date['date-parts'][0] if pub_date['date-parts'] else []
                    if date_parts and len(date_parts) > 0:
                        publication_year = date_parts[0]
                        # Intentar construir fecha completa
                        try:
                            if len(date_parts) >= 3:
                                publication_date = datetime(
                                    date_parts[0], 
                                    date_parts[1], 
                                    date_parts[2]
                                ).date()
                        except:
                            pass
                        break  # Usar la primera fecha válida encontrada
            
            # Log si no se encontró el año
            if not publication_year:
                logger.debug(f"No se pudo extraer año para: {title[:50]}...")
            
            # Extraer journal
            container_title = raw_data.get('container-title', [])
            journal = container_title[0] if container_title else None
            
            # Si no hay journal, intentar con short-container-title
            if not journal:
                short_container = raw_data.get('short-container-title', [])
                journal = short_container[0] if short_container else None
            
            # Log si no se encontró el journal
            if not journal:
                logger.debug(f"No se pudo extraer journal para: {title[:50]}...")
            
            # Extraer keywords de subjects
            subjects = raw_data.get('subject', [])
            keywords = [subj.lower() for subj in subjects]
            
            # Extraer otros metadatos
            url = raw_data.get('URL')
            citation_count = raw_data.get('is-referenced-by-count', 0)
            publisher = raw_data.get('publisher')
            volume = raw_data.get('volume')
            issue = raw_data.get('issue')
            page = raw_data.get('page')
            issn_list = raw_data.get('ISSN', [])
            issn = issn_list[0] if issn_list else None
            
            # Determinar tipo de publicación
            pub_type_map = {
                'journal-article': 'article',
                'proceedings-article': 'conference',
                'book-chapter': 'book_chapter',
                'posted-content': 'article',
                'monograph': 'book_chapter'
            }
            crossref_type = raw_data.get('type', 'journal-article')
            publication_type = pub_type_map.get(crossref_type, 'article')
            
            # Crear objeto Publication
            publication = Publication(
                title=self._sanitize_text(title),
                abstract=self._sanitize_text(abstract),
                authors=authors,
                keywords=keywords,
                doi=doi,
                publication_date=publication_date,
                publication_year=publication_year,
                journal=self._sanitize_text(journal) if journal else None,
                volume=volume,
                issue=issue,
                pages=page,
                publisher=self._sanitize_text(publisher) if publisher else None,
                source=self.source_name,
                source_id=doi,
                url=url,
                citation_count=citation_count,
                publication_type=publication_type,
                issn=issn
            )
            
            # Generar ID
            publication.id = publication.generate_id()
            
            # Log de verificación de campos importantes
            logger.info(f"✓ Parseado: {title[:60]}... | Year: {publication_year or 'N/A'} | Journal: {journal[:40] if journal else 'N/A'}")
            
            return publication
        
        except Exception as e:
            logger.error(f"Error parseando publicación de CrossRef: {e}")
            logger.debug(f"Datos crudos: {raw_data}")
            return None
    
    def _extract_affiliation(self, author_data: Dict) -> Optional[str]:
        """Extrae afiliación del autor si está disponible."""
        affiliations = author_data.get('affiliation', [])
        if affiliations:
            affiliation_names = [aff.get('name', '') for aff in affiliations]
            return ', '.join(filter(None, affiliation_names))
        return None
    
    async def download_metadata(self, publication_id: str) -> Optional[Publication]:
        """
        Descarga metadatos completos de una publicación por DOI.
        
        Args:
            publication_id: DOI de la publicación
        
        Returns:
            Objeto Publication con metadatos completos
        """
        self.status = ScraperStatus.DOWNLOADING
        logger.info(f"Descargando metadatos para DOI: {publication_id}")
        
        session = await self._get_session()
        
        try:
            url = f"{self.base_url}/works/{publication_id}"
            
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Error descargando DOI {publication_id}: HTTP {response.status}")
                    return None
                
                data = await response.json()
                item = data.get('message', {})
                
                publication = self.parse_publication(item)
                
                if publication:
                    self.downloaded_count += 1
                
                return publication
        
        except Exception as e:
            logger.error(f"Error descargando metadatos: {e}")
            return None
    
    async def download_file(
        self,
        publication: Publication,
        file_format: str = "pdf"
    ) -> Optional[str]:
        """
        CrossRef no proporciona descarga directa de PDFs.
        
        Esta funcionalidad requeriría acceso a la editorial del artículo.
        """
        logger.warning("CrossRef no soporta descarga directa de archivos PDF")
        return None
    
    async def get_publication_types(self) -> List[str]:
        """
        Obtiene la lista de tipos de publicación soportados por CrossRef.
        
        Returns:
            Lista de tipos de publicación
        """
        session = await self._get_session()
        
        try:
            url = f"{self.base_url}/types"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get('message', {}).get('items', [])
                    return [item.get('id') for item in items]
                
        except Exception as e:
            logger.error(f"Error obteniendo tipos de publicación: {e}")
        
        return []


# Ejemplo de uso
async def main():
    """Función de ejemplo para probar el scraper."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    scraper = CrossRefScraper(rate_limit=1.0)
    
    try:
        # Buscar publicaciones sobre IA Generativa
        publications = await scraper.search(
            query="generative artificial intelligence",
            max_results=10,
            start_year=2023
        )
        
        print(f"\n{'='*80}")
        print(f"RESULTADOS DE BÚSQUEDA EN CROSSREF")
        print(f"{'='*80}")
        print(f"Query: 'generative artificial intelligence'")
        print(f"Resultados encontrados: {len(publications)}")
        print(f"{'='*80}\n")
        
        # Mostrar primeras 3 publicaciones
        for i, pub in enumerate(publications[:3], 1):
            print(f"\n{i}. {pub.title}")
            print(f"   Autores: {', '.join(pub.get_author_names()[:3])}")
            print(f"   Año: {pub.publication_year}")
            print(f"   Journal: {pub.journal}")
            print(f"   DOI: {pub.doi}")
            print(f"   Citas: {pub.citation_count}")
            print(f"   Abstract: {pub.abstract[:150]}...")
        
        # Exportar a BibTeX
        bibtex = scraper.export_to_format(publications, scraper.ExportFormat.BIBTEX)
        with open('crossref_results.bib', 'w', encoding='utf-8') as f:
            f.write(bibtex)
        
        print(f"\n{'='*80}")
        print("Resultados exportados a: crossref_results.bib")
        print(f"{'='*80}\n")
    
    finally:
        await scraper.close()


if __name__ == "__main__":
    asyncio.run(main())
