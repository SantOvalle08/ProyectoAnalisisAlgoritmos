"""
Implementación del Coeficiente de Jaccard
=========================================

El Coeficiente de Jaccard (también conocido como Índice de Jaccard o Jaccard
Similarity) mide la similitud entre dos conjuntos calculando el tamaño de su
intersección dividido por el tamaño de su unión.

FUNDAMENTO MATEMÁTICO:
=====================

Para dos conjuntos A y B:

J(A, B) = |A ∩ B| / |A u B|

Donde:
- |A ∩ B| = Cardinalidad de la intersección (elementos comunes)
- |A u B| = Cardinalidad de la unión (todos los elementos únicos)

PROPIEDADES:
- Rango: [0, 1]
  - J(A, B) = 0 cuando A y B son disjuntos (sin elementos comunes)
  - J(A, B) = 1 cuando A = B (conjuntos idénticos)
- Simétrico: J(A, B) = J(B, A)
- No métrica: No satisface la desigualdad triangular

APLICACIÓN A TEXTOS:
Para comparar textos, convertimos cada texto en un conjunto de tokens (palabras).
Existen dos enfoques principales:

1. **Jaccard de Palabras**: Conjuntos de palabras únicas
2. **Jaccard de N-gramas de Caracteres**: Conjuntos de subsecuencias de n caracteres

COMPLEJIDAD:
- Tokenización: O(m + n) donde m, n son longitudes de textos
- Intersección y unión: O(min(|A|, |B|)) con conjuntos
- Total: O(m + n)

VENTAJAS:
- Simple de implementar y entender
- Eficiente computacionalmente
- Robusto ante diferencias de longitud

DESVENTAJAS:
- No considera orden de palabras
- No pondera palabras por importancia
- Sensible a variaciones morfológicas

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

import re
from typing import Set, List, Dict, Any, Tuple
import logging

from .base_similarity import BaseSimilarity, SimilarityAlgorithmType

logger = logging.getLogger(__name__)


class JaccardSimilarity(BaseSimilarity):
    """
    Implementación del Coeficiente de Jaccard para similitud textual.
    
    Este algoritmo convierte cada texto en un conjunto de tokens y calcula
    la similitud basándose en la intersección y unión de estos conjuntos.
    
    Soporta dos modos:
    1. Token-based: Conjuntos de palabras
    2. Character n-gram based: Conjuntos de n-gramas de caracteres
    
    Attributes:
        name: "Coeficiente de Jaccard"
        description: Descripción del algoritmo
        algorithm_type: JACCARD
        use_char_ngrams: Si True, usa n-gramas de caracteres
        ngram_size: Tamaño de los n-gramas (solo si use_char_ngrams=True)
        case_sensitive: Si True, considera mayúsculas/minúsculas
        remove_stopwords: Si True, elimina palabras vacías
    """
    
    # Lista básica de palabras vacías en inglés
    STOPWORDS = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
        'to', 'was', 'will', 'with', 'the', 'this', 'but', 'they', 'have',
        'had', 'what', 'when', 'where', 'who', 'which', 'why', 'how'
    }
    
    def __init__(
        self,
        use_char_ngrams: bool = False,
        ngram_size: int = 3,
        case_sensitive: bool = False,
        remove_stopwords: bool = True
    ):
        """
        Inicializa el algoritmo de Jaccard.
        
        Args:
            use_char_ngrams: Si True, usa n-gramas de caracteres en lugar de palabras
            ngram_size: Tamaño de los n-gramas (solo si use_char_ngrams=True)
            case_sensitive: Si True, distingue mayúsculas de minúsculas
            remove_stopwords: Si True, elimina palabras vacías comunes
        """
        mode = "character n-grams" if use_char_ngrams else "word tokens"
        super().__init__(
            name=f"Coeficiente de Jaccard ({mode})",
            description=f"Similitud basada en intersección/unión de {mode}",
            algorithm_type=SimilarityAlgorithmType.JACCARD
        )
        
        self.use_char_ngrams = use_char_ngrams
        self.ngram_size = ngram_size
        self.case_sensitive = case_sensitive
        self.remove_stopwords = remove_stopwords
        
        logger.info(f"JaccardSimilarity inicializado: char_ngrams={use_char_ngrams}, "
                   f"ngram_size={ngram_size}, case_sensitive={case_sensitive}")
    
    def tokenize_text(self, text: str) -> Set[str]:
        """
        Convierte un texto en un conjunto de tokens.
        
        Si use_char_ngrams=True, genera n-gramas de caracteres.
        Si use_char_ngrams=False, genera tokens de palabras.
        
        Args:
            text: Texto a tokenizar
        
        Returns:
            Conjunto de tokens (palabras o n-gramas)
        """
        if not self.case_sensitive:
            text = text.lower()
        
        if self.use_char_ngrams:
            # Generar n-gramas de caracteres
            # Remover espacios y puntuación para n-gramas
            clean_text = re.sub(r'[^\w]', '', text)
            ngrams = set()
            for i in range(len(clean_text) - self.ngram_size + 1):
                ngram = clean_text[i:i + self.ngram_size]
                ngrams.add(ngram)
            return ngrams
        else:
            # Tokenizar por palabras
            # Extraer palabras (secuencias de letras y números)
            words = re.findall(r'\b\w+\b', text)
            
            # Convertir a conjunto
            token_set = set(words)
            
            # Remover stopwords si está habilitado
            if self.remove_stopwords:
                token_set = token_set - self.STOPWORDS
            
            return token_set
    
    def calculate_jaccard_coefficient(
        self,
        set1: Set[str],
        set2: Set[str]
    ) -> Tuple[float, Set[str], Set[str]]:
        """
        Calcula el coeficiente de Jaccard entre dos conjuntos.
        
        Fórmula: J(A, B) = |A ∩ B| / |A ∪ B|
        
        Args:
            set1: Primer conjunto
            set2: Segundo conjunto
        
        Returns:
            Tupla (coeficiente, intersección, unión)
        """
        # Calcular intersección y unión
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        
        # Caso especial: ambos conjuntos vacíos
        if len(union) == 0:
            return 1.0, intersection, union
        
        # Calcular coeficiente
        coefficient = len(intersection) / len(union)
        
        return coefficient, intersection, union
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula la similitud de Jaccard entre dos textos.
        
        Proceso:
        1. Tokenizar ambos textos en conjuntos
        2. Calcular intersección y unión
        3. Retornar |intersección| / |unión|
        
        Args:
            text1: Primer texto
            text2: Segundo texto
        
        Returns:
            Coeficiente de Jaccard entre 0.0 y 1.0
        """
        # Validar entradas
        self.validate_inputs(text1, text2)
        
        # Preprocesar textos
        text1 = self.preprocess_text(text1)
        text2 = self.preprocess_text(text2)
        
        # Tokenizar
        tokens1 = self.tokenize_text(text1)
        tokens2 = self.tokenize_text(text2)
        
        # Calcular coeficiente
        coefficient, _, _ = self.calculate_jaccard_coefficient(tokens1, tokens2)
        
        logger.debug(f"Jaccard: tokens1={len(tokens1)}, tokens2={len(tokens2)}, "
                    f"coefficient={coefficient:.4f}")
        
        return float(coefficient)
    
    def analyze_step_by_step(self, text1: str, text2: str) -> Dict[str, Any]:
        """
        Análisis detallado paso a paso con explicación matemática.
        
        Retorna información completa sobre:
        - Conjuntos de tokens generados
        - Intersección y unión
        - Coeficiente calculado
        - Tokens comunes y únicos
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
        
        # Tokenizar
        tokens1 = self.tokenize_text(text1_processed)
        tokens2 = self.tokenize_text(text2_processed)
        
        # Calcular coeficiente con detalles
        coefficient, intersection, union = self.calculate_jaccard_coefficient(
            tokens1, tokens2
        )
        
        # Identificar tokens únicos de cada texto
        unique_to_text1 = tokens1 - tokens2
        unique_to_text2 = tokens2 - tokens1
        
        # Generar explicación detallada
        explanation = self._generate_explanation(
            text1_processed, text2_processed,
            tokens1, tokens2,
            intersection, union,
            unique_to_text1, unique_to_text2,
            coefficient
        )
        
        return {
            "algorithm": self.name,
            "algorithm_type": self.algorithm_type.value,
            "configuration": {
                "mode": "character n-grams" if self.use_char_ngrams else "word tokens",
                "ngram_size": self.ngram_size if self.use_char_ngrams else None,
                "case_sensitive": self.case_sensitive,
                "remove_stopwords": self.remove_stopwords
            },
            "inputs": {
                "text1_original": text1[:100] + "..." if len(text1) > 100 else text1,
                "text2_original": text2[:100] + "..." if len(text2) > 100 else text2,
                "text1_processed": text1_processed[:100] + "..." if len(text1_processed) > 100 else text1_processed,
                "text2_processed": text2_processed[:100] + "..." if len(text2_processed) > 100 else text2_processed
            },
            "tokenization": {
                "tokens_text1": sorted(list(tokens1))[:30],  # Primeros 30 tokens
                "tokens_text2": sorted(list(tokens2))[:30],
                "total_tokens_text1": len(tokens1),
                "total_tokens_text2": len(tokens2)
            },
            "set_operations": {
                "intersection": sorted(list(intersection))[:20],  # Primeros 20
                "intersection_size": len(intersection),
                "union_size": len(union),
                "unique_to_text1": sorted(list(unique_to_text1))[:20],
                "unique_to_text1_size": len(unique_to_text1),
                "unique_to_text2": sorted(list(unique_to_text2))[:20],
                "unique_to_text2_size": len(unique_to_text2)
            },
            "results": {
                "jaccard_coefficient": float(coefficient),
                "jaccard_percentage": f"{coefficient * 100:.2f}%",
                "jaccard_distance": float(1 - coefficient)
            },
            "complexity": {
                "tokenization": f"O(m+n) donde m={len(text1_processed)}, n={len(text2_processed)}",
                "set_operations": f"O(min(|A|,|B|)) = O({min(len(tokens1), len(tokens2))})",
                "total": f"O(m+n) = O({len(text1_processed) + len(text2_processed)})"
            },
            "explanation": explanation
        }
    
    def _generate_explanation(
        self,
        text1: str,
        text2: str,
        tokens1: Set[str],
        tokens2: Set[str],
        intersection: Set[str],
        union: Set[str],
        unique_to_text1: Set[str],
        unique_to_text2: Set[str],
        coefficient: float
    ) -> str:
        """
        Genera explicación matemática detallada en formato Markdown.
        
        Returns:
            Explicación completa en Markdown
        """
        mode = "n-gramas de caracteres" if self.use_char_ngrams else "palabras"
        
        explanation = f"""
# ANÁLISIS DE SIMILITUD CON COEFICIENTE DE JACCARD

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

El **Coeficiente de Jaccard** mide la similitud entre dos conjuntos como el
tamaño de su intersección dividido por el tamaño de su unión.

### Fórmula

Para dos conjuntos A y B:

```
J(A, B) = |A ∩ B| / |A ∪ B|
```

Donde:
- **|A ∩ B|** = Número de elementos en la intersección (comunes a ambos)
- **|A ∪ B|** = Número de elementos en la unión (presentes en al menos uno)

## Paso 1: Tokenización

Modo de tokenización: **{mode}**

"""
        
        if self.use_char_ngrams:
            explanation += f"Tamaño de n-gramas: **{self.ngram_size}** caracteres\n\n"
        
        explanation += f"""
**Conjunto A (Texto 1)**:
- Total de {mode}: {len(tokens1)}
- Ejemplo: {{{', '.join(["'" + t + "'" for t in sorted(list(tokens1))[:10]])}{"..." if len(tokens1) > 10 else ""}}}

**Conjunto B (Texto 2)**:
- Total de {mode}: {len(tokens2)}
- Ejemplo: {{{', '.join(["'" + t + "'" for t in sorted(list(tokens2))[:10]])}{"..." if len(tokens2) > 10 else ""}}}

## Paso 2: Operaciones de Conjuntos

### Intersección (A ∩ B)
Elementos comunes a ambos textos:

"""
        
        if len(intersection) > 0:
            explanation += f"**{len(intersection)} elementos comunes**:\n"
            explanation += f"{{{', '.join(["'" + t + "'" for t in sorted(list(intersection))[:15]])}{"..." if len(intersection) > 15 else ""}}}\n\n"
        else:
            explanation += "**No hay elementos comunes** (conjuntos disjuntos)\n\n"
        
        explanation += f"""
### Unión (A ∪ B)
Todos los elementos únicos presentes en al menos uno de los textos:

**{len(union)} elementos únicos en total**

### Elementos Únicos

**Solo en Texto 1** ({len(unique_to_text1)} elementos):
{{{', '.join(["'" + t + "'" for t in sorted(list(unique_to_text1))[:10]])}{"..." if len(unique_to_text1) > 10 else ""}}}

**Solo en Texto 2** ({len(unique_to_text2)} elementos):
{{{', '.join(["'" + t + "'" for t in sorted(list(unique_to_text2))[:10]])}{"..." if len(unique_to_text2) > 10 else ""}}}

## Paso 3: Cálculo del Coeficiente

```
J(A, B) = |A ∩ B| / |A ∪ B|
        = {len(intersection)} / {len(union)}
        = {coefficient:.6f}
```

## Resultados

- **Coeficiente de Jaccard**: {coefficient:.4f} ({coefficient*100:.2f}%)
- **Distancia de Jaccard**: {1-coefficient:.4f} ({(1-coefficient)*100:.2f}%)
  - Distancia = 1 - Similitud

## Interpretación

Con un coeficiente de Jaccard de **{coefficient*100:.2f}%**:

- ✅ **Muy similares** (>70%) si J > 0.70
- ⚠️ **Moderadamente similares** (30-70%) si 0.30 ≤ J ≤ 0.70
- ❌ **Poco similares** (<30%) si J < 0.30

**Conclusión**: Los textos son **{"muy similares" if coefficient > 0.7 else "moderadamente similares" if coefficient > 0.3 else "poco similares"}**.

### Desglose de Similitud

- **Elementos compartidos**: {len(intersection)}/{len(union)} ({len(intersection)/len(union)*100 if len(union) > 0 else 0:.1f}%)
- **Solo en Texto 1**: {len(unique_to_text1)}/{len(union)} ({len(unique_to_text1)/len(union)*100 if len(union) > 0 else 0:.1f}%)
- **Solo en Texto 2**: {len(unique_to_text2)}/{len(union)} ({len(unique_to_text2)/len(union)*100 if len(union) > 0 else 0:.1f}%)

## Complejidad Algorítmica

- **Tokenización**: O(m + n) donde m = {len(text1)}, n = {len(text2)}
- **Operaciones de conjunto**: O(min(|A|, |B|)) = O({min(len(tokens1), len(tokens2))})
- **Total**: O(m + n) = O({len(text1) + len(text2)})

## Propiedades del Coeficiente de Jaccard

- **Rango**: [0, 1]
- **Simetría**: J(A, B) = J(B, A) ✓
- **Identidad**: J(A, A) = 1 ✓
- **Disjuntos**: J(A, B) = 0 si A ∩ B = ∅
"""
        
        return explanation.strip()
