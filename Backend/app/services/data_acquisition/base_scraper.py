"""
Scraper Base Abstracto
======================

Clase base abstracta que define la interfaz común para todos los scrapers
de bases de datos científicas.

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Course: Análisis de Algoritmos (2025-2), Universidad del Quindío
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from enum import Enum
import logging

from app.models.publication import Publication

logger = logging.getLogger(__name__)


class ExportFormat(str, Enum):
    """Formatos de exportación soportados."""
    JSON = "json"
    BIBTEX = "bibtex"
    RIS = "ris"
    CSV = "csv"


class ScraperStatus(str, Enum):
    """Estados posibles del scraper."""
    IDLE = "idle"
    SEARCHING = "searching"
    DOWNLOADING = "downloading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


class BaseScraper(ABC):
    """
    Clase base abstracta para scrapers de bases de datos científicas.
    
    Todos los scrapers específicos (ACM, SAGE, ScienceDirect) deben heredar
    de esta clase e implementar los métodos abstractos.
    
    Atributos:
        source_name: Nombre de la fuente de datos
        base_url: URL base de la fuente
        status: Estado actual del scraper
        total_results: Total de resultados encontrados
        downloaded_count: Cantidad de publicaciones descargadas
    """
    
    def __init__(
        self,
        source_name: str,
        base_url: str,
        api_key: Optional[str] = None,
        rate_limit: float = 1.0,
        timeout: int = 30
    ):
        """
        Inicializa el scraper base.
        
        Args:
            source_name: Nombre identificador de la fuente
            base_url: URL base de la API o sitio web
            api_key: Clave de API si es requerida
            rate_limit: Límite de peticiones por segundo
            timeout: Tiempo máximo de espera por petición (segundos)
        """
        self.source_name = source_name
        self.base_url = base_url
        self.api_key = api_key
        self.rate_limit = rate_limit
        self.timeout = timeout
        
        self.status = ScraperStatus.IDLE
        self.total_results = 0
        self.downloaded_count = 0
        self.errors: List[str] = []
        
        logger.info(f"Scraper inicializado para: {source_name}")
    
    @abstractmethod
    async def search(
        self,
        query: str,
        max_results: int = 100,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        publication_type: Optional[str] = None
    ) -> List[Publication]:
        """
        Busca publicaciones en la base de datos.
        
        Args:
            query: Cadena de búsqueda
            max_results: Número máximo de resultados a retornar
            start_year: Año de inicio para filtrar resultados
            end_year: Año final para filtrar resultados
            publication_type: Tipo de publicación (article, conference, etc.)
        
        Returns:
            Lista de publicaciones encontradas
        """
        pass
    
    @abstractmethod
    async def download_metadata(
        self,
        publication_id: str
    ) -> Optional[Publication]:
        """
        Descarga metadatos completos de una publicación específica.
        
        Args:
            publication_id: Identificador único de la publicación en la fuente
        
        Returns:
            Objeto Publication con metadatos completos o None si falla
        """
        pass
    
    @abstractmethod
    def parse_publication(
        self,
        raw_data: Dict[str, Any]
    ) -> Optional[Publication]:
        """
        Parsea datos crudos de la fuente a objeto Publication.
        
        Args:
            raw_data: Diccionario con datos crudos de la fuente
        
        Returns:
            Objeto Publication parseado o None si falla
        """
        pass
    
    @abstractmethod
    async def download_file(
        self,
        publication: Publication,
        file_format: str = "pdf"
    ) -> Optional[str]:
        """
        Descarga el archivo completo de una publicación (PDF, etc.).
        
        Args:
            publication: Publicación de la cual descargar el archivo
            file_format: Formato del archivo a descargar
        
        Returns:
            Ruta al archivo descargado o None si falla
        """
        pass
    
    def export_to_format(
        self,
        publications: List[Publication],
        format: ExportFormat
    ) -> str:
        """
        Exporta publicaciones al formato especificado.
        
        Args:
            publications: Lista de publicaciones a exportar
            format: Formato de exportación deseado
        
        Returns:
            String con datos exportados en el formato especificado
        """
        if format == ExportFormat.JSON:
            return self._export_to_json(publications)
        elif format == ExportFormat.BIBTEX:
            return self._export_to_bibtex(publications)
        elif format == ExportFormat.RIS:
            return self._export_to_ris(publications)
        elif format == ExportFormat.CSV:
            return self._export_to_csv(publications)
        else:
            raise ValueError(f"Formato no soportado: {format}")
    
    def _export_to_json(self, publications: List[Publication]) -> str:
        """Exporta a formato JSON."""
        import json
        
        data = [pub.model_dump() for pub in publications]
        return json.dumps(data, indent=2, ensure_ascii=False, default=str)
    
    def _export_to_bibtex(self, publications: List[Publication]) -> str:
        """Exporta a formato BibTeX."""
        bibtex_entries = []
        
        for pub in publications:
            bibtex_entries.append(pub.to_bibtex())
        
        return "\n\n".join(bibtex_entries)
    
    def _export_to_ris(self, publications: List[Publication]) -> str:
        """Exporta a formato RIS."""
        ris_entries = []
        
        for pub in publications:
            entry = []
            
            # Tipo de publicación
            entry.append("TY  - JOUR" if pub.publication_type == "article" else "TY  - CONF")
            
            # Título
            entry.append(f"TI  - {pub.title}")
            
            # Autores
            for author in pub.authors:
                entry.append(f"AU  - {author.name}")
            
            # Año
            if pub.publication_year:
                entry.append(f"PY  - {pub.publication_year}")
            
            # Revista
            if pub.journal:
                entry.append(f"JO  - {pub.journal}")
            
            # DOI
            if pub.doi:
                entry.append(f"DO  - {pub.doi}")
            
            # URL
            if pub.url:
                entry.append(f"UR  - {pub.url}")
            
            # Abstract
            if pub.abstract:
                entry.append(f"AB  - {pub.abstract}")
            
            # Keywords
            for keyword in pub.keywords:
                entry.append(f"KW  - {keyword}")
            
            entry.append("ER  - ")
            
            ris_entries.append("\n".join(entry))
        
        return "\n\n".join(ris_entries)
    
    def _export_to_csv(self, publications: List[Publication]) -> str:
        """Exporta a formato CSV."""
        import csv
        from io import StringIO
        
        output = StringIO()
        
        # Definir columnas
        fieldnames = [
            'id', 'title', 'abstract', 'authors', 'keywords', 'doi',
            'publication_year', 'journal', 'source', 'url', 'citation_count'
        ]
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for pub in publications:
            writer.writerow({
                'id': pub.id or pub.generate_id(),
                'title': pub.title,
                'abstract': pub.abstract[:500] + '...' if len(pub.abstract) > 500 else pub.abstract,
                'authors': '; '.join(pub.get_author_names()),
                'keywords': '; '.join(pub.keywords),
                'doi': pub.doi or '',
                'publication_year': pub.publication_year or '',
                'journal': pub.journal or '',
                'source': pub.source,
                'url': pub.url or '',
                'citation_count': pub.citation_count
            })
        
        return output.getvalue()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado actual del scraper.
        
        Returns:
            Diccionario con información de estado
        """
        return {
            'source': self.source_name,
            'status': self.status.value,
            'total_results': self.total_results,
            'downloaded_count': self.downloaded_count,
            'errors': self.errors,
            'success_rate': f"{(self.downloaded_count / self.total_results * 100):.2f}%" if self.total_results > 0 else "0%"
        }
    
    def reset(self):
        """Reinicia el estado del scraper."""
        self.status = ScraperStatus.IDLE
        self.total_results = 0
        self.downloaded_count = 0
        self.errors = []
        logger.info(f"Scraper {self.source_name} reiniciado")
    
    async def validate_connection(self) -> bool:
        """
        Valida que la conexión con la fuente esté funcionando.
        
        Returns:
            True si la conexión es válida
        """
        try:
            # Realizar una búsqueda de prueba con 1 resultado
            results = await self.search("test", max_results=1)
            return True
        except Exception as e:
            logger.error(f"Error validando conexión con {self.source_name}: {e}")
            return False
    
    def _sanitize_text(self, text: Optional[str]) -> str:
        """
        Limpia y sanitiza texto.
        
        Args:
            text: Texto a limpiar
        
        Returns:
            Texto limpio
        """
        if not text:
            return ""
        
        # Eliminar espacios extras
        text = " ".join(text.split())
        
        # Eliminar caracteres de control
        text = "".join(char for char in text if ord(char) >= 32 or char == '\n')
        
        return text.strip()
    
    def _extract_year(self, date_str: Optional[str]) -> Optional[int]:
        """
        Extrae el año de una cadena de fecha.
        
        Args:
            date_str: Cadena con fecha en cualquier formato
        
        Returns:
            Año como entero o None
        """
        if not date_str:
            return None
        
        import re
        
        # Buscar patrón de 4 dígitos que represente un año
        match = re.search(r'\b(19\d{2}|20\d{2})\b', str(date_str))
        
        if match:
            return int(match.group(1))
        
        return None
    
    def __repr__(self) -> str:
        """Representación del scraper."""
        return f"<{self.__class__.__name__}(source='{self.source_name}', status='{self.status.value}')>"
