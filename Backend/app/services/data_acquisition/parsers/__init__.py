"""
Parsers Module
==============

Módulo para parsear diferentes formatos bibliográficos y convertirlos
al modelo unificado de Publication.

Formatos soportados:
- BibTeX (.bib)
- RIS (.ris)
- CSV (.csv)
- JSON (.json)

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Date: Octubre 2025
University: Universidad del Quindío - Análisis de Algoritmos
"""

from .bibtex_parser import BibTeXParser
from .ris_parser import RISParser
from .csv_parser import CSVParser
from .unifier import PublicationUnifier

__all__ = [
    'BibTeXParser',
    'RISParser',
    'CSVParser',
    'PublicationUnifier'
]
