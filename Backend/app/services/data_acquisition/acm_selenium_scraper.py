"""
Scraper ACM con Selenium
=========================

Implementación del scraper de ACM Digital Library usando Selenium
para bypassear Cloudflare y autenticación.

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Course: Análisis de Algoritmos (2025-2), Universidad del Quindío
"""

import asyncio
import time
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from .selenium_scraper import SeleniumBaseScraper
from app.models.publication import Publication, Author
from app.config.settings import get_settings

logger = logging.getLogger(__name__)


class ACMSeleniumScraper(SeleniumBaseScraper):
    """
    Scraper para ACM Digital Library usando Selenium.
    
    ACM implementa Cloudflare y protecciones anti-bot que bloquean
    peticiones HTTP directas. Este scraper usa Selenium para simular
    un navegador real.
    """
    
    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        rate_limit: float = 1.0,
        timeout: int = 30,
        headless: bool = True
    ):
        """
        Inicializa el scraper de ACM con Selenium.
        
        Args:
            username: Usuario de ACM (opcional, para acceso institucional)
            password: Contraseña de ACM (opcional)
            rate_limit: Peticiones por segundo
            timeout: Timeout en segundos
            headless: Ejecutar sin interfaz gráfica
        """
        settings = get_settings()
        
        # Usar credenciales de configuración si no se proporcionan
        if username is None:
            username = settings.acm_username
        if password is None:
            password = settings.acm_password
        
        super().__init__(
            source_name="acm",
            base_url="https://dl.acm.org",
            username=username,
            password=password,
            rate_limit=rate_limit,
            timeout=timeout,
            headless=headless
        )
        
        logger.info(f"ACMSeleniumScraper inicializado (auth={'Sí' if username else 'No'})")
    
    def _authenticate(self, login_url: str = "https://dl.acm.org/login") -> bool:
        """
        Realiza autenticación en ACM Digital Library.
        
        ACM puede requerir autenticación institucional para acceso completo.
        
        Returns:
            True si la autenticación fue exitosa
        """
        if not self.username or not self.password:
            logger.info("No hay credenciales de ACM, continuando sin autenticación")
            return False
        
        try:
            driver = self._get_driver()
            
            logger.info("Navegando a página de login de ACM...")
            driver.get(login_url)
            
            # Esperar bypass de Cloudflare
            self._bypass_cloudflare()
            
            # Buscar campos de login
            username_field = self._wait_for_element(By.ID, "username", timeout=10)
            password_field = self._wait_for_element(By.ID, "password", timeout=10)
            
            # Ingresar credenciales
            username_field.clear()
            username_field.send_keys(self.username)
            
            password_field.clear()
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)
            
            # Esperar a que cargue página principal
            time.sleep(3)
            
            # Verificar si login fue exitoso
            if self._is_logged_in():
                logger.info("✓ Autenticación en ACM exitosa")
                self._save_cookies(f"acm_cookies_{self.username}.pkl")
                self.is_authenticated = True
                return True
            else:
                logger.warning("✗ Autenticación en ACM falló")
                return False
                
        except Exception as e:
            logger.error(f"Error en autenticación de ACM: {e}")
            return False
    
    def _is_logged_in(self) -> bool:
        """
        Verifica si el usuario está autenticado en ACM.
        
        Returns:
            True si está autenticado
        """
        try:
            # ACM muestra el nombre de usuario en la esquina cuando estás logueado
            driver = self._get_driver()
            page_source = driver.page_source
            
            # Verificar indicadores de sesión activa
            if self.username and self.username.lower() in page_source.lower():
                return True
            
            # Verificar botón de "Sign Out"
            if "sign out" in page_source.lower() or "logout" in page_source.lower():
                return True
            
            return False
        except:
            return False
    
    async def search(
        self,
        query: str,
        max_results: int = 100,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        publication_type: Optional[str] = None
    ) -> List[Publication]:
        """
        Busca publicaciones en ACM Digital Library usando Selenium.
        
        Args:
            query: Consulta de búsqueda
            max_results: Número máximo de resultados
            start_year: Año inicial (filtro)
            end_year: Año final (filtro)
            publication_type: Tipo de publicación
            
        Returns:
            Lista de publicaciones encontradas
        """
        self.status = "searching"
        logger.info(f"Iniciando búsqueda en ACM con Selenium: '{query}' (max: {max_results})")
        
        try:
            driver = self._get_driver()
            publications: List[Publication] = []
            
            # Construir URL de búsqueda
            search_url = f"{self.base_url}/action/doSearch"
            params = {
                'AllField': query,
                'pageSize': '50'  # ACM max por página
            }
            
            # Agregar filtros de año
            if start_year:
                params['AfterYear'] = str(start_year)
            if end_year:
                params['BeforeYear'] = str(end_year)
            
            # Construir URL completa
            url_with_params = f"{search_url}?" + "&".join(
                [f"{k}={v}" for k, v in params.items()]
            )
            
            logger.info(f"Navegando a: {url_with_params}")
            driver.get(url_with_params)
            
            # Esperar bypass de Cloudflare con indicadores específicos de ACM
            logger.info("⏳ Esperando carga completa (resuelve captcha si aparece)...")
            success_indicators = [
                "div.issue-item",           # Resultados en formato grid
                "div.search-result",        # Resultados en formato lista
                "ul.rlist--inline",         # Lista de resultados
                "div.items-results"         # Contenedor de resultados
            ]
            bypass_success = self._bypass_cloudflare(max_wait=120, success_indicators=success_indicators)
            
            if bypass_success:
                logger.info("✅ Página cargada correctamente, continuando con parseo...")
            else:
                logger.warning("⚠ Timeout alcanzado, intentando parsear de todos modos...")
            
            # Verificar que realmente hay resultados
            try:
                self._wait_for_element(By.CSS_SELECTOR, "div.issue-item, div.search-result", timeout=10)
                logger.info("✓ Elementos de resultados encontrados")
            except TimeoutException:
                logger.warning("⚠ No se encontraron elementos de resultados en ACM")
                # Intentar buscar con otro selector alternativo
                try:
                    self._wait_for_element(By.CLASS_NAME, "search-result", timeout=5)
                    logger.info("✓ Resultados encontrados con selector alternativo")
                except TimeoutException:
                    logger.error("✗ No se encontraron resultados en ACM")
                    return publications
            
            page = 0
            max_pages = 10  # Límite de seguridad para evitar loops infinitos
            
            while len(publications) < max_results and page < max_pages:
                # Respetar rate limit (esperar según configuración)
                if self.rate_limit > 0:
                    await asyncio.sleep(1.0 / self.rate_limit)
                
                # Obtener HTML de la página actual
                page_html = driver.page_source
                soup = BeautifulSoup(page_html, 'html.parser')
                
                # Parsear resultados
                result_items = soup.find_all('div', class_='issue-item')
                
                if not result_items:
                    logger.info("No hay más resultados en ACM")
                    break
                
                logger.info(f"Página {page + 1}: {len(result_items)} resultados encontrados")
                
                # DEBUG: Guardar HTML del primer item de la primera página
                if page == 0 and result_items:
                    sample_html = result_items[0].prettify()
                    
                    # Guardar a archivo para inspección
                    debug_file = Path(__file__).parent.parent.parent.parent / "acm_sample.html"
                    with open(debug_file, 'w', encoding='utf-8') as f:
                        f.write(sample_html)
                    logger.info(f"💾 HTML sample guardado en: {debug_file}")
                    
                    logger.info("=" * 80)
                    logger.info("HTML SAMPLE DEL PRIMER RESULTADO:")
                    logger.info(sample_html[:1500])
                    logger.info("=" * 80)
                
                # Parsear cada resultado
                for item in result_items:
                    if len(publications) >= max_results:
                        break
                    
                    try:
                        pub = self._parse_result_item(item)
                        if pub:
                            publications.append(pub)
                            logger.debug(
                                f"ACM: {len(publications)}/{max_results} - "
                                f"{pub.title[:50]}..."
                            )
                    except Exception as e:
                        logger.warning(f"Error parseando resultado de ACM: {e}")
                        continue
                
                # Intentar ir a siguiente página
                try:
                    next_button = driver.find_element(By.CLASS_NAME, "pagination__btn--next")
                    if "disabled" in next_button.get_attribute("class"):
                        logger.info("Última página alcanzada")
                        break
                    
                    next_button.click()
                    time.sleep(2)  # Esperar carga de página
                    page += 1
                    
                except NoSuchElementException:
                    logger.info("No hay botón de siguiente página")
                    break
            
            self.status = "completed"
            logger.info(f"✓ Búsqueda en ACM completada: {len(publications)} publicaciones")
            return publications
            
        except Exception as e:
            self.status = "error"
            logger.error(f"✗ Error en búsqueda de ACM con Selenium: {e}")
            raise
        finally:
            # No cerrar driver aquí, se reutiliza
            pass
    
    def _parse_result_item(self, item: BeautifulSoup) -> Optional[Publication]:
        """
        Parsea un resultado de búsqueda de ACM con múltiples estrategias.
        
        Args:
            item: Elemento HTML del resultado
            
        Returns:
            Publicación parseada o None
        """
        try:
            # Estrategia 1: Buscar título con múltiples selectores
            title = None
            title_selectors = [
                ('h3', 'issue-item__title'),        # Selector CORRECTO (H3, no H5)
                ('h5', 'issue-item__title'),        # Fallback H5
                ('span', 'hlFld-Title'),            # Selector alternativo ACM
            ]
            
            for tag, class_name in title_selectors:
                title_elem = item.find(tag, class_=class_name)
                if title_elem:
                    # El título puede estar en el <a> dentro del <h3>
                    title_link = title_elem.find('a')
                    if title_link:
                        title = title_link.get_text(strip=True)
                    else:
                        title = title_elem.get_text(strip=True)
                    
                    if title:
                        logger.debug(f"✓ Título encontrado: {title[:50]}...")
                        break
            
            if not title:
                logger.warning("⚠ No se encontró título en item")
                return None
            
            # Estrategia 2: Extraer URL y DOI
            import re
            doi = None
            url = None
            
            # Buscar enlaces en el item
            all_links = item.find_all('a', href=True)
            for link in all_links:
                href = link['href']
                
                # Si es URL relativa, hacerla absoluta
                if href.startswith('/'):
                    href = f"{self.base_url}{href}"
                
                # Buscar DOI en el href
                doi_match = re.search(r'10\.\d{4,}/[\w\.\-/]+', href)
                if doi_match:
                    doi = doi_match.group(0)
                    url = href
                    logger.debug(f"✓ DOI encontrado: {doi}")
                    break
            
            # Si no se encontró DOI, usar el primer enlace como URL
            if not url and all_links:
                url = all_links[0]['href']
                if url.startswith('/'):
                    url = f"{self.base_url}{url}"
                logger.debug(f"✓ URL sin DOI: {url[:50]}...")
            
            # Estrategia 3: Extraer autores (estructura: ul > li > a > span)
            authors = []
            
            # Buscar el contenedor <ul class="rlist--inline loa">
            authors_container = item.find('ul', class_='rlist--inline')
            if authors_container and 'loa' in authors_container.get('class', []):
                # Encontrar todos los <li> dentro del <ul>
                author_items = authors_container.find_all('li')
                for li in author_items:
                    # Dentro de cada <li>, buscar <a> → <span>
                    link = li.find('a')
                    if link:
                        span = link.find('span')
                        if span:
                            author_name = span.get_text(strip=True)
                        else:
                            # Si no hay span, tomar el texto del link
                            author_name = link.get_text(strip=True)
                    else:
                        # Si no hay link, tomar el texto del li
                        author_name = li.get_text(strip=True)
                    
                    if author_name and len(author_name) > 2:
                        author_name = author_name.replace('by ', '').strip()
                        if author_name not in [a.name for a in authors]:
                            authors.append(Author(name=author_name))
                
                if authors:
                    logger.debug(f"✓ {len(authors)} autores encontrados")
            
            # Fallback: buscar spans con clase hlFld-ContribAuthor
            if not authors:
                authors_elems = item.find_all('span', class_='hlFld-ContribAuthor')
                for author_elem in authors_elems:
                    author_name = author_elem.get_text(strip=True)
                    if author_name and len(author_name) > 2:
                        author_name = author_name.replace('by ', '').strip()
                        if author_name not in [a.name for a in authors]:
                            authors.append(Author(name=author_name))
                if authors:
                    logger.debug(f"✓ {len(authors)} autores (fallback)")
            
            # Estrategia 4: Extraer año de todo el texto del item
            year = None
            full_text = item.get_text()
            # Buscar años de 4 dígitos (1900-2099)
            year_matches = re.findall(r'\b(?:19|20)\d{2}\b', full_text)
            if year_matches:
                # Usar el primer año encontrado (convertir a int)
                year = int(year_matches[0])
                logger.debug(f"✓ Año encontrado: {year}")
            
            # Estrategia 5: Extraer abstract
            abstract = None
            abstract_selectors = [
                ('div', 'issue-item__abstract'),
                ('div', 'abstractSection'),
                ('p', 'shorttext')
            ]
            
            for tag, class_name in abstract_selectors:
                abstract_elem = item.find(tag, class_=class_name)
                if abstract_elem:
                    abstract = abstract_elem.get_text(strip=True)
                    if abstract:
                        logger.debug(f"✓ Abstract encontrado ({len(abstract)} chars)")
                        break
            
            # Crear publicación
            publication = Publication(
                title=title,
                authors=authors,
                publication_date=year,
                doi=doi,
                url=url,
                abstract=abstract,
                source="acm"
            )
            
            return publication
            
        except Exception as e:
            logger.warning(f"Error parseando item de ACM: {e}")
            return None
    
    async def download_metadata(self, publication_id: str) -> Optional[Publication]:
        """
        Descarga metadatos completos de una publicación específica por DOI/ID.
        
        Args:
            publication_id: DOI o identificador de la publicación en ACM
        
        Returns:
            Publication con metadatos completos o None si falla
        """
        try:
            driver = self._get_driver()
            
            # Construir URL de la publicación
            url = f"{self.base_url}/doi/{publication_id}"
            driver.get(url)
            
            # Bypass Cloudflare
            self._bypass_cloudflare(max_wait=30)
            
            # Parsear página con BeautifulSoup
            page_html = driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')
            
            # Aquí iría la lógica de extracción específica de la página de detalle
            # Por ahora, simplemente retornamos None para el test básico
            logger.warning(f"download_metadata no implementado completamente para {publication_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error descargando metadata de {publication_id}: {e}")
            return None
    
    def parse_publication(self, raw_data: Dict[str, Any]) -> Optional[Publication]:
        """
        Parsea datos crudos de ACM a objeto Publication.
        
        Args:
            raw_data: Diccionario con datos crudos de ACM
        
        Returns:
            Objeto Publication parseado o None si falla
        """
        try:
            # Extraer campos básicos
            title = raw_data.get('title', '')
            doi = raw_data.get('doi', None)
            url = raw_data.get('url', None)
            abstract = raw_data.get('abstract', None)
            year = raw_data.get('year', None)
            
            # Parsear autores
            authors = []
            for author_data in raw_data.get('authors', []):
                if isinstance(author_data, str):
                    authors.append(Author(name=author_data))
                elif isinstance(author_data, dict):
                    authors.append(Author(
                        name=author_data.get('name', ''),
                        affiliation=author_data.get('affiliation', None)
                    ))
            
            # Crear publicación
            publication = Publication(
                title=title,
                authors=authors,
                publication_date=year,
                doi=doi,
                url=url,
                abstract=abstract,
                source="acm"
            )
            
            return publication
            
        except Exception as e:
            logger.error(f"Error parseando datos crudos: {e}")
            return None
    
    async def download_file(
        self,
        publication: Publication,
        file_format: str = "pdf"
    ) -> Optional[str]:
        """
        Descarga el archivo PDF de una publicación de ACM.
        
        Args:
            publication: Objeto Publication con los datos de la publicación
            file_format: Formato del archivo (por defecto 'pdf')
        
        Returns:
            Ruta local del archivo descargado o None si falla
        """
        try:
            # La descarga de archivos requiere autenticación y permisos especiales
            # Por ahora, retornamos None para indicar que no está implementado
            logger.warning(f"download_file no implementado para ACM (requiere suscripción)")
            return None
            
        except Exception as e:
            logger.error(f"Error descargando archivo: {e}")
            return None
