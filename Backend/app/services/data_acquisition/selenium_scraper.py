"""
Scraper Base con Selenium
==========================

Clase base para scrapers que utilizan Selenium para evitar bloqueos
de Cloudflare y otras protecciones anti-bot.

Características:
- Bypass de Cloudflare y protecciones anti-bot
- Autenticación automática con credenciales
- Manejo de cookies y sesiones persistentes
- Detección automática de ChromeDriver

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Course: Análisis de Algoritmos (2025-2), Universidad del Quindío
"""

import time
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException,
    WebDriverException
)

from .base_scraper import BaseScraper, ScraperStatus
from app.config.settings import get_settings

logger = logging.getLogger(__name__)


class SeleniumBaseScraper(BaseScraper):
    """
    Clase base para scrapers que usan Selenium para bypass de anti-bot.
    
    Ventajas de usar Selenium:
    - Bypasea Cloudflare y protecciones similares
    - Simula navegador real (no es detectado como bot)
    - Permite autenticación automática
    - Maneja JavaScript dinámico
    
    Desventajas:
    - Más lento que requests/aiohttp
    - Mayor consumo de recursos
    - Requiere ChromeDriver instalado
    """
    
    def __init__(
        self,
        source_name: str,
        base_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        rate_limit: float = 1.0,
        timeout: int = 30,
        headless: bool = True
    ):
        """
        Inicializa el scraper con Selenium.
        
        Args:
            source_name: Nombre de la fuente de datos
            base_url: URL base del sitio
            username: Usuario para autenticación (opcional)
            password: Contraseña para autenticación (opcional)
            rate_limit: Peticiones por segundo
            timeout: Timeout en segundos
            headless: Si True, ejecuta navegador sin interfaz gráfica
        """
        super().__init__(
            source_name=source_name,
            base_url=base_url,
            api_key=None,
            rate_limit=rate_limit,
            timeout=timeout
        )
        
        self.username = username
        self.password = password
        self.headless = headless
        self.driver: Optional[uc.Chrome] = None
        self.is_authenticated = False
        
        settings = get_settings()
        self.selenium_implicit_wait = settings.selenium_implicit_wait
        self.selenium_page_load_timeout = settings.selenium_page_load_timeout
        
        logger.info(
            f"SeleniumBaseScraper inicializado para {source_name}: "
            f"headless={headless}, timeout={timeout}s"
        )
    
    def _create_driver(self) -> uc.Chrome:
        """
        Crea una instancia de Chrome con undetected-chromedriver.
        
        undetected-chromedriver es una versión modificada que bypasea
        detecciones de automatización (Cloudflare, DataDome, etc.)
        """
        try:
            options = uc.ChromeOptions()
            
            if self.headless:
                options.add_argument('--headless=new')
            
            # Argumentos para evitar detección
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            
            # User agent realista
            options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            )
            
            # Crear driver con undetected_chromedriver
            # version_main=None permite que detecte la versión de Chrome instalada automáticamente
            driver = uc.Chrome(options=options, use_subprocess=True, version_main=None)
            
            # Configurar timeouts (aumentados para dar tiempo al usuario)
            driver.implicitly_wait(self.selenium_implicit_wait)
            driver.set_page_load_timeout(max(self.selenium_page_load_timeout, 60))  # Mínimo 60s
            
            # Maximizar ventana para mejor visibilidad
            if not self.headless:
                driver.maximize_window()
            
            logger.info(f"ChromeDriver creado exitosamente (headless={self.headless})")
            return driver
            
        except Exception as e:
            logger.error(f"Error creando ChromeDriver: {e}")
            raise
    
    def _get_driver(self) -> uc.Chrome:
        """Obtiene o crea el driver de Selenium."""
        if self.driver is None:
            self.driver = self._create_driver()
        return self.driver
    
    async def close(self):
        """Cierra el navegador y limpia recursos."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info(f"Driver de {self.source_name} cerrado correctamente")
            except Exception as e:
                logger.warning(f"Error cerrando driver: {e}")
            finally:
                self.driver = None
                self.is_authenticated = False
    
    def _wait_for_element(
        self, 
        by: By, 
        value: str, 
        timeout: int = 10
    ) -> Any:
        """
        Espera a que un elemento aparezca en la página.
        
        Args:
            by: Método de búsqueda (By.ID, By.XPATH, etc.)
            value: Valor del selector
            timeout: Tiempo máximo de espera
            
        Returns:
            El elemento encontrado
            
        Raises:
            TimeoutException: Si el elemento no aparece
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"Timeout esperando elemento: {by}={value}")
            raise
    
    def _wait_for_clickable(
        self, 
        by: By, 
        value: str, 
        timeout: int = 10
    ) -> Any:
        """
        Espera a que un elemento sea clickeable.
        
        Args:
            by: Método de búsqueda
            value: Valor del selector
            timeout: Tiempo máximo de espera
            
        Returns:
            El elemento clickeable
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"Timeout esperando elemento clickeable: {by}={value}")
            raise
    
    def _accept_cookies(self):
        """
        Intenta aceptar el banner de cookies automáticamente.
        
        Busca botones comunes de aceptar cookies y hace clic.
        """
        try:
            # Lista de selectores comunes para botones de cookies
            cookie_selectors = [
                "//button[contains(translate(., 'ACCEPT', 'accept'), 'accept')]",
                "//button[contains(translate(., 'ACEPTAR', 'aceptar'), 'aceptar')]",
                "//button[contains(@id, 'accept')]",
                "//button[contains(@class, 'accept')]",
                "//a[contains(translate(., 'ACCEPT', 'accept'), 'accept')]",
                "//div[contains(@class, 'cookie')]//button",
                "#onetrust-accept-btn-handler",  # OneTrust (común)
                ".cky-btn-accept",  # CookieYes
            ]
            
            for selector in cookie_selectors:
                try:
                    if selector.startswith("//"):
                        # XPath
                        button = WebDriverWait(self.driver, 2).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        # CSS Selector
                        button = WebDriverWait(self.driver, 2).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    button.click()
                    logger.info(f"✓ Banner de cookies aceptado: {selector}")
                    time.sleep(1)  # Esperar a que se procese
                    return True
                    
                except (TimeoutException, NoSuchElementException):
                    continue
                except Exception as e:
                    logger.debug(f"Error intentando selector {selector}: {e}")
                    continue
            
            logger.debug("No se encontró banner de cookies (o ya fue aceptado)")
            return False
            
        except Exception as e:
            logger.debug(f"Error aceptando cookies: {e}")
            return False
    
    def _bypass_cloudflare(self, max_wait: int = 60, success_indicators: list = None):
        """
        Espera a que Cloudflare complete su verificación.
        
        Detecta continuamente si el captcha fue resuelto buscando:
        1. Desaparición del texto "just a moment" / "cloudflare"
        2. Aparición de elementos específicos (success_indicators)
        3. Contenido sustancial en body (>100 chars)
        
        Args:
            max_wait: Tiempo máximo de espera en segundos (default: 60s)
            success_indicators: Lista de selectores CSS que indican éxito
        """
        logger.info("⏳ Esperando bypass de Cloudflare (resuelve captcha si aparece)...")
        start_time = time.time()
        cookies_accepted = False
        check_count = 0
        force_check_after = 30  # Después de 30s, ignorar detección de Cloudflare y revisar contenido
        
        while time.time() - start_time < max_wait:
            check_count += 1
            elapsed = int(time.time() - start_time)
            
            try:
                # Verificar si estamos en página de Cloudflare
                page_source = self.driver.page_source.lower()
                
                # Mostrar progreso cada 20 verificaciones (~10s con checks cada 0.5s)
                if check_count % 20 == 0:
                    logger.info(f"⏱ Esperando... ({elapsed}s/{max_wait}s)")
                
                # Después de 30s, forzar verificación de contenido (asumir captcha resuelto)
                skip_cloudflare_check = elapsed > force_check_after
                
                if skip_cloudflare_check:
                    logger.info(f"⏰ Modo detección forzada activado ({elapsed}s)")
                else:
                    # Detectar challenge activo de Cloudflare (no solo la palabra "cloudflare")
                    is_cloudflare_challenge = (
                        "just a moment" in page_source or 
                        "checking your browser" in page_source or
                        "cloudflare-static" in page_source or
                        ("cloudflare" in page_source and "challenge" in page_source)
                    )
                    
                    if is_cloudflare_challenge:
                        logger.debug(f"🔄 Challenge de Cloudflare activo ({elapsed}s)")
                        time.sleep(0.5)  # Verificar más frecuentemente (antes: 2s)
                        continue
                
                # Verificar si la página cargó correctamente (tanto en modo normal como forzado)
                ready_state = self.driver.execute_script("return document.readyState")
                if ready_state == "complete":
                    # Intentar aceptar cookies una vez
                    if not cookies_accepted:
                        self._accept_cookies()
                        cookies_accepted = True
                        time.sleep(1)  # Esperar después de aceptar cookies
                    
                    # Verificar si hay contenido real (no solo error)
                    body_text = self.driver.find_element(By.TAG_NAME, "body").text
                    if len(body_text) > 100:  # Tiene contenido sustancial
                        # Verificar indicadores específicos de éxito (ej: resultados)
                        found_indicator = False
                        if success_indicators:
                            for indicator in success_indicators:
                                try:
                                    elements = self.driver.find_elements(By.CSS_SELECTOR, indicator)
                                    if elements:
                                        logger.info(f"✅ Captcha resuelto! Encontrado: {indicator} ({elapsed}s)")
                                        found_indicator = True
                                        break
                                except:
                                    pass
                        
                        # Si no hay indicadores específicos O no se encontraron, usar contenido como éxito
                        if not success_indicators or found_indicator or elapsed > 10:
                            # Después de 10s con contenido, asumir éxito
                            logger.info(f"✅ Cloudflare bypasseado exitosamente ({elapsed}s)")
                            return True
                    
            except Exception as e:
                logger.debug(f"Error verificando Cloudflare: {e}")
            
            time.sleep(0.5)  # Verificar cada 0.5s (antes: 1s)
        
        logger.warning(f"⚠ Timeout de {max_wait}s alcanzado (puede que ya esté resuelto)")
        return False
    
    def _authenticate(self, login_url: str) -> bool:
        """
        Método abstracto para autenticación.
        
        Debe ser implementado por cada scraper específico
        según su sitio web (cada sitio tiene formularios diferentes).
        
        Args:
            login_url: URL de la página de login
            
        Returns:
            True si la autenticación fue exitosa
        """
        raise NotImplementedError(
            "Cada scraper debe implementar su propia lógica de autenticación"
        )
    
    def _is_logged_in(self) -> bool:
        """
        Verifica si el usuario está autenticado.
        
        Debe ser implementado por cada scraper específico.
        
        Returns:
            True si está autenticado
        """
        raise NotImplementedError(
            "Cada scraper debe implementar su verificación de login"
        )
    
    def _save_cookies(self, filepath: str = "cookies.pkl"):
        """
        Guarda las cookies de sesión para reutilización.
        
        Útil para mantener sesiones entre ejecuciones.
        """
        import pickle
        
        try:
            cookies = self.driver.get_cookies()
            with open(filepath, 'wb') as f:
                pickle.dump(cookies, f)
            logger.info(f"Cookies guardadas en {filepath}")
        except Exception as e:
            logger.error(f"Error guardando cookies: {e}")
    
    def _load_cookies(self, filepath: str = "cookies.pkl") -> bool:
        """
        Carga cookies guardadas previamente.
        
        Returns:
            True si se cargaron correctamente
        """
        import pickle
        
        try:
            if not Path(filepath).exists():
                return False
            
            with open(filepath, 'rb') as f:
                cookies = pickle.load(f)
            
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            
            logger.info(f"Cookies cargadas desde {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error cargando cookies: {e}")
            return False
