"""
CSV Parser
==========

Parser para archivos bibliográficos en formato CSV (.csv).

CSV (Comma-Separated Values) es un formato tabular común para exportar
datos bibliográficos de herramientas como Excel, Google Sheets, etc.

FORMATO ESPERADO:
title,authors,year,abstract,keywords,doi,url,venue,volume,issue,pages
"Title","Author1; Author2",2024,"Abstract text","kw1; kw2","10.1234/ex","http://...","Journal",10,2,"123-145"

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

import csv
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from io import StringIO

from app.models.publication import Publication, Author

logger = logging.getLogger(__name__)


class CSVParser:
    """Parser para archivos CSV con metadatos bibliográficos."""
    
    # Mapeo de columnas comunes a campos Publication
    COLUMN_MAPPING = {
        'title': 'title',
        'authors': 'authors',
        'author': 'authors',
        'year': 'year',
        'publication_year': 'year',
        'abstract': 'abstract',
        'keywords': 'keywords',
        'doi': 'doi',
        'url': 'url',
        'link': 'url',
        'venue': 'venue',
        'journal': 'venue',
        'conference': 'venue',
        'volume': 'volume',
        'issue': 'issue',
        'number': 'issue',
        'pages': 'pages',
        'publisher': 'publisher',
        'issn': 'issn',
        'isbn': 'isbn',
        'type': 'publication_type',
        'publication_type': 'publication_type'
    }
    
    def __init__(self):
        """Inicializa el parser CSV."""
        self.stats = {
            'total_rows': 0,
            'parsed_successfully': 0,
            'parsing_errors': 0,
            'validation_errors': 0
        }
        logger.info("CSVParser inicializado")
    
    def parse_file(
        self, 
        file_path: str,
        delimiter: str = ',',
        encoding: str = 'utf-8'
    ) -> List[Publication]:
        """
        Parsea un archivo CSV.
        
        Args:
            file_path: Ruta al archivo CSV
            delimiter: Delimitador usado (por defecto: coma)
            encoding: Encoding del archivo
        
        Returns:
            Lista de objetos Publication
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        logger.info(f"Parseando archivo CSV: {file_path}")
        
        try:
            with open(path, 'r', encoding=encoding) as f:
                content = f.read()
            
            return self.parse_string(content, delimiter=delimiter)
            
        except UnicodeDecodeError:
            logger.warning(f"{encoding} falló, intentando con latin-1")
            with open(path, 'r', encoding='latin-1') as f:
                content = f.read()
            return self.parse_string(content, delimiter=delimiter)
    
    def parse_string(self, csv_string: str, delimiter: str = ',') -> List[Publication]:
        """
        Parsea una cadena CSV.
        
        Args:
            csv_string: Contenido CSV como string
            delimiter: Delimitador
        
        Returns:
            Lista de objetos Publication
        """
        publications = []
        
        # Resetear stats
        self.stats = {
            'total_rows': 0,
            'parsed_successfully': 0,
            'parsing_errors': 0,
            'validation_errors': 0
        }
        
        try:
            # Parsear CSV
            reader = csv.DictReader(StringIO(csv_string), delimiter=delimiter)
            
            for row_num, row in enumerate(reader, start=2):  # start=2 (header=1)
                self.stats['total_rows'] += 1
                
                try:
                    publication = self._parse_row(row)
                    
                    if publication:
                        publications.append(publication)
                        self.stats['parsed_successfully'] += 1
                    else:
                        self.stats['validation_errors'] += 1
                        
                except Exception as e:
                    logger.error(f"Error parseando fila {row_num}: {str(e)}")
                    self.stats['parsing_errors'] += 1
            
            logger.info(
                f"CSV parseado: {self.stats['parsed_successfully']} exitosos, "
                f"{self.stats['parsing_errors']} errores"
            )
            
            return publications
            
        except Exception as e:
            logger.error(f"Error parseando CSV: {str(e)}")
            raise
    
    def _parse_row(self, row: Dict[str, str]) -> Optional[Publication]:
        """
        Convierte una fila CSV en Publication.
        
        Args:
            row: Diccionario con datos de la fila
        
        Returns:
            Objeto Publication o None
        """
        try:
            # Normalizar nombres de columnas
            normalized_row = self._normalize_columns(row)
            
            # Extraer campos
            title = normalized_row.get('title', '')
            if not title:
                logger.warning("Fila sin título, saltando")
                return None
            
            # Parsear autores como objetos Author
            authors_str = normalized_row.get('authors', '')
            author_names = self._parse_authors(authors_str)
            authors = [Author(name=name) for name in author_names] if author_names else []
            
            # Parsear año
            year = self._parse_year(normalized_row.get('year', ''))
            
            # Parsear keywords
            keywords_str = normalized_row.get('keywords', '')
            keywords = self._parse_keywords(keywords_str)
            
            # Extraer abstract
            abstract = normalized_row.get('abstract', '')
            if not abstract:
                abstract = 'No abstract available'
            
            # Extraer DOI (opcional)
            doi = normalized_row.get('doi', '')
            
            # Crear Publication
            publication = Publication(
                title=title,
                authors=authors,
                publication_year=year,
                abstract=abstract,
                keywords=keywords,
                doi=doi if doi else None,
                url=normalized_row.get('url', ''),
                source='crossref',  # Usar crossref como fuente genérica
                publication_type=normalized_row.get('publication_type', 'article'),
                journal=normalized_row.get('venue'),
                volume=normalized_row.get('volume'),
                issue=normalized_row.get('issue'),
                pages=normalized_row.get('pages'),
                publisher=normalized_row.get('publisher'),
                issn=normalized_row.get('issn'),
                isbn=normalized_row.get('isbn'),
                metadata={
                    'csv_row': row,
                    'original_source': 'csv'
                }
            )
            
            return publication
            
        except Exception as e:
            logger.error(f"Error creando Publication desde CSV: {str(e)}")
            return None
    
    def _normalize_columns(self, row: Dict[str, str]) -> Dict[str, str]:
        """
        Normaliza nombres de columnas usando el mapeo.
        
        Args:
            row: Fila original
        
        Returns:
            Fila con columnas normalizadas
        """
        normalized = {}
        
        for col_name, value in row.items():
            # Normalizar nombre de columna
            col_lower = col_name.lower().strip()
            normalized_name = self.COLUMN_MAPPING.get(col_lower, col_lower)
            
            normalized[normalized_name] = value.strip() if value else ''
        
        return normalized
    
    def _parse_authors(self, authors_str: str) -> List[str]:
        """
        Parsea string de autores.
        
        Soporta separadores: ; | and ,
        
        Args:
            authors_str: String con autores
        
        Returns:
            Lista de autores
        """
        if not authors_str:
            return []
        
        # Probar diferentes separadores
        separators = [';', '|', ' and ', ',']
        
        for sep in separators:
            if sep in authors_str:
                authors = [a.strip() for a in authors_str.split(sep)]
                return [a for a in authors if a]
        
        # Si no hay separadores, retornar como único autor
        return [authors_str.strip()] if authors_str.strip() else []
    
    def _parse_year(self, year_str: str) -> Optional[int]:
        """Extrae año del string."""
        if not year_str:
            return None
        
        try:
            # Intentar conversión directa
            year = int(year_str)
            if 1900 <= year <= 2100:
                return year
        except ValueError:
            pass
        
        # Buscar 4 dígitos
        import re
        match = re.search(r'\d{4}', year_str)
        if match:
            return int(match.group())
        
        return None
    
    def _parse_keywords(self, keywords_str: str) -> List[str]:
        """
        Parsea keywords.
        
        Args:
            keywords_str: String con keywords
        
        Returns:
            Lista de keywords
        """
        if not keywords_str:
            return []
        
        # Probar separadores
        for sep in [';', '|', ',']:
            if sep in keywords_str:
                kws = [k.strip() for k in keywords_str.split(sep)]
                return [k for k in kws if k]
        
        return [keywords_str.strip()] if keywords_str.strip() else []
    
    def get_stats(self) -> Dict[str, int]:
        """Retorna estadísticas del parsing."""
        return self.stats.copy()
