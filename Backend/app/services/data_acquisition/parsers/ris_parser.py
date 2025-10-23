"""
RIS Parser
==========

Parser para archivos bibliográficos en formato RIS (.ris).

RIS (Research Information Systems) es un formato estandarizado para
intercambio de referencias bibliográficas. Usado por EndNote, Mendeley,
Zotero y muchas bases de datos académicas.

FORMATO RIS:
TY  - JOUR
AU  - Smith, John
AU  - Doe, Jane
TI  - Sample Article
JO  - Journal Name
PY  - 2024
VL  - 10
IS  - 2
SP  - 123
EP  - 145
DO  - 10.1234/example
ER  -

TAGS PRINCIPALES:
- TY: Tipo de referencia
- AU: Autor
- TI: Título
- JO: Journal (revista)
- PY: Año de publicación
- AB: Abstract
- KW: Keywords
- DO: DOI
- UR: URL
- ER: End of Reference

COMPLEJIDAD:
- Parsing: O(n) donde n = líneas del archivo
- Por entrada: O(m) donde m = campos de la entrada

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

import re
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from app.models.publication import Publication, Author

logger = logging.getLogger(__name__)


class RISParser:
    """
    Parser para archivos RIS.
    
    Soporta todos los tipos de referencia RIS estándar según
    la especificación de RefMan.
    """
    
    # Mapeo de tipos RIS a categorías Publication
    TYPE_MAPPING = {
        'JOUR': 'article',          # Journal article
        'CONF': 'conference',       # Conference proceeding
        'BOOK': 'book',             # Book
        'CHAP': 'book_chapter',     # Book chapter
        'THES': 'thesis',           # Thesis
        'RPRT': 'report',           # Report
        'UNPB': 'preprint',         # Unpublished work
        'ELEC': 'web',             # Electronic source
        'GEN': 'other',            # Generic
        'ABST': 'abstract',        # Abstract
        'INPR': 'preprint',        # In press
        'JFULL': 'article',        # Journal (full)
        'MGZN': 'magazine',        # Magazine article
        'NEWS': 'news',            # Newspaper
        'PAMP': 'pamphlet',        # Pamphlet
        'PAT': 'patent',           # Patent
        'PCOMM': 'personal_communication',  # Personal communication
        'SLIDE': 'presentation',   # Slide
        'SOUND': 'multimedia',     # Sound recording
        'STAT': 'statute',         # Statute
        'UNBILL': 'bill',          # Unenacted bill
        'VIDEO': 'multimedia',     # Video recording
    }
    
    # Tags RIS y su significado
    RIS_TAGS = {
        'TY': 'type',
        'AU': 'author',
        'A1': 'author',         # Primary author
        'A2': 'secondary_author',
        'A3': 'tertiary_author',
        'TI': 'title',
        'T1': 'title',          # Primary title
        'T2': 'secondary_title',
        'AB': 'abstract',
        'KW': 'keyword',
        'PY': 'year',
        'Y1': 'year',           # Primary date
        'JO': 'journal',        # Journal name (abbreviated)
        'JF': 'journal_full',   # Journal name (full)
        'JA': 'journal_abbr',   # Journal abbreviation
        'VL': 'volume',
        'IS': 'issue',
        'SP': 'start_page',
        'EP': 'end_page',
        'DO': 'doi',
        'UR': 'url',
        'L1': 'file_url',       # Link to PDF
        'L2': 'related_url',
        'PB': 'publisher',
        'CY': 'place',          # Place of publication
        'SN': 'issn_isbn',
        'M3': 'type_of_work',
        'N1': 'notes',
        'N2': 'abstract_alt',   # Abstract alternativo
        'ER': 'end_of_record',
    }
    
    def __init__(self):
        """Inicializa el parser RIS."""
        self.stats = {
            'total_entries': 0,
            'parsed_successfully': 0,
            'parsing_errors': 0,
            'validation_errors': 0
        }
        logger.info("RISParser inicializado")
    
    def parse_file(self, file_path: str) -> List[Publication]:
        """
        Parsea un archivo RIS completo.
        
        Args:
            file_path: Ruta al archivo .ris
        
        Returns:
            Lista de objetos Publication
        
        Raises:
            FileNotFoundError: Si el archivo no existe
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        if path.suffix.lower() != '.ris':
            logger.warning(f"Extensión inesperada: {path.suffix}. Se esperaba .ris")
        
        logger.info(f"Parseando archivo RIS: {file_path}")
        
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
            logger.warning("UTF-8 falló, intentando con latin-1")
            with open(path, 'r', encoding='latin-1') as f:
                content = f.read()
            return self.parse_string(content)
    
    def parse_string(self, ris_string: str) -> List[Publication]:
        """
        Parsea una cadena RIS.
        
        Args:
            ris_string: Contenido RIS como string
        
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
        
        # Dividir en entradas individuales
        entries = self._split_entries(ris_string)
        
        self.stats['total_entries'] = len(entries)
        logger.debug(f"Encontradas {len(entries)} entradas RIS")
        
        for entry_lines in entries:
            try:
                publication = self._parse_entry(entry_lines)
                
                if publication:
                    publications.append(publication)
                    self.stats['parsed_successfully'] += 1
                else:
                    self.stats['validation_errors'] += 1
                    
            except Exception as e:
                logger.error(f"Error parseando entrada RIS: {str(e)}")
                self.stats['parsing_errors'] += 1
        
        return publications
    
    def _split_entries(self, content: str) -> List[List[str]]:
        """
        Divide el contenido en entradas individuales.
        
        Cada entrada comienza con "TY  -" y termina con "ER  -"
        
        Args:
            content: Contenido completo del archivo RIS
        
        Returns:
            Lista de listas de líneas (una por entrada)
        """
        entries = []
        current_entry = []
        in_entry = False
        
        for line in content.split('\n'):
            line = line.rstrip()
            
            if not line:
                continue
            
            # Detectar inicio de entrada
            if line.startswith('TY  -'):
                if current_entry:
                    # Guardar entrada anterior
                    entries.append(current_entry)
                current_entry = [line]
                in_entry = True
            
            # Detectar fin de entrada
            elif line.startswith('ER  -'):
                if current_entry:
                    current_entry.append(line)
                    entries.append(current_entry)
                    current_entry = []
                in_entry = False
            
            # Línea de contenido
            elif in_entry:
                current_entry.append(line)
        
        # Agregar última entrada si existe
        if current_entry:
            entries.append(current_entry)
        
        return entries
    
    def _parse_entry(self, lines: List[str]) -> Optional[Publication]:
        """
        Parsea una entrada RIS individual.
        
        Args:
            lines: Lista de líneas de la entrada
        
        Returns:
            Objeto Publication o None
        """
        fields = {}
        current_tag = None
        current_value = []
        
        for line in lines:
            # Parsear línea: "TAG - VALUE"
            match = re.match(r'^([A-Z][A-Z0-9])\s+-\s*(.*)$', line)
            
            if match:
                # Guardar valor anterior si existe
                if current_tag and current_value:
                    self._add_field(fields, current_tag, ' '.join(current_value))
                
                # Nueva tag
                current_tag = match.group(1)
                current_value = [match.group(2)] if match.group(2) else []
            
            else:
                # Continuación de valor en múltiples líneas
                if current_tag and line.strip():
                    current_value.append(line.strip())
        
        # Guardar último valor
        if current_tag and current_value:
            self._add_field(fields, current_tag, ' '.join(current_value))
        
        # Convertir a Publication
        return self._fields_to_publication(fields)
    
    def _add_field(self, fields: Dict[str, Any], tag: str, value: str):
        """
        Agrega un campo al diccionario de campos.
        
        Maneja campos múltiples (como autores, keywords).
        
        Args:
            fields: Diccionario de campos
            tag: Tag RIS
            value: Valor del campo
        """
        field_name = self.RIS_TAGS.get(tag, f'unknown_{tag}')
        
        # Campos que pueden aparecer múltiples veces
        multi_fields = ['author', 'keyword']
        
        if field_name in multi_fields:
            if field_name not in fields:
                fields[field_name] = []
            fields[field_name].append(value)
        else:
            fields[field_name] = value
    
    def _fields_to_publication(self, fields: Dict[str, Any]) -> Optional[Publication]:
        """
        Convierte campos RIS en objeto Publication.
        
        Args:
            fields: Diccionario con campos parseados
        
        Returns:
            Objeto Publication o None
        """
        try:
            # Determinar tipo
            ris_type = fields.get('type', 'GEN')
            pub_type = self.TYPE_MAPPING.get(ris_type, 'other')
            
            # Extraer autores como objetos Author
            author_names = fields.get('author', [])
            if isinstance(author_names, str):
                author_names = [author_names]
            authors = [Author(name=name) for name in author_names] if author_names else []
            
            # Extraer año
            year = self._parse_year(fields.get('year', ''))
            
            # Determinar journal/venue
            venue = (
                fields.get('journal_full') or 
                fields.get('journal') or 
                fields.get('secondary_title')
            )
            
            # Extraer abstract
            abstract = (
                fields.get('abstract') or 
                fields.get('abstract_alt', '')
            )
            if not abstract:
                abstract = 'No abstract available'
            
            # Extraer keywords
            keywords = fields.get('keyword', [])
            if isinstance(keywords, str):
                keywords = [keywords]
            
            # Páginas
            pages = self._format_pages(
                fields.get('start_page'),
                fields.get('end_page')
            )
            
            # DOI (opcional)
            doi = fields.get('doi', '')
            
            # Crear Publication
            publication = Publication(
                title=fields.get('title', 'Untitled'),
                authors=authors,
                publication_year=year,
                abstract=abstract,
                keywords=keywords,
                doi=doi if doi else None,
                url=fields.get('url', ''),
                source='crossref',  # Usar crossref como fuente genérica
                publication_type=pub_type,
                journal=venue,
                volume=fields.get('volume'),
                issue=fields.get('issue'),
                pages=pages,
                publisher=fields.get('publisher'),
                issn=fields.get('issn_isbn'),
                metadata={
                    'ris_type': ris_type,
                    'ris_fields': fields,
                    'notes': fields.get('notes'),
                    'original_source': 'ris'
                }
            )
            
            logger.debug(f"Entrada RIS parseada: {publication.title[:50]}")
            return publication
            
        except Exception as e:
            logger.error(f"Error creando Publication desde RIS: {str(e)}")
            return None
    
    def _parse_year(self, year_string: str) -> Optional[int]:
        """
        Extrae año de la cadena.
        
        RIS puede tener formatos como "2024", "2024/01/15", "2024////"
        
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
    
    def _format_pages(
        self, 
        start_page: Optional[str], 
        end_page: Optional[str]
    ) -> Optional[str]:
        """
        Formatea las páginas en formato "inicio-fin".
        
        Args:
            start_page: Página inicial
            end_page: Página final
        
        Returns:
            String formateado o None
        """
        if start_page and end_page:
            return f"{start_page}-{end_page}"
        elif start_page:
            return start_page
        
        return None
    
    def get_stats(self) -> Dict[str, int]:
        """
        Retorna estadísticas del parsing.
        
        Returns:
            Diccionario con estadísticas
        """
        return self.stats.copy()
