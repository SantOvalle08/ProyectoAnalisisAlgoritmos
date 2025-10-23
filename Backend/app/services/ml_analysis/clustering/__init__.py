"""
Clustering Module - Requerimiento 4
====================================

Módulo para agrupamiento jerárquico de publicaciones científicas.

Componentes:
- HierarchicalClustering: Clase principal para clustering jerárquico
- LinkageMethod: Enum con métodos de linkage disponibles

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Date: Octubre 2025
University: Universidad del Quindío - Análisis de Algoritmos
"""

from .hierarchical_clustering import (
    HierarchicalClustering,
    LinkageMethod,
    ClusteringResult
)

__all__ = [
    'HierarchicalClustering',
    'LinkageMethod',
    'ClusteringResult'
]
