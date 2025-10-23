"""
Módulo de Análisis de Frecuencias
==================================

Este módulo proporciona herramientas para análisis de frecuencias
de conceptos en textos científicos.

Exporta:
- ConceptAnalyzer: Clase principal para análisis de frecuencias
- ConceptFrequency: Dataclass para representar frecuencias
- KeywordScore: Dataclass para keywords extraídos
- ExtractionMethod: Enum de métodos de extracción
"""

from .concept_analyzer import (
    ConceptAnalyzer,
    ConceptFrequency,
    KeywordScore,
    ExtractionMethod
)

__all__ = [
    'ConceptAnalyzer',
    'ConceptFrequency',
    'KeywordScore',
    'ExtractionMethod'
]
