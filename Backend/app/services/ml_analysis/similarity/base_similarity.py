"""
Clase Base para Algoritmos de Similitud Textual
================================================

Define la interfaz común para todos los algoritmos de similitud implementados.

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SimilarityAlgorithmType(Enum):
    """Tipos de algoritmos de similitud disponibles."""
    LEVENSHTEIN = "levenshtein"
    TFIDF_COSINE = "tfidf_cosine"
    JACCARD = "jaccard"
    NGRAMS = "ngrams"
    BERT = "bert"
    SENTENCE_BERT = "sentence_bert"


class BaseSimilarity(ABC):
    """
    Clase base abstracta para algoritmos de similitud textual.
    
    Esta clase define la interfaz que deben implementar todos los algoritmos
    de similitud, tanto clásicos como basados en IA.
    
    Attributes:
        name: Nombre del algoritmo
        description: Descripción breve del funcionamiento
        algorithm_type: Tipo de algoritmo (clásico o IA)
    """
    
    def __init__(self, name: str, description: str, algorithm_type: SimilarityAlgorithmType):
        """
        Inicializa el algoritmo de similitud.
        
        Args:
            name: Nombre descriptivo del algoritmo
            description: Descripción del funcionamiento
            algorithm_type: Tipo de algoritmo
        """
        self.name = name
        self.description = description
        self.algorithm_type = algorithm_type
        logger.info(f"Inicializado algoritmo: {name}")
    
    @abstractmethod
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula la similitud entre dos textos.
        
        Args:
            text1: Primer texto a comparar
            text2: Segundo texto a comparar
        
        Returns:
            Valor de similitud entre 0.0 y 1.0
            - 0.0: Completamente diferentes
            - 1.0: Idénticos
        """
        pass
    
    @abstractmethod
    def analyze_step_by_step(self, text1: str, text2: str) -> Dict[str, Any]:
        """
        Realiza análisis detallado paso a paso con explicaciones matemáticas.
        
        Este método debe retornar información completa sobre el proceso de
        cálculo, incluyendo:
        - Pasos intermedios
        - Valores de métricas
        - Explicaciones matemáticas
        - Complejidad algorítmica
        
        Args:
            text1: Primer texto a analizar
            text2: Segundo texto a analizar
        
        Returns:
            Diccionario con análisis completo del proceso
        """
        pass
    
    def compare_multiple(
        self, 
        reference_text: str, 
        texts_to_compare: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Compara un texto de referencia con múltiples textos.
        
        Args:
            reference_text: Texto de referencia
            texts_to_compare: Lista de textos para comparar
        
        Returns:
            Lista de diccionarios con resultados de cada comparación
        """
        results = []
        
        for i, text in enumerate(texts_to_compare):
            similarity = self.calculate_similarity(reference_text, text)
            results.append({
                "index": i,
                "text": text[:100] + "..." if len(text) > 100 else text,
                "similarity": similarity,
                "algorithm": self.name
            })
        
        # Ordenar por similitud descendente
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        return results
    
    def get_algorithm_info(self) -> Dict[str, Any]:
        """
        Retorna información completa sobre el algoritmo.
        
        Returns:
            Diccionario con información del algoritmo
        """
        return {
            "name": self.name,
            "description": self.description,
            "type": self.algorithm_type.value,
            "category": "AI-based" if "bert" in self.algorithm_type.value else "Classical"
        }
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocesa el texto antes del análisis.
        
        Este método puede ser sobrescrito por subclases que requieran
        preprocesamiento específico.
        
        Args:
            text: Texto a preprocesar
        
        Returns:
            Texto preprocesado
        """
        # Preprocesamiento básico
        if not text:
            return ""
        
        # Eliminar espacios múltiples
        text = " ".join(text.split())
        
        return text.strip()
    
    def validate_inputs(self, text1: str, text2: str) -> None:
        """
        Valida las entradas antes del cálculo.
        
        Args:
            text1: Primer texto
            text2: Segundo texto
        
        Raises:
            ValueError: Si alguna entrada es inválida
        """
        if text1 is None or text2 is None:
            raise ValueError("Los textos no pueden ser None")
        
        if not isinstance(text1, str) or not isinstance(text2, str):
            raise ValueError("Los textos deben ser cadenas de caracteres")
        
        if len(text1.strip()) == 0 and len(text2.strip()) == 0:
            logger.warning("Ambos textos están vacíos")
