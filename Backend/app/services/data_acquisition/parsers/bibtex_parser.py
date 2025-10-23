"""
BibTeX Parser
=============

Parser para archivos bibliográficos en formato BibTeX (.bib).

BibTeX es el formato estándar para referencias en LaTeX, ampliamente
utilizado en el ámbito académico. Este parser convierte entradas BibTeX
al modelo unificado de Publication.

FORMATO BIBTEX:
@article{key,
  author = {Smith, John and Doe, Jane},
  title = {Sample Article},
  journal = {Journal Name},
  year = {2024},
  volume = {10},
  number = {2},
  pages = {123--145},
  doi = {10.1234/example}
}

COMPLEJIDAD:
- Parsing: O(n) donde n = caracteres del archivo
- Validación: O(m) donde m = número de entradas

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

import re
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from app.models.publication import Publication, Author

logger = logging.getLogger(__name__)


class BibTeXParser:
    """
    Parser para archivos BibTeX.
    
    Soporta todos los tipos de entradas estándar:
    - @article: Artículos de revistas
    - @inproceedings: Conferencias
    - @book: Libros
    - @incollection: Capítulos de libros
    - @phdthesis: Tesis doctorales
    - @mastersthesis: Tesis de maestría
    - @techreport: Reportes técnicos
    - @misc: Otros tipos
    """
    
    # Tipos de entrada válidos en BibTeX
    ENTRY_TYPES = {
        'article', 'inproceedings', 'conference', 'book', 
        'incollection', 'phdthesis', 'mastersthesis', 
        'techreport', 'misc', 'unpublished'
    }
    
    # Mapeo de tipos BibTeX a categorías Publication
    TYPE_MAPPING = {
        'article': 'article',
        'inproceedings': 'conference',
        'conference': 'conference',
        'book': 'book',
        'incollection': 'book_chapter',
        'phdthesis': 'thesis',
        'mastersthesis': 'thesis',
        'techreport': 'report',
        'misc': 'other',
        'unpublished': 'preprint'
    }
    
    def __init__(self):
        """Inicializa el parser BibTeX."""
        self.stats = {
            'total_entries': 0,
            'parsed_successfully': 0,
            'parsing_errors': 0,
            'validation_errors': 0
        }
        logger.info("BibTeXParser inicializado")
    
    def parse_file(self, file_path: str) -> List[Publication]:
        """
        Parsea un archivo BibTeX completo.
        
        Args:
            file_path: Ruta al archivo .bib
        
        Returns:
            Lista de objetos Publication
        
        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el formato es inválido
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        if path.suffix.lower() != '.bib':
            logger.warning(f"Extensión inesperada: {path.suffix}. Se esperaba .bib")
        
        logger.info(f"Parseando archivo BibTeX: {file_path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            publications = self.parse_string(content)
            
            logger.info(
                f"Parseado completo: {self.stats['parsed_successfully']} exitosos, "
                f"{self.stats['parsing_errors']} errores"
            )
            
            return publications
            
        except UnicodeDecodeError:
            # Intentar con encoding alternativo
            logger.warning("UTF-8 falló, intentando con latin-1")
            with open(path, 'r', encoding='latin-1') as f:
                content = f.read()
            return self.parse_string(content)
    
    def parse_string(self, bibtex_string: str) -> List[Publication]:
        """
        Parsea una cadena BibTeX.
        
        Args:
            bibtex_string: Contenido BibTeX como string
        
        Returns:
            Lista de objetos Publication
        """
        publications = []
        
        # Resetear estadísticas
        self.stats = {
            'total_entries': 0,
            'parsed_successfully': 0,
            'parsing_errors': 0,
            'validation_errors': 0
        }
        
        # Extraer todas las entradas BibTeX
        entries = self._extract_entries(bibtex_string)
        
        self.stats['total_entries'] = len(entries)
        logger.debug(f"Encontradas {len(entries)} entradas BibTeX")
        
        for entry_type, citation_key, fields in entries:
            try:
                publication = self._parse_entry(entry_type, citation_key, fields)
                
                if publication:
                    publications.append(publication)
                    self.stats['parsed_successfully'] += 1
                else:
                    self.stats['validation_errors'] += 1
                    
            except Exception as e:
                logger.error(f"Error parseando entrada {citation_key}: {str(e)}")
                self.stats['parsing_errors'] += 1
        
        return publications
    
    def _extract_entries(self, content: str) -> List[tuple]:
        """
        Extrae todas las entradas BibTeX del contenido.
        
        Usa un enfoque más robusto para manejar braces anidados.
        
        Args:
            content: Contenido del archivo BibTeX
        
        Returns:
            Lista de tuplas (tipo, clave, campos)
        """
        entries = []
        
        # Encontrar todas las posiciones de @tipo{
        entry_pattern = r'@(\w+)\s*\{'
        
        for match in re.finditer(entry_pattern, content, re.IGNORECASE):
            entry_type = match.group(1).lower()
            start_pos = match.end()
            
            # Validar tipo de entrada
            if entry_type not in self.ENTRY_TYPES:
                logger.warning(f"Tipo de entrada desconocido: @{entry_type}")
                continue
            
            # Encontrar el cierre correspondiente usando conteo de braces
            brace_count = 1
            pos = start_pos
            
            while pos < len(content) and brace_count > 0:
                if content[pos] == '{':
                    brace_count += 1
                elif content[pos] == '}':
                    brace_count -= 1
                pos += 1
            
            if brace_count == 0:
                # Extraer contenido entre braces
                entry_content = content[start_pos:pos-1]
                
                # Separar citation key del resto
                comma_pos = entry_content.find(',')
                if comma_pos > 0:
                    citation_key = entry_content[:comma_pos].strip()
                    fields_str = entry_content[comma_pos+1:].strip()
                    
                    # Parsear campos
                    fields = self._parse_fields(fields_str)
                    
                    entries.append((entry_type, citation_key, fields))
        
        return entries
    
    def _parse_fields(self, fields_str: str) -> Dict[str, str]:
        """
        Parsea los campos de una entrada BibTeX.
        
        Formato: key = {value} o key = "value"
        
        Args:
            fields_str: String con los campos
        
        Returns:
            Diccionario con campos parseados
        """
        fields = {}
        
        # Patrón para capturar campo = valor
        # Soporta tanto {valor} como "valor"
        pattern = r'(\w+)\s*=\s*(?:\{([^}]*)\}|"([^"]*)")'
        
        matches = re.finditer(pattern, fields_str, re.MULTILINE)
        
        for match in matches:
            key = match.group(1).lower()
            # El valor puede estar en grupo 2 ({}) o grupo 3 ("")
            value = match.group(2) if match.group(2) else match.group(3)
            
            if value:
                # Limpiar valor
                value = value.strip()
                # Reemplazar dobles espacios
                value = re.sub(r'\s+', ' ', value)
                # Eliminar saltos de línea
                value = value.replace('\n', ' ')
                
                fields[key] = value
        
        return fields
    
    def _parse_entry(
        self, 
        entry_type: str, 
        citation_key: str, 
        fields: Dict[str, str]
    ) -> Optional[Publication]:
        """
        Convierte una entrada BibTeX en un objeto Publication.
        
        Args:
            entry_type: Tipo de entrada (@article, @inproceedings, etc.)
            citation_key: Clave de citación
            fields: Diccionario con campos
        
        Returns:
            Objeto Publication o None si falla la validación
        """
        try:
            # Extraer autores como objetos Author
            author_names = self._parse_authors(fields.get('author', ''))
            authors = [Author(name=name) for name in author_names] if author_names else []
            
            # Extraer año
            year = self._parse_year(fields.get('year', ''))
            
            # Mapear tipo
            pub_type = self.TYPE_MAPPING.get(entry_type, 'other')
            
            # Abstract (puede estar vacío)
            abstract = fields.get('abstract', '')
            if not abstract:
                abstract = 'No abstract available'
            
            # DOI (opcional)
            doi = fields.get('doi', '')
            
            # Crear objeto Publication
            publication = Publication(
                title=fields.get('title', 'Untitled'),
                authors=authors,
                publication_year=year,
                abstract=abstract,
                keywords=self._parse_keywords(fields.get('keywords', '')),
                doi=doi if doi else None,
                url=fields.get('url', ''),
                source='crossref',  # Usar crossref como fuente genérica
                publication_type=pub_type,
                journal=self._extract_venue(entry_type, fields),
                volume=fields.get('volume'),
                issue=fields.get('number'),
                pages=fields.get('pages'),
                publisher=fields.get('publisher'),
                isbn=fields.get('isbn'),
                issn=fields.get('issn'),
                metadata={
                    'citation_key': citation_key,
                    'entry_type': entry_type,
                    'bibtex_fields': fields,
                    'original_source': 'bibtex'
                }
            )
            
            logger.debug(f"Entrada parseada: {citation_key}")
            return publication
            
        except Exception as e:
            logger.error(f"Error creando Publication para {citation_key}: {str(e)}")
            return None
    
    def _parse_authors(self, author_string: str) -> List[str]:
        """
        Parsea la cadena de autores de BibTeX.
        
        BibTeX usa "and" como separador: "Smith, John and Doe, Jane"
        
        Args:
            author_string: Cadena de autores
        
        Returns:
            Lista de autores formateados
        """
        if not author_string:
            return []
        
        # Separar por "and"
        authors = [a.strip() for a in author_string.split(' and ')]
        
        # Formatear cada autor
        formatted = []
        for author in authors:
            if ',' in author:
                # Formato "Apellido, Nombre" -> "Nombre Apellido"
                parts = author.split(',', 1)
                formatted.append(f"{parts[1].strip()} {parts[0].strip()}")
            else:
                formatted.append(author)
        
        return formatted
    
    def _parse_year(self, year_string: str) -> Optional[int]:
        """
        Extrae el año de la cadena.
        
        Args:
            year_string: Cadena con año
        
        Returns:
            Año como entero o None
        """
        if not year_string:
            return None
        
        # Buscar 4 dígitos consecutivos
        match = re.search(r'\d{4}', year_string)
        if match:
            return int(match.group())
        
        return None
    
    def _parse_keywords(self, keywords_string: str) -> List[str]:
        """
        Parsea palabras clave.
        
        Soporta separadores: coma, punto y coma, "and"
        
        Args:
            keywords_string: Cadena con keywords
        
        Returns:
            Lista de keywords
        """
        if not keywords_string:
            return []
        
        # Reemplazar separadores comunes
        keywords_string = keywords_string.replace(';', ',')
        keywords_string = keywords_string.replace(' and ', ',')
        
        # Separar y limpiar
        keywords = [k.strip() for k in keywords_string.split(',')]
        
        return [k for k in keywords if k]  # Filtrar vacíos
    
    def _extract_venue(self, entry_type: str, fields: Dict[str, str]) -> Optional[str]:
        """
        Extrae el venue (revista, conferencia, etc.) según el tipo.
        
        Args:
            entry_type: Tipo de entrada BibTeX
            fields: Campos de la entrada
        
        Returns:
            Nombre del venue
        """
        if entry_type == 'article':
            return fields.get('journal')
        elif entry_type in ('inproceedings', 'conference'):
            return fields.get('booktitle')
        elif entry_type == 'book':
            return fields.get('publisher')
        elif entry_type == 'incollection':
            return fields.get('booktitle')
        
        return None
    
    def get_stats(self) -> Dict[str, int]:
        """
        Retorna estadísticas del parsing.
        
        Returns:
            Diccionario con estadísticas
        """
        return self.stats.copy()
