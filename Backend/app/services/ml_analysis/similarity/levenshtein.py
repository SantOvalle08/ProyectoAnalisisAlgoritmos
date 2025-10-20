"""
Implementación de Distancia de Levenshtein (Edit Distance)
==========================================================

La distancia de Levenshtein es una métrica de similitud entre dos secuencias
de caracteres que mide el número mínimo de operaciones de edición necesarias
para transformar una cadena en otra.

OPERACIONES PERMITIDAS:
- Inserción: Agregar un carácter
- Eliminación: Remover un carácter
- Sustitución: Reemplazar un carácter por otro

FUNDAMENTO MATEMÁTICO:
=====================
Sea s1 y s2 dos cadenas de longitud m y n respectivamente.
Sea DP[i][j] = distancia entre s1[0...i-1] y s2[0...j-1]

Casos base:
- DP[0][j] = j (insertar j caracteres)
- DP[i][0] = i (eliminar i caracteres)

Recurrencia:
DP[i][j] = {
    DP[i-1][j-1]                           si s1[i-1] == s2[j-1]
    1 + min(DP[i-1][j],                    eliminación
            DP[i][j-1],                    inserción
            DP[i-1][j-1])                  sustitución
                                           en caso contrario
}

COMPLEJIDAD:
- Tiempo: O(m x n)
- Espacio: O(m x n) para la matriz DP completa
          O(min(m, n)) con optimización de espacio

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

import numpy as np
from typing import Tuple, List, Dict, Any
import logging

from .base_similarity import BaseSimilarity, SimilarityAlgorithmType

logger = logging.getLogger(__name__)


class LevenshteinSimilarity(BaseSimilarity):
    """
    Implementación de la Distancia de Levenshtein usando Programación Dinámica.
    
    Este algoritmo calcula el número mínimo de operaciones de edición necesarias
    para transformar una cadena en otra, y convierte esta distancia en una
    medida de similitud normalizada.
    
    Attributes:
        name: "Distancia de Levenshtein"
        description: Descripción del algoritmo
        algorithm_type: LEVENSHTEIN
    """
    
    def __init__(self):
        """Inicializa el algoritmo de Levenshtein."""
        super().__init__(
            name="Distancia de Levenshtein (Edit Distance)",
            description="Mide similitud basándose en operaciones de edición (inserción, eliminación, sustitución)",
            algorithm_type=SimilarityAlgorithmType.LEVENSHTEIN
        )
    
    def calculate_distance(
        self, 
        text1: str, 
        text2: str,
        return_matrix: bool = False
    ) -> Tuple[int, np.ndarray]:
        """
        Calcula la distancia de Levenshtein usando programación dinámica.
        
        Algoritmo:
        1. Crear matriz DP de tamaño (m+1) × (n+1)
        2. Inicializar casos base (fila y columna 0)
        3. Llenar matriz usando la recurrencia
        4. Retornar DP[m][n] como la distancia mínima
        
        Args:
            text1: Primer texto
            text2: Segundo texto
            return_matrix: Si True, retorna la matriz DP completa
        
        Returns:
            Tupla (distancia, matriz_dp)
        """
        m, n = len(text1), len(text2)
        
        # Inicializar matriz DP
        dp = np.zeros((m + 1, n + 1), dtype=int)
        
        # Casos base
        for i in range(m + 1):
            dp[i][0] = i  # Eliminar i caracteres
        for j in range(n + 1):
            dp[0][j] = j  # Insertar j caracteres
        
        # Llenar matriz usando programación dinámica
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i-1] == text2[j-1]:
                    # Los caracteres coinciden, no hay costo
                    dp[i][j] = dp[i-1][j-1]
                else:
                    # Tomar el mínimo de las tres operaciones
                    dp[i][j] = 1 + min(
                        dp[i-1][j],      # Eliminación
                        dp[i][j-1],      # Inserción
                        dp[i-1][j-1]     # Sustitución
                    )
        
        distance = dp[m][n]
        return (distance, dp) if return_matrix else (distance, None)
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula similitud normalizada entre dos textos.
        
        Fórmula de normalización:
        similarity = 1 - (distance / max_length)
        
        Donde max_length es la longitud del texto más largo.
        
        Args:
            text1: Primer texto
            text2: Segundo texto
        
        Returns:
            Similitud normalizada entre 0.0 y 1.0
            - 0.0: Completamente diferentes
            - 1.0: Idénticos
        """
        # Validar entradas
        self.validate_inputs(text1, text2)
        
        # Preprocesar textos
        text1 = self.preprocess_text(text1)
        text2 = self.preprocess_text(text2)
        
        # Caso especial: ambos textos vacíos
        if len(text1) == 0 and len(text2) == 0:
            return 1.0
        
        # Calcular distancia
        distance, _ = self.calculate_distance(text1, text2)
        
        # Normalizar por la longitud máxima
        max_len = max(len(text1), len(text2))
        
        if max_len == 0:
            return 1.0
        
        similarity = 1.0 - (distance / max_len)
        
        logger.debug(f"Levenshtein: distance={distance}, max_len={max_len}, similarity={similarity:.4f}")
        
        return float(similarity)
    
    def analyze_step_by_step(self, text1: str, text2: str) -> Dict[str, Any]:
        """
        Análisis detallado paso a paso con explicación matemática completa.
        
        Este método retorna:
        - Distancia de Levenshtein
        - Similitud normalizada
        - Matriz de programación dinámica completa
        - Secuencia de operaciones de edición
        - Explicación matemática detallada
        - Análisis de complejidad
        
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
        
        # Calcular distancia con matriz completa
        distance, dp_matrix = self.calculate_distance(
            text1_processed, text2_processed, return_matrix=True
        )
        
        # Calcular similitud
        max_len = max(len(text1_processed), len(text2_processed))
        similarity = 1.0 - (distance / max_len) if max_len > 0 else 1.0
        
        # Reconstruir secuencia de operaciones
        operations = self._reconstruct_operations(
            text1_processed, text2_processed, dp_matrix
        )
        
        # Generar explicación detallada
        explanation = self._generate_explanation(
            text1_processed, text2_processed, distance, similarity, operations
        )
        
        # Contar tipos de operaciones
        operation_counts = {
            "insert": sum(1 for op in operations if op["type"] == "insert"),
            "delete": sum(1 for op in operations if op["type"] == "delete"),
            "substitute": sum(1 for op in operations if op["type"] == "substitute"),
            "match": sum(1 for op in operations if op["type"] == "match")
        }
        
        return {
            "algorithm": self.name,
            "algorithm_type": self.algorithm_type.value,
            "inputs": {
                "text1_original": text1[:100] + "..." if len(text1) > 100 else text1,
                "text2_original": text2[:100] + "..." if len(text2) > 100 else text2,
                "text1_processed": text1_processed[:100] + "..." if len(text1_processed) > 100 else text1_processed,
                "text2_processed": text2_processed[:100] + "..." if len(text2_processed) > 100 else text2_processed,
                "length1": len(text1_processed),
                "length2": len(text2_processed)
            },
            "results": {
                "distance": int(distance),
                "similarity": float(similarity),
                "similarity_percentage": f"{similarity * 100:.2f}%",
                "max_length": max_len
            },
            "operations": {
                "total_edits": distance,
                "sequence": operations[:20],  # Primeras 20 operaciones
                "counts": operation_counts,
                "efficiency": f"{operation_counts['match']}/{len(operations)} caracteres coinciden"
            },
            "dp_matrix": {
                "shape": f"{dp_matrix.shape[0]}×{dp_matrix.shape[1]}",
                "matrix": dp_matrix.tolist() if dp_matrix.shape[0] <= 20 and dp_matrix.shape[1] <= 20 else "Matriz muy grande para mostrar completa",
                "final_value": int(dp_matrix[-1, -1])
            },
            "complexity": {
                "time": f"O(m×n) = O({len(text1_processed)}×{len(text2_processed)}) = O({len(text1_processed) * len(text2_processed)})",
                "space": f"O(m×n) = O({len(text1_processed) * len(text2_processed)}) para matriz completa"
            },
            "explanation": explanation
        }
    
    def _reconstruct_operations(
        self, 
        text1: str, 
        text2: str, 
        dp: np.ndarray
    ) -> List[Dict[str, Any]]:
        """
        Reconstruye la secuencia de operaciones de edición óptima.
        
        Algoritmo de backtracking desde DP[m][n] hasta DP[0][0]:
        1. Si caracteres coinciden: match
        2. Si no coinciden, elegir operación que dio el mínimo costo
        
        Args:
            text1: Primer texto
            text2: Segundo texto
            dp: Matriz de programación dinámica
        
        Returns:
            Lista de operaciones en orden de aplicación
        """
        operations = []
        i, j = len(text1), len(text2)
        
        while i > 0 or j > 0:
            if i == 0:
                # Solo quedan inserciones
                operations.append({
                    "type": "insert",
                    "char": text2[j-1],
                    "position": j-1,
                    "description": f"Insertar '{text2[j-1]}' en posición {j-1}"
                })
                j -= 1
            elif j == 0:
                # Solo quedan eliminaciones
                operations.append({
                    "type": "delete",
                    "char": text1[i-1],
                    "position": i-1,
                    "description": f"Eliminar '{text1[i-1]}' de posición {i-1}"
                })
                i -= 1
            elif text1[i-1] == text2[j-1]:
                # Caracteres coinciden
                operations.append({
                    "type": "match",
                    "char": text1[i-1],
                    "position": i-1,
                    "description": f"Caracteres coinciden: '{text1[i-1]}'"
                })
                i -= 1
                j -= 1
            else:
                # Determinar operación óptima
                delete_cost = dp[i-1][j]
                insert_cost = dp[i][j-1]
                substitute_cost = dp[i-1][j-1]
                
                min_cost = min(delete_cost, insert_cost, substitute_cost)
                
                if min_cost == substitute_cost:
                    operations.append({
                        "type": "substitute",
                        "from_char": text1[i-1],
                        "to_char": text2[j-1],
                        "position": i-1,
                        "description": f"Sustituir '{text1[i-1]}' por '{text2[j-1]}' en posición {i-1}"
                    })
                    i -= 1
                    j -= 1
                elif min_cost == delete_cost:
                    operations.append({
                        "type": "delete",
                        "char": text1[i-1],
                        "position": i-1,
                        "description": f"Eliminar '{text1[i-1]}' de posición {i-1}"
                    })
                    i -= 1
                else:
                    operations.append({
                        "type": "insert",
                        "char": text2[j-1],
                        "position": j-1,
                        "description": f"Insertar '{text2[j-1]}' en posición {j-1}"
                    })
                    j -= 1
        
        return list(reversed(operations))
    
    def _generate_explanation(
        self,
        text1: str,
        text2: str,
        distance: int,
        similarity: float,
        operations: List[Dict]
    ) -> str:
        """
        Genera explicación matemática detallada en formato Markdown.
        
        Args:
            text1: Primer texto
            text2: Segundo texto
            distance: Distancia calculada
            similarity: Similitud normalizada
            operations: Lista de operaciones
        
        Returns:
            Explicación en formato Markdown
        """
        # Contar operaciones de edición (excluir matches)
        edit_ops = [op for op in operations if op['type'] != 'match']
        
        explanation = f"""
# ANÁLISIS DE SIMILITUD CON DISTANCIA DE LEVENSHTEIN

## Textos Analizados

**Texto 1** (longitud: {len(text1)}):
```
{text1[:200]}{"..." if len(text1) > 200 else ""}
```

**Texto 2** (longitud: {len(text2)}):
```
{text2[:200]}{"..." if len(text2) > 200 else ""}
```

## Fundamento Matemático

La **Distancia de Levenshtein** mide el número mínimo de operaciones de edición
necesarias para transformar una cadena en otra.

### Fórmula de Programación Dinámica

Sea `DP[i][j]` la distancia entre `text1[0...i-1]` y `text2[0...j-1]`:

```
DP[i][j] = {{
    DP[i-1][j-1]                    si text1[i-1] == text2[j-1]
    1 + min(DP[i-1][j],             eliminación
            DP[i][j-1],             inserción
            DP[i-1][j-1])           sustitución
}}
```

## Resultados

- **Distancia de Levenshtein**: {distance}
- **Similitud normalizada**: {similarity:.4f} ({similarity*100:.2f}%)
- **Longitud máxima**: {max(len(text1), len(text2))}

### Fórmula de Normalización

```
similarity = 1 - (distance / max_length)
           = 1 - ({distance} / {max(len(text1), len(text2))})
           = {similarity:.4f}
```

## Operaciones Necesarias ({len(edit_ops)} ediciones)

Las primeras 10 operaciones de edición:

"""
        
        # Mostrar primeras 10 operaciones de edición
        edit_count = 0
        for i, op in enumerate(operations[:30], 1):
            if op['type'] != 'match' and edit_count < 10:
                edit_count += 1
                if op['type'] == 'substitute':
                    explanation += f"{edit_count}. **Sustituir** '{op['from_char']}' → '{op['to_char']}' (pos {op['position']})\n"
                elif op['type'] == 'insert':
                    explanation += f"{edit_count}. **Insertar** '{op['char']}' (pos {op['position']})\n"
                elif op['type'] == 'delete':
                    explanation += f"{edit_count}. **Eliminar** '{op['char']}' (pos {op['position']})\n"
        
        if len(edit_ops) > 10:
            explanation += f"\n... y {len(edit_ops) - 10} operaciones más.\n"
        
        explanation += f"""

## Interpretación

Con una similitud del **{similarity*100:.2f}%**, los textos son:
- ✅ **Muy similares** (>90%) si similarity > 0.90
- ⚠️ **Moderadamente similares** (50-90%) si 0.50 ≤ similarity ≤ 0.90
- ❌ **Poco similares** (<50%) si similarity < 0.50

**Conclusión**: Los textos son **{"muy similares" if similarity > 0.9 else "moderadamente similares" if similarity > 0.5 else "poco similares"}**.

## Complejidad Algorítmica

- **Tiempo**: O(m × n) = O({len(text1)} × {len(text2)}) = O({len(text1) * len(text2)})
- **Espacio**: O(m × n) para la matriz DP completa
"""
        
        return explanation.strip()
