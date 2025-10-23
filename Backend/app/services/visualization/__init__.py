"""
Módulo de Visualizaciones para Análisis Bibliométrico
======================================================

Servicio para generación de visualizaciones interactivas:
- Mapas de calor geográficos (distribución de autores)
- Nubes de palabras dinámicas (abstracts + keywords)
- Líneas temporales interactivas (publicaciones por año/revista)
- Exportación automática a PDF

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Date: Octubre 2025
University: Universidad del Quindío - Análisis de Algoritmos
"""

from .geographic_heatmap import GeographicHeatmap
from .wordcloud_generator import WordCloudGenerator
from .timeline_chart import TimelineChart
from .pdf_exporter import PDFExporter

__all__ = [
    'GeographicHeatmap',
    'WordCloudGenerator',
    'TimelineChart',
    'PDFExporter'
]