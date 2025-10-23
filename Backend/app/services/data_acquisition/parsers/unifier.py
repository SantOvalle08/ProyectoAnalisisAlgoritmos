"""
Publication Unifier
==================

Módulo unificador que detecta automáticamente el formato de archivo
bibliográfico y aplica el parser correspondiente.

Soporta:
- BibTeX (.bib)
- RIS (.ris)
- CSV (.csv)
- JSON (.json)

Convierte todos los formatos al modelo unificado Publication.

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

import json
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from app.models.publication import Publication, Author
from .bibtex_parser import BibTeXParser
from .ris_parser import RISParser
from .csv_parser import CSVParser

logger = logging.getLogger(__name__)


class PublicationUnifier:
    """
    Unificador de formatos bibliográficos.
    
    Detecta automáticamente el formato y parsea a Publication.
    """
    
    def __init__(self):
        """Inicializa el unificador con todos los parsers."""
        self.parsers = {
            '.bib': BibTeXParser(),
            '.ris': RISParser(),
            '.csv': CSVParser()
        }
        
        self.stats = {
            'files_processed': 0,
            'total_publications': 0,
            'errors': 0
        }
        
        logger.info("PublicationUnifier inicializado")
    
    def parse_file(self, file_path: str) -> List[Publication]:
        """
        Parsea un archivo bibliográfico.
        
        Detecta automáticamente el formato por extensión.
        
        Args:
            file_path: Ruta al archivo
        
        Returns:
            Lista de objetos Publication
        
        Raises:
            ValueError: Si el formato no es soportado
            FileNotFoundError: Si el archivo no existe
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        # Detectar formato
        ext = path.suffix.lower()
        
        logger.info(f"Unificando archivo: {file_path} (formato: {ext})")
        
        try:
            # JSON se maneja directamente
            if ext == '.json':
                return self._parse_json_file(path)
            
            # Usar parser específico
            parser = self.parsers.get(ext)
            
            if not parser:
                raise ValueError(
                    f"Formato no soportado: {ext}. "
                    f"Formatos válidos: {list(self.parsers.keys()) + ['.json']}"
                )
            
            publications = parser.parse_file(str(path))
            
            self.stats['files_processed'] += 1
            self.stats['total_publications'] += len(publications)
            
            logger.info(f"Parseado exitoso: {len(publications)} publicaciones")
            
            return publications
            
        except Exception as e:
            self.stats['errors'] += 1
            logger.error(f"Error parseando {file_path}: {str(e)}")
            raise
    
    def parse_multiple_files(self, file_paths: List[str]) -> List[Publication]:
        """
        Parsea múltiples archivos y combina resultados.
        
        Args:
            file_paths: Lista de rutas a archivos
        
        Returns:
            Lista combinada de publicaciones
        """
        all_publications = []
        
        for file_path in file_paths:
            try:
                pubs = self.parse_file(file_path)
                all_publications.extend(pubs)
            except Exception as e:
                logger.error(f"Error con {file_path}: {str(e)}")
                continue
        
        logger.info(
            f"Procesados {len(file_paths)} archivos, "
            f"total: {len(all_publications)} publicaciones"
        )
        
        return all_publications
    
    def _parse_json_file(self, path: Path) -> List[Publication]:
        """
        Parsea archivo JSON con lista de publicaciones.
        
        Asume que el JSON es un array de objetos Publication
        o tiene estructura {'publications': [...]}
        
        Args:
            path: Path del archivo JSON
        
        Returns:
            Lista de Publications
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Si es un diccionario con key 'publications'
            if isinstance(data, dict) and 'publications' in data:
                data = data['publications']
            
            # Si no es lista, convertir a lista
            if not isinstance(data, list):
                data = [data]
            
            publications = []
            
            for item in data:
                try:
                    # Normalizar authors si son strings
                    if 'authors' in item and isinstance(item['authors'], list):
                        if item['authors'] and isinstance(item['authors'][0], str):
                            item['authors'] = [Author(name=name) for name in item['authors']]
                    
                    # Asegurar abstract no vacío
                    if 'abstract' in item and not item['abstract']:
                        item['abstract'] = 'No abstract available'
                    
                    # Convertir DOI vacío a None
                    if 'doi' in item and not item['doi']:
                        item['doi'] = None
                    
                    # Intentar crear Publication directamente
                    pub = Publication(**item)
                    publications.append(pub)
                except Exception as e:
                    logger.warning(f"Error creando Publication desde JSON: {str(e)}")
                    continue
            
            logger.info(f"JSON parseado: {len(publications)} publicaciones")
            
            return publications
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parseando JSON: {str(e)}")
            raise ValueError(f"JSON inválido: {str(e)}")
    
    def export_to_json(
        self, 
        publications: List[Publication], 
        output_path: str,
        indent: int = 2
    ) -> None:
        """
        Exporta publicaciones a JSON.
        
        Args:
            publications: Lista de publicaciones
            output_path: Ruta del archivo de salida
            indent: Espacios de indentación
        """
        data = {
            'total': len(publications),
            'publications': [pub.model_dump() for pub in publications]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        
        logger.info(f"Exportadas {len(publications)} publicaciones a {output_path}")
    
    def export_to_csv(
        self, 
        publications: List[Publication], 
        output_path: str
    ) -> None:
        """
        Exporta publicaciones a CSV.
        
        Args:
            publications: Lista de publicaciones
            output_path: Ruta del archivo de salida
        """
        import csv
        
        if not publications:
            logger.warning("No hay publicaciones para exportar")
            return
        
        # Definir columnas
        fieldnames = [
            'title', 'authors', 'year', 'abstract', 'keywords',
            'doi', 'url', 'venue', 'volume', 'issue', 'pages',
            'publisher', 'publication_type', 'source'
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for pub in publications:
                row = {
                    'title': pub.title,
                    'authors': '; '.join(pub.authors) if pub.authors else '',
                    'year': pub.year or '',
                    'abstract': pub.abstract,
                    'keywords': '; '.join(pub.keywords) if pub.keywords else '',
                    'doi': pub.doi,
                    'url': pub.url,
                    'venue': pub.venue or '',
                    'volume': pub.volume or '',
                    'issue': pub.issue or '',
                    'pages': pub.pages or '',
                    'publisher': pub.publisher or '',
                    'publication_type': pub.publication_type,
                    'source': pub.source
                }
                writer.writerow(row)
        
        logger.info(f"Exportadas {len(publications)} publicaciones a {output_path}")
    
    def get_stats(self) -> Dict[str, int]:
        """Retorna estadísticas del unificador."""
        return self.stats.copy()
    
    def get_parser_stats(self) -> Dict[str, Dict[str, int]]:
        """
        Retorna estadísticas de cada parser.
        
        Returns:
            Diccionario con stats de cada parser
        """
        return {
            ext: parser.get_stats()
            for ext, parser in self.parsers.items()
        }
