"""
Implementación de TF-IDF + Similitud del Coseno
===============================================

TF-IDF (Term Frequency - Inverse Document Frequency) es una técnica de
vectorización de texto que representa documentos como vectores numéricos
basados en la importancia de las palabras.

FUNDAMENTO MATEMÁTICO:
=====================

1. TF (Term Frequency) - Frecuencia del término:
   TF(t,d) = Frecuencia del término t en el documento d
             -----------------------------------------------
             Número total de términos en el documento d

2. IDF (Inverse Document Frequency) - Frecuencia inversa de documento:
   IDF(t,D) = log( Número total de documentos en D )
                   ------------------------------------
                   Número de documentos que contienen t

3. TF-IDF:
   TF-IDF(t,d,D) = TF(t,d) x IDF(t,D)

4. Similitud del Coseno:
   cos(θ) = (A · B) / (||A|| x ||B||)
   
   Donde:
   - A · B = Producto punto = Σ(Ai x Bi)
   - ||A|| = Norma euclidiana = √(Σ(Ai²))
   - ||B|| = Norma euclidiana = √(Σ(Bi²))
   
   Rango: [-1, 1]
   - 1 = Vectores idénticos en dirección
   - 0 = Vectores ortogonales (perpendiculares)
   - -1 = Vectores opuestos

INTERPRETACIÓN:
- Mide el ángulo entre dos vectores en el espacio de características
- No considera la magnitud, solo la orientación
- Ideal para comparar documentos de diferentes longitudes

COMPLEJIDAD:
- Vectorización: O(n x m) donde n = documentos, m = vocabulario
- Similitud del coseno: O(m) por par de documentos

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List, Tuple, Any
import logging

from .base_similarity import BaseSimilarity, SimilarityAlgorithmType

logger = logging.getLogger(__name__)


class TFIDFCosineSimilarity(BaseSimilarity):
    """
    Implementación de similitud usando TF-IDF + Coseno.
    
    Este algoritmo vectoriza los textos usando TF-IDF y luego calcula
    la similitud del coseno entre los vectores resultantes.
    
    Attributes:
        name: "TF-IDF + Similitud del Coseno"
        description: Descripción del algoritmo
        algorithm_type: TFIDF_COSINE
        vectorizer: Vectorizador TF-IDF de scikit-learn
    """
    
    def __init__(
        self, 
        max_features: int = 5000,
        ngram_range: Tuple[int, int] = (1, 2),
        min_df: int = 1,
        max_df: float = 0.9,
        use_stopwords: bool = True
    ):
        """
        Inicializa el algoritmo TF-IDF + Coseno.
        
        Args:
            max_features: Número máximo de características (términos)
            ngram_range: Rango de n-gramas a considerar (min, max)
            min_df: Frecuencia mínima de documento
            max_df: Frecuencia máxima de documento (fracción)
            use_stopwords: Si True, elimina palabras vacías en inglés
        """
        super().__init__(
            name="TF-IDF + Similitud del Coseno",
            description="Vectorización estadística con TF-IDF y similitud angular (coseno)",
            algorithm_type=SimilarityAlgorithmType.TFIDF_COSINE
        )
        
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.min_df = min_df
        self.max_df = max_df
        
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=min_df,
            max_df=max_df,
            stop_words='english' if use_stopwords else None,
            lowercase=True,
            strip_accents='unicode',
            token_pattern=r'\b\w+\b'
        )
        
        logger.info(f"TFIDFCosineSimilarity inicializado con max_features={max_features}, ngram_range={ngram_range}")
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula similitud del coseno entre dos textos.
        
        Proceso:
        1. Vectorizar ambos textos con TF-IDF
        2. Calcular similitud del coseno entre vectores
        3. Retornar valor normalizado [0, 1]
        
        Args:
            text1: Primer texto
            text2: Segundo texto
        
        Returns:
            Similitud del coseno entre 0.0 y 1.0
        """
        # Validar entradas
        self.validate_inputs(text1, text2)
        
        # Preprocesar textos
        text1 = self.preprocess_text(text1)
        text2 = self.preprocess_text(text2)
        
        # Caso especial: textos vacíos
        if len(text1) == 0 and len(text2) == 0:
            return 1.0
        if len(text1) == 0 or len(text2) == 0:
            return 0.0
        
        try:
            # Vectorizar textos
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            
            # Calcular similitud del coseno
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Asegurar que el valor esté en [0, 1]
            similarity = max(0.0, min(1.0, float(similarity)))
            
            logger.debug(f"TF-IDF Cosine: similarity={similarity:.4f}")
            
            return similarity
            
        except Exception as e:
            logger.error(f"Error en calculate_similarity: {str(e)}")
            return 0.0
    
    def analyze_step_by_step(self, text1: str, text2: str) -> Dict[str, Any]:
        """
        Análisis detallado con vectores TF-IDF y explicación matemática.
        
        Retorna información completa sobre:
        - Vectores TF-IDF de ambos textos
        - Términos más relevantes (mayor peso TF-IDF)
        - Producto punto y normas
        - Ángulo entre vectores
        - Explicación matemática paso a paso
        
        Args:
            text1: Primer texto
            text2: Segundo texto
        
        Returns:
            Diccionario con análisis completo
        """
        # Validar y preprocesar
        self.validate_inputs(text1, text2)
        text1_processed = self.preprocess_text(text1)
        text2_processed = self.preprocess_text(text2)
        
        # Vectorizar textos
        tfidf_matrix = self.vectorizer.fit_transform([text1_processed, text2_processed])
        
        # Obtener nombres de características (términos)
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Extraer vectores TF-IDF
        vector1 = tfidf_matrix[0].toarray()[0]
        vector2 = tfidf_matrix[1].toarray()[0]
        
        # Calcular similitud del coseno
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Identificar términos más relevantes
        top_terms_text1 = self._get_top_terms(vector1, feature_names, top_n=15)
        top_terms_text2 = self._get_top_terms(vector2, feature_names, top_n=15)
        
        # Identificar términos comunes
        common_terms = self._get_common_terms(vector1, vector2, feature_names, top_n=10)
        
        # Calcular normas euclidianas
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        
        # Calcular producto punto
        dot_product = np.dot(vector1, vector2)
        
        # Calcular ángulo en grados
        angle_radians = np.arccos(np.clip(similarity, -1, 1))
        angle_degrees = np.degrees(angle_radians)
        
        # Generar explicación detallada
        explanation = self._generate_explanation(
            text1_processed, text2_processed,
            vector1, vector2,
            dot_product, norm1, norm2,
            similarity, angle_degrees,
            top_terms_text1, top_terms_text2,
            common_terms,
            feature_names
        )
        
        # Estadísticas de vocabulario
        vocab_stats = self._get_vocabulary_stats(vector1, vector2, feature_names)
        
        return {
            "algorithm": self.name,
            "algorithm_type": self.algorithm_type.value,
            "inputs": {
                "text1_original": text1[:100] + "..." if len(text1) > 100 else text1,
                "text2_original": text2[:100] + "..." if len(text2) > 100 else text2,
                "text1_processed": text1_processed[:100] + "..." if len(text1_processed) > 100 else text1_processed,
                "text2_processed": text2_processed[:100] + "..." if len(text2_processed) > 100 else text2_processed
            },
            "vectorization": {
                "vocabulary_size": len(feature_names),
                "ngram_range": self.ngram_range,
                "max_features": self.max_features,
                "top_terms_text1": top_terms_text1,
                "top_terms_text2": top_terms_text2,
                "common_terms": common_terms
            },
            "vectors": {
                "text1": {
                    "norm": float(norm1),
                    "non_zero_features": int(np.count_nonzero(vector1)),
                    "sparsity": f"{(1 - np.count_nonzero(vector1) / len(vector1)) * 100:.2f}%"
                },
                "text2": {
                    "norm": float(norm2),
                    "non_zero_features": int(np.count_nonzero(vector2)),
                    "sparsity": f"{(1 - np.count_nonzero(vector2) / len(vector2)) * 100:.2f}%"
                }
            },
            "results": {
                "dot_product": float(dot_product),
                "similarity": float(similarity),
                "similarity_percentage": f"{similarity * 100:.2f}%",
                "angle_radians": float(angle_radians),
                "angle_degrees": float(angle_degrees)
            },
            "vocabulary_stats": vocab_stats,
            "complexity": {
                "vectorization": f"O(n x m) donde n=2 documentos, m={len(feature_names)} términos del vocabulario",
                "similarity": f"O(m) para producto punto y normas = O({len(feature_names)})"
            },
            "explanation": explanation
        }
    
    def _get_top_terms(
        self, 
        vector: np.ndarray, 
        feature_names: np.ndarray, 
        top_n: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Extrae los términos con mayor peso TF-IDF.
        
        Args:
            vector: Vector TF-IDF
            feature_names: Nombres de las características
            top_n: Número de términos a retornar
        
        Returns:
            Lista de diccionarios con término y peso TF-IDF
        """
        # Obtener índices ordenados por peso TF-IDF (descendente)
        top_indices = np.argsort(vector)[-top_n:][::-1]
        
        top_terms = []
        for idx in top_indices:
            if vector[idx] > 0:
                top_terms.append({
                    "term": feature_names[idx],
                    "tfidf_weight": float(vector[idx])
                })
        
        return top_terms
    
    def _get_common_terms(
        self,
        vector1: np.ndarray,
        vector2: np.ndarray,
        feature_names: np.ndarray,
        top_n: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Identifica términos comunes entre ambos vectores.
        
        Args:
            vector1: Vector TF-IDF del texto 1
            vector2: Vector TF-IDF del texto 2
            feature_names: Nombres de las características
            top_n: Número de términos comunes a retornar
        
        Returns:
            Lista de términos comunes con sus pesos
        """
        # Encontrar índices donde ambos vectores tienen valores > 0
        common_indices = np.where((vector1 > 0) & (vector2 > 0))[0]
        
        if len(common_indices) == 0:
            return []
        
        # Calcular importancia combinada
        combined_weights = vector1[common_indices] * vector2[common_indices]
        
        # Ordenar por importancia combinada
        sorted_indices = common_indices[np.argsort(combined_weights)[-top_n:][::-1]]
        
        common_terms = []
        for idx in sorted_indices:
            common_terms.append({
                "term": feature_names[idx],
                "weight_text1": float(vector1[idx]),
                "weight_text2": float(vector2[idx]),
                "combined_weight": float(vector1[idx] * vector2[idx])
            })
        
        return common_terms
    
    def _get_vocabulary_stats(
        self,
        vector1: np.ndarray,
        vector2: np.ndarray,
        feature_names: np.ndarray
    ) -> Dict[str, Any]:
        """
        Calcula estadísticas sobre el vocabulario.
        
        Returns:
            Diccionario con estadísticas de vocabulario
        """
        unique_terms_text1 = set(feature_names[vector1 > 0])
        unique_terms_text2 = set(feature_names[vector2 > 0])
        
        common_terms = unique_terms_text1.intersection(unique_terms_text2)
        
        return {
            "total_vocabulary": len(feature_names),
            "unique_terms_text1": len(unique_terms_text1),
            "unique_terms_text2": len(unique_terms_text2),
            "common_terms_count": len(common_terms),
            "jaccard_similarity": len(common_terms) / len(unique_terms_text1.union(unique_terms_text2)) if unique_terms_text1 or unique_terms_text2 else 0.0,
            "overlap_percentage": f"{(len(common_terms) / max(len(unique_terms_text1), len(unique_terms_text2)) * 100) if unique_terms_text1 or unique_terms_text2 else 0:.2f}%"
        }
    
    def _generate_explanation(
        self,
        text1: str,
        text2: str,
        vector1: np.ndarray,
        vector2: np.ndarray,
        dot_product: float,
        norm1: float,
        norm2: float,
        similarity: float,
        angle_degrees: float,
        top_terms1: List[Dict],
        top_terms2: List[Dict],
        common_terms: List[Dict],
        feature_names: np.ndarray
    ) -> str:
        """
        Genera explicación matemática detallada en formato Markdown.
        
        Returns:
            Explicación completa en Markdown
        """
        explanation = f"""
# ANÁLISIS DE SIMILITUD CON TF-IDF + COSENO

## Textos Analizados

**Texto 1**:
```
{text1[:200]}{"..." if len(text1) > 200 else ""}
```

**Texto 2**:
```
{text2[:200]}{"..." if len(text2) > 200 else ""}
```

## Fundamento Matemático

### 1. Vectorización TF-IDF

**TF (Term Frequency)**:
```
TF(t,d) = Frecuencia del término t en documento d / Total de términos en d
```

**IDF (Inverse Document Frequency)**:
```
IDF(t,D) = log(Total de documentos / Documentos que contienen t)
```

**TF-IDF**:
```
TF-IDF(t,d,D) = TF(t,d) x IDF(t,D)
```

**Vocabulario total**: {len(feature_names)} términos únicos

### 2. Términos Más Relevantes

**Texto 1** (Top 5):
"""
        
        for i, term_info in enumerate(top_terms1[:5], 1):
            explanation += f"{i}. `{term_info['term']}`: TF-IDF = {term_info['tfidf_weight']:.4f}\n"
        
        explanation += "\n**Texto 2** (Top 5):\n"
        for i, term_info in enumerate(top_terms2[:5], 1):
            explanation += f"{i}. `{term_info['term']}`: TF-IDF = {term_info['tfidf_weight']:.4f}\n"
        
        if common_terms:
            explanation += "\n**Términos Comunes** (Top 5):\n"
            for i, term_info in enumerate(common_terms[:5], 1):
                explanation += f"{i}. `{term_info['term']}`: T1={term_info['weight_text1']:.4f}, T2={term_info['weight_text2']:.4f}\n"
        
        explanation += f"""

### 3. Similitud del Coseno

**Fórmula**:
```
cos(θ) = (A · B) / (||A|| x ||B||)
```

Donde:
- **A · B** = Producto punto de vectores
- **||A||** = Norma euclidiana de A
- **||B||** = Norma euclidiana de B

**Cálculo**:
```
Producto punto (A · B) = {dot_product:.6f}
Norma de A (||A||)     = {norm1:.6f}
Norma de B (||B||)     = {norm2:.6f}

cos(θ) = {dot_product:.6f} / ({norm1:.6f} × {norm2:.6f})
       = {dot_product:.6f} / {norm1 * norm2:.6f}
       = {similarity:.6f}
```

## Resultados

- **Similitud del coseno**: {similarity:.4f} ({similarity*100:.2f}%)
- **Ángulo entre vectores**: {angle_degrees:.2f}°
- **Términos no-cero en Texto 1**: {np.count_nonzero(vector1)} de {len(vector1)}
- **Términos no-cero en Texto 2**: {np.count_nonzero(vector2)} de {len(vector2)}
- **Términos comunes**: {len(common_terms)}

## Interpretación

- **Ángulo de {angle_degrees:.2f}°**:
  - 0° = Vectores idénticos
  - 90° = Vectores ortogonales (sin relación)
  - 180° = Vectores opuestos

- **Similitud de {similarity*100:.2f}%**:
  - ✅ **Muy similares** (>80%) si similarity > 0.80
  - ⚠️ **Moderadamente similares** (50-80%) si 0.50 ≤ similarity ≤ 0.80
  - ❌ **Poco similares** (<50%) si similarity < 0.50

**Conclusión**: Los documentos son **{"muy similares" if similarity > 0.8 else "moderadamente similares" if similarity > 0.5 else "poco similares"}**.

## Complejidad Algorítmica

- **Vectorización**: O(n x m) donde n=2 documentos, m={len(feature_names)} términos
- **Similitud del coseno**: O(m) = O({len(feature_names)})
- **Total**: O(m) = O({len(feature_names)})
"""
        
        return explanation.strip()
