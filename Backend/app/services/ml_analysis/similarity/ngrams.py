"""
Implementación de Similitud por N-gramas
========================================

La similitud por n-gramas es una técnica que compara textos basándose en
secuencias contiguas de n elementos (caracteres o palabras). Es especialmente
útil para detectar similitudes a pesar de pequeñas variaciones ortográficas
o errores tipográficos.

FUNDAMENTO MATEMÁTICO:
=====================

Un **n-grama** es una secuencia contigua de n elementos extraídos de un texto.

Para caracteres:
- Texto: "hello"
- 2-gramas (bigramas): ["he", "el", "ll", "lo"]
- 3-gramas (trigramas): ["hel", "ell", "llo"]

Para palabras:
- Texto: "machine learning is powerful"
- 2-gramas: ["machine learning", "learning is", "is powerful"]

MEDIDAS DE SIMILITUD:
====================

1. **Coeficiente de Dice** (recomendado):
   ```
   Dice(A, B) = 2 x |A ∩ | / (|A| + |B|)
   ```

2. **Coeficiente de Jaccard**:
   ```
   Jaccard(A, B) = |A ∩ B| / |A u B|
   ```

3. **Similitud del Coseno** (con frecuencias):
   ```
   cos(θ) = Σ(freq_A[i] x freq_B[i]) / (||freq_A|| x ||freq_B||)
   ```

PROPIEDADES:
- Robusto ante errores tipográficos
- Captura similitud local (subsecuencias)
- Eficiente computacionalmente
- Ajustable mediante el valor de n

COMPLEJIDAD:
- Generación de n-gramas: O(m) por texto
- Comparación: O(min(|A|, |B|)) con conjuntos
- Total: O(m + n) donde m, n son longitudes de textos

VENTAJAS:
- Detecta similitud parcial
- Robusto ante reordenamientos locales
- Funciona bien con múltiples idiomas

DESVENTAJAS:
- No captura similitud semántica
- Sensible a la elección de n
- Genera muchos n-gramas para valores altos de n

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

from collections import Counter
from typing import List, Dict, Any, Tuple, Set
import math
import logging

from .base_similarity import BaseSimilarity, SimilarityAlgorithmType

logger = logging.getLogger(__name__)


class NGramSimilarity(BaseSimilarity):
    """
    Implementación de similitud basada en n-gramas.
    
    Este algoritmo extrae n-gramas de los textos y calcula similitud usando
    diferentes métricas: Dice, Jaccard, o Coseno.
    
    Soporta:
    - N-gramas de caracteres (más robusto ante errores)
    - N-gramas de palabras (captura contexto)
    - Múltiples métricas de similitud
    
    Attributes:
        name: "Similitud por N-gramas"
        description: Descripción del algoritmo
        algorithm_type: NGRAMS
        n: Tamaño de los n-gramas
        ngram_type: 'char' o 'word'
        similarity_metric: 'dice', 'jaccard', o 'cosine'
        use_padding: Si True, agrega padding al inicio/fin
    """
    
    def __init__(
        self,
        n: int = 3,
        ngram_type: str = 'char',
        similarity_metric: str = 'dice',
        use_padding: bool = True,
        case_sensitive: bool = False
    ):
        """
        Inicializa el algoritmo de n-gramas.
        
        Args:
            n: Tamaño de los n-gramas (típicamente 2-5)
            ngram_type: 'char' para n-gramas de caracteres, 'word' para palabras
            similarity_metric: 'dice', 'jaccard', o 'cosine'
            use_padding: Si True, agrega espacios al inicio/fin para n-gramas de bordes
            case_sensitive: Si True, distingue mayúsculas/minúsculas
        """
        super().__init__(
            name=f"Similitud por {n}-gramas de {ngram_type}",
            description=f"Similitud basada en {n}-gramas con métrica {similarity_metric}",
            algorithm_type=SimilarityAlgorithmType.NGRAMS
        )
        
        if n < 1:
            raise ValueError("n debe ser al menos 1")
        if ngram_type not in ['char', 'word']:
            raise ValueError("ngram_type debe ser 'char' o 'word'")
        if similarity_metric not in ['dice', 'jaccard', 'cosine']:
            raise ValueError("similarity_metric debe ser 'dice', 'jaccard', o 'cosine'")
        
        self.n = n
        self.ngram_type = ngram_type
        self.similarity_metric = similarity_metric
        self.use_padding = use_padding
        self.case_sensitive = case_sensitive
        
        logger.info(f"NGramSimilarity inicializado: n={n}, type={ngram_type}, "
                   f"metric={similarity_metric}")
    
    def extract_ngrams(self, text: str) -> List[str]:
        """
        Extrae n-gramas de un texto.
        
        Args:
            text: Texto del cual extraer n-gramas
        
        Returns:
            Lista de n-gramas
        """
        if not self.case_sensitive:
            text = text.lower()
        
        if self.ngram_type == 'char':
            # N-gramas de caracteres
            if self.use_padding:
                # Agregar padding
                padding = ' ' * (self.n - 1)
                text = padding + text + padding
            
            ngrams = []
            for i in range(len(text) - self.n + 1):
                ngram = text[i:i + self.n]
                ngrams.append(ngram)
            
            return ngrams
        
        else:  # word
            # N-gramas de palabras
            words = text.split()
            
            if len(words) < self.n:
                # Si hay menos palabras que n, retornar el texto completo como un n-grama
                return [' '.join(words)] if words else []
            
            ngrams = []
            for i in range(len(words) - self.n + 1):
                ngram = ' '.join(words[i:i + self.n])
                ngrams.append(ngram)
            
            return ngrams
    
    def calculate_dice_coefficient(
        self,
        ngrams1: List[str],
        ngrams2: List[str]
    ) -> float:
        """
        Calcula el coeficiente de Dice.
        
        Fórmula: Dice(A, B) = 2 x |A ∩ B| / (|A| + |B|)
        
        Args:
            ngrams1: N-gramas del primer texto
            ngrams2: N-gramas del segundo texto
        
        Returns:
            Coeficiente de Dice entre 0.0 y 1.0
        """
        set1 = set(ngrams1)
        set2 = set(ngrams2)
        
        intersection = set1.intersection(set2)
        
        denominator = len(set1) + len(set2)
        if denominator == 0:
            return 0.0
        
        return (2.0 * len(intersection)) / denominator
    
    def calculate_jaccard_coefficient(
        self,
        ngrams1: List[str],
        ngrams2: List[str]
    ) -> float:
        """
        Calcula el coeficiente de Jaccard.
        
        Fórmula: Jaccard(A, B) = |A ∩ B| / |A u B|
        
        Args:
            ngrams1: N-gramas del primer texto
            ngrams2: N-gramas del segundo texto
        
        Returns:
            Coeficiente de Jaccard entre 0.0 y 1.0
        """
        set1 = set(ngrams1)
        set2 = set(ngrams2)
        
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        
        if len(union) == 0:
            return 0.0
        
        return len(intersection) / len(union)
    
    def calculate_cosine_similarity(
        self,
        ngrams1: List[str],
        ngrams2: List[str]
    ) -> float:
        """
        Calcula similitud del coseno basada en frecuencias de n-gramas.
        
        Fórmula: cos(θ) = Σ(freq1[i] x freq2[i]) / (||freq1|| x ||freq2||)
        
        Args:
            ngrams1: N-gramas del primer texto
            ngrams2: N-gramas del segundo texto
        
        Returns:
            Similitud del coseno entre 0.0 y 1.0
        """
        # Contar frecuencias
        counter1 = Counter(ngrams1)
        counter2 = Counter(ngrams2)
        
        # Obtener todos los n-gramas únicos
        all_ngrams = set(counter1.keys()).union(set(counter2.keys()))
        
        if len(all_ngrams) == 0:
            return 0.0
        
        # Calcular producto punto
        dot_product = sum(counter1[ngram] * counter2[ngram] for ngram in all_ngrams)
        
        # Calcular normas
        norm1 = math.sqrt(sum(count ** 2 for count in counter1.values()))
        norm2 = math.sqrt(sum(count ** 2 for count in counter2.values()))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula similitud por n-gramas entre dos textos.
        
        Proceso:
        1. Extraer n-gramas de ambos textos
        2. Calcular similitud usando la métrica configurada
        3. Retornar valor normalizado [0, 1]
        
        Args:
            text1: Primer texto
            text2: Segundo texto
        
        Returns:
            Similitud entre 0.0 y 1.0
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
        
        # Extraer n-gramas
        ngrams1 = self.extract_ngrams(text1)
        ngrams2 = self.extract_ngrams(text2)
        
        # Calcular similitud según métrica configurada
        if self.similarity_metric == 'dice':
            similarity = self.calculate_dice_coefficient(ngrams1, ngrams2)
        elif self.similarity_metric == 'jaccard':
            similarity = self.calculate_jaccard_coefficient(ngrams1, ngrams2)
        else:  # cosine
            similarity = self.calculate_cosine_similarity(ngrams1, ngrams2)
        
        logger.debug(f"N-gram similarity: n={self.n}, type={self.ngram_type}, "
                    f"metric={self.similarity_metric}, similarity={similarity:.4f}")
        
        return float(similarity)
    
    def analyze_step_by_step(self, text1: str, text2: str) -> Dict[str, Any]:
        """
        Análisis detallado paso a paso con explicación matemática.
        
        Retorna información completa sobre:
        - N-gramas extraídos de cada texto
        - N-gramas comunes y únicos
        - Frecuencias de n-gramas
        - Cálculos de la métrica de similitud
        - Explicación matemática detallada
        
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
        
        # Extraer n-gramas
        ngrams1 = self.extract_ngrams(text1_processed)
        ngrams2 = self.extract_ngrams(text2_processed)
        
        # Contar frecuencias
        counter1 = Counter(ngrams1)
        counter2 = Counter(ngrams2)
        
        # Calcular conjuntos
        set1 = set(ngrams1)
        set2 = set(ngrams2)
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        unique_to_text1 = set1 - set2
        unique_to_text2 = set2 - set1
        
        # Calcular similitud con todas las métricas para comparación
        dice = self.calculate_dice_coefficient(ngrams1, ngrams2)
        jaccard = self.calculate_jaccard_coefficient(ngrams1, ngrams2)
        cosine = self.calculate_cosine_similarity(ngrams1, ngrams2)
        
        # La similitud principal es la métrica configurada
        similarity = {
            'dice': dice,
            'jaccard': jaccard,
            'cosine': cosine
        }[self.similarity_metric]
        
        # Obtener n-gramas más frecuentes
        top_ngrams1 = counter1.most_common(15)
        top_ngrams2 = counter2.most_common(15)
        
        # N-gramas comunes con sus frecuencias
        common_ngrams = []
        for ngram in intersection:
            common_ngrams.append({
                "ngram": ngram,
                "freq_text1": counter1[ngram],
                "freq_text2": counter2[ngram]
            })
        common_ngrams.sort(key=lambda x: x["freq_text1"] + x["freq_text2"], reverse=True)
        
        # Generar explicación detallada
        explanation = self._generate_explanation(
            text1_processed, text2_processed,
            ngrams1, ngrams2,
            set1, set2, intersection, union,
            counter1, counter2,
            dice, jaccard, cosine,
            top_ngrams1, top_ngrams2,
            common_ngrams[:15]
        )
        
        return {
            "algorithm": self.name,
            "algorithm_type": self.algorithm_type.value,
            "configuration": {
                "n": self.n,
                "ngram_type": self.ngram_type,
                "similarity_metric": self.similarity_metric,
                "use_padding": self.use_padding,
                "case_sensitive": self.case_sensitive
            },
            "inputs": {
                "text1_original": text1[:100] + "..." if len(text1) > 100 else text1,
                "text2_original": text2[:100] + "..." if len(text2) > 100 else text2,
                "text1_processed": text1_processed[:100] + "..." if len(text1_processed) > 100 else text1_processed,
                "text2_processed": text2_processed[:100] + "..." if len(text2_processed) > 100 else text2_processed
            },
            "ngrams": {
                "total_ngrams_text1": len(ngrams1),
                "total_ngrams_text2": len(ngrams2),
                "unique_ngrams_text1": len(set1),
                "unique_ngrams_text2": len(set2),
                "sample_ngrams_text1": ngrams1[:20],
                "sample_ngrams_text2": ngrams2[:20],
                "top_ngrams_text1": [{"ngram": ng, "freq": freq} for ng, freq in top_ngrams1[:10]],
                "top_ngrams_text2": [{"ngram": ng, "freq": freq} for ng, freq in top_ngrams2[:10]]
            },
            "set_operations": {
                "intersection_size": len(intersection),
                "union_size": len(union),
                "unique_to_text1_size": len(unique_to_text1),
                "unique_to_text2_size": len(unique_to_text2),
                "common_ngrams": common_ngrams[:15],
                "sample_unique_to_text1": list(unique_to_text1)[:10],
                "sample_unique_to_text2": list(unique_to_text2)[:10]
            },
            "results": {
                "similarity": float(similarity),
                "similarity_percentage": f"{similarity * 100:.2f}%",
                "metric_used": self.similarity_metric,
                "all_metrics": {
                    "dice": float(dice),
                    "jaccard": float(jaccard),
                    "cosine": float(cosine)
                }
            },
            "complexity": {
                "extraction": f"O(m) + O(n) donde m={len(text1_processed)}, n={len(text2_processed)}",
                "comparison": f"O(min(|A|,|B|)) = O({min(len(set1), len(set2))})",
                "total": f"O(m+n) = O({len(text1_processed) + len(text2_processed)})"
            },
            "explanation": explanation
        }
    
    def _generate_explanation(
        self,
        text1: str,
        text2: str,
        ngrams1: List[str],
        ngrams2: List[str],
        set1: Set[str],
        set2: Set[str],
        intersection: Set[str],
        union: Set[str],
        counter1: Counter,
        counter2: Counter,
        dice: float,
        jaccard: float,
        cosine: float,
        top_ngrams1: List[Tuple[str, int]],
        top_ngrams2: List[Tuple[str, int]],
        common_ngrams: List[Dict]
    ) -> str:
        """
        Genera explicación matemática detallada en formato Markdown.
        
        Returns:
            Explicación completa en Markdown
        """
        explanation = f"""
# ANÁLISIS DE SIMILITUD CON {self.n}-GRAMAS

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

Un **{self.n}-grama** es una secuencia contigua de {self.n} elementos ({self.ngram_type}).

### Configuración
- **Tipo**: {self.n}-gramas de {self.ngram_type}
- **Métrica**: {self.similarity_metric}
- **Padding**: {"Sí" if self.use_padding else "No"}
- **Case sensitive**: {"Sí" if self.case_sensitive else "No"}

## Paso 1: Extracción de N-gramas

**Texto 1**:
- Total de {self.n}-gramas: {len(ngrams1)}
- N-gramas únicos: {len(set1)}
- Ejemplo de primeros {self.n}-gramas: {ngrams1[:5]}

**Top 5 {self.n}-gramas más frecuentes en Texto 1**:
"""
        
        for i, (ngram, freq) in enumerate(top_ngrams1[:5], 1):
            explanation += f"{i}. `{ngram}`: {freq} veces\n"
        
        explanation += f"""

**Texto 2**:
- Total de {self.n}-gramas: {len(ngrams2)}
- N-gramas únicos: {len(set2)}
- Ejemplo de primeros {self.n}-gramas: {ngrams2[:5]}

**Top 5 {self.n}-gramas más frecuentes en Texto 2**:
"""
        
        for i, (ngram, freq) in enumerate(top_ngrams2[:5], 1):
            explanation += f"{i}. `{ngram}`: {freq} veces\n"
        
        explanation += f"""

## Paso 2: Operaciones de Conjuntos

**Intersección (n-gramas comunes)**:
- Total: {len(intersection)} n-gramas

"""
        
        if common_ngrams:
            explanation += "Top 5 n-gramas comunes:\n"
            for i, item in enumerate(common_ngrams[:5], 1):
                explanation += f"{i}. `{item['ngram']}`: T1={item['freq_text1']}x, T2={item['freq_text2']}x\n"
        
        explanation += f"""

**Unión**:
- Total: {len(union)} n-gramas únicos

**Solo en Texto 1**: {len(set1 - set2)} n-gramas
**Solo en Texto 2**: {len(set2 - set1)} n-gramas

## Paso 3: Cálculo de Similitud

### Coeficiente de Dice
```
Dice(A, B) = 2 × |A ∩ B| / (|A| + |B|)
           = 2 × {len(intersection)} / ({len(set1)} + {len(set2)})
           = {dice:.6f}
```

### Coeficiente de Jaccard
```
Jaccard(A, B) = |A ∩ B| / |A ∪ B|
              = {len(intersection)} / {len(union)}
              = {jaccard:.6f}
```

### Similitud del Coseno (con frecuencias)
```
cos(θ) = Σ(freq_A[i] × freq_B[i]) / (||freq_A|| × ||freq_B||)
       = {cosine:.6f}
```

## Resultados

**Métrica principal**: {self.similarity_metric}

- **Similitud de Dice**: {dice:.4f} ({dice*100:.2f}%)
- **Similitud de Jaccard**: {jaccard:.4f} ({jaccard*100:.2f}%)
- **Similitud del Coseno**: {cosine:.4f} ({cosine*100:.2f}%)

## Interpretación

"""
        
        # Calcular similitud según métrica
        metric_value = {"dice": dice, "jaccard": jaccard, "cosine": cosine}[self.similarity_metric]
        
        if metric_value > 0.7:
            conclusion = "muy similares"
        elif metric_value > 0.4:
            conclusion = "moderadamente similares"
        else:
            conclusion = "poco similares"
        
        explanation += f"""
Con una similitud de **{self.similarity_metric}** de **{metric_value*100:.2f}%**:

- ✅ **Muy similares** (>70%) si similitud > 0.70
- ⚠️ **Moderadamente similares** (40-70%) si 0.40 ≤ similitud ≤ 0.70
- ❌ **Poco similares** (<40%) si similitud < 0.40

**Conclusión**: Los textos son **{conclusion}** según la métrica {self.similarity_metric}.

## Complejidad Algorítmica

- **Extracción de n-gramas**: O(m) + O(n) = O({len(text1)} + {len(text2)})
- **Comparación de conjuntos**: O(min(|A|, |B|)) = O({min(len(set1), len(set2))})
- **Total**: O(m + n) = O({len(text1) + len(text2)})
"""
        
        return explanation.strip()
