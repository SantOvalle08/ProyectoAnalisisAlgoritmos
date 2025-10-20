"""
Data Models Module

Contiene los modelos de datos Pydantic para validación y serialización.

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

from .publication import Publication, Author

__all__ = [
    'Publication',
    'Author'
]