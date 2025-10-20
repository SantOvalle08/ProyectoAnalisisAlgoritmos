"""
Implementación de Sentence-BERT (SBERT) para Similitud Semántica
================================================================

Sentence-BERT es una modificación de BERT optimizada específicamente para
generar embeddings de oraciones de alta calidad usando redes siamesas y
triplet networks.

DIFERENCIAS CON BERT ESTÁNDAR:
==============================

**BERT Estándar**:
- Diseñado para tareas de clasificación de pares
- Requiere pasar ambos textos juntos
- Lento para comparaciones masivas (O(n²) comparaciones)
- No optimizado para similitud semántica

**Sentence-BERT**:
- Optimizado para generar embeddings independientes
- Cada texto se procesa separadamente
- Rápido para comparaciones masivas (O(n) generación + O(1) comparación)
- Fine-tuned en datasets de similitud semántica (NLI, STSb)

FUNDAMENTO MATEMÁTICO:
=====================

1. **Arquitectura Siamesa/Triplet**:
   ```
   BERT → Pooling → Normalize → Embedding
   ```

2. **Función de Pérdida**:
   - **Softmax Loss**: Para clasificación de similitud
   - **Triplet Loss**: Para optimizar distancia entre embeddings
   ```
   L = max(0, ||a - p||² - ||a - n||² + margin)
   ```
   Donde: a=anchor, p=positive, n=negative

3. **Pooling Strategies**:
   - **CLS-token**: Usar [CLS]
   - **Mean**: Promedio de todos los tokens
   - **Max**: Valor máximo por dimensión

4. **Similitud**:
   ```
   cos(u, v) = (u · v) / (||u|| x ||v||)
   ```

MODELOS DISPONIBLES:
===================

1. **all-MiniLM-L6-v2**: 
   - Rápido y eficiente (23M parámetros)
   - 384 dimensiones
   - Bueno para casos generales

2. **all-mpnet-base-v2**:
   - Mejor calidad (110M parámetros)
   - 768 dimensiones
   - Mejor rendimiento en benchmarks

3. **paraphrase-multilingual-MiniLM-L12-v2**:
   - Soporte multilingüe
   - 384 dimensiones

VENTAJAS:
- 5-10x más rápido que BERT para similitud
- Embeddings de alta calidad
- Fácil de usar (una línea para encode)
- Optimizado para tareas de similitud

COMPLEJIDAD:
- Tiempo: O(n) por texto (vs O(n²) para pares en BERT)
- Espacio: O(d) donde d = dimensión del modelo

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Dict, Any, List, Optional
import logging

from .base_similarity import BaseSimilarity, SimilarityAlgorithmType

logger = logging.getLogger(__name__)


class SentenceBERTSimilarity(BaseSimilarity):
    """
    Implementación de similitud usando Sentence-BERT (SBERT).
    
    SBERT es una modificación de BERT que produce embeddings semánticamente
    significativos que pueden compararse usando similitud del coseno de
    manera eficiente.
    
    Características:
    - Modelos pre-entrenados optimizados para similitud
    - Inferencia rápida (5-10x más rápido que BERT estándar)
    - Embeddings normalizados listos para usar
    - Soporte multilingüe opcional
    
    Attributes:
        name: "Sentence-BERT"
        description: Descripción del algoritmo
        algorithm_type: SENTENCE_BERT
        model: Modelo SBERT cargado
        embedding_dimension: Dimensión de los embeddings
    """
    
    def __init__(
        self,
        model_name: str = 'all-MiniLM-L6-v2',
        normalize_embeddings: bool = True,
        device: Optional[str] = None
    ):
        """
        Inicializa Sentence-BERT.
        
        Args:
            model_name: Nombre del modelo pre-entrenado
                - 'all-MiniLM-L6-v2': Rápido, 384 dim (recomendado)
                - 'all-mpnet-base-v2': Alta calidad, 768 dim
                - 'paraphrase-multilingual-MiniLM-L12-v2': Multilingüe, 384 dim
            normalize_embeddings: Si True, normaliza embeddings a norma 1
            device: 'cuda', 'cpu' o None (auto-detectar)
        """
        super().__init__(
            name=f"Sentence-BERT ({model_name})",
            description="Embeddings optimizados para similitud semántica con redes siamesas",
            algorithm_type=SimilarityAlgorithmType.SENTENCE_BERT
        )
        
        self.model_name = model_name
        self.normalize_embeddings = normalize_embeddings
        
        logger.info(f"Inicializando Sentence-BERT: modelo={model_name}")
        
        try:
            # Cargar modelo (descarga automática si no existe)
            self.model = SentenceTransformer(model_name, device=device)
            
            # Obtener dimensión de embeddings
            self.embedding_dimension = self.model.get_sentence_embedding_dimension()
            
            # Obtener dispositivo
            self.device = self.model.device
            
            logger.info(
                f"Sentence-BERT cargado: dim={self.embedding_dimension}, "
                f"device={self.device}"
            )
            
        except Exception as e:
            logger.error(f"Error cargando Sentence-BERT: {str(e)}")
            raise
    
    def get_embedding(
        self,
        text: str,
        show_progress_bar: bool = False
    ) -> np.ndarray:
        """
        Genera embedding SBERT para un texto.
        
        SBERT hace todo el trabajo pesado internamente:
        1. Tokeniza el texto
        2. Pasa por el modelo transformer
        3. Aplica pooling (mean por defecto)
        4. Normaliza (si normalize_embeddings=True)
        
        Args:
            text: Texto para generar embedding
            show_progress_bar: Mostrar barra de progreso
        
        Returns:
            Embedding numpy de dimensión [embedding_dimension]
        """
        # Generar embedding usando el modelo
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize_embeddings,
            show_progress_bar=show_progress_bar
        )
        
        return embedding
    
    def get_embeddings_batch(
        self,
        texts: List[str],
        batch_size: int = 32,
        show_progress_bar: bool = False
    ) -> np.ndarray:
        """
        Genera embeddings para múltiples textos eficientemente.
        
        Usa procesamiento por lotes para optimizar GPU/CPU.
        
        Args:
            texts: Lista de textos
            batch_size: Tamaño de lote para procesamiento
            show_progress_bar: Mostrar progreso
        
        Returns:
            Matriz numpy de forma [len(texts), embedding_dimension]
        """
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize_embeddings,
            show_progress_bar=show_progress_bar
        )
        
        return embeddings
    
    def calculate_cosine_similarity(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray
    ) -> float:
        """
        Calcula similitud del coseno entre embeddings.
        
        Si los embeddings están normalizados, el cálculo se simplifica a
        un producto punto (más eficiente).
        
        Args:
            embedding1: Primer embedding
            embedding2: Segundo embedding
        
        Returns:
            Similitud del coseno entre -1 y 1
        """
        if self.normalize_embeddings:
            # Si están normalizados, coseno = producto punto
            similarity = np.dot(embedding1, embedding2)
        else:
            # Cálculo estándar
            dot_product = np.dot(embedding1, embedding2)
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
        
        # Asegurar rango [-1, 1]
        similarity = np.clip(similarity, -1.0, 1.0)
        
        return float(similarity)
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula similitud entre dos textos usando Sentence-BERT.
        
        Proceso:
        1. Generar embedding para texto 1
        2. Generar embedding para texto 2
        3. Calcular similitud del coseno
        4. Normalizar a [0, 1]
        
        Args:
            text1: Primer texto
            text2: Segundo texto
        
        Returns:
            Similitud entre 0.0 y 1.0
        """
        # Validar entradas
        self.validate_inputs(text1, text2)
        
        # Preprocesar
        text1 = self.preprocess_text(text1)
        text2 = self.preprocess_text(text2)
        
        # Caso especial: textos vacíos
        if len(text1) == 0 and len(text2) == 0:
            return 1.0
        if len(text1) == 0 or len(text2) == 0:
            return 0.0
        
        try:
            # Generar embeddings (puede hacerse en batch para eficiencia)
            embeddings = self.get_embeddings_batch([text1, text2])
            embedding1 = embeddings[0]
            embedding2 = embeddings[1]
            
            # Calcular similitud
            similarity = self.calculate_cosine_similarity(embedding1, embedding2)
            
            # Normalizar de [-1, 1] a [0, 1]
            similarity_normalized = (similarity + 1) / 2
            
            logger.debug(f"SBERT similarity: raw={similarity:.4f}, normalized={similarity_normalized:.4f}")
            
            return float(similarity_normalized)
            
        except Exception as e:
            logger.error(f"Error en calculate_similarity: {str(e)}")
            return 0.0
    
    def analyze_step_by_step(self, text1: str, text2: str) -> Dict[str, Any]:
        """
        Análisis detallado paso a paso con explicación completa.
        
        Retorna información sobre:
        - Embeddings generados
        - Similitud calculada
        - Comparación con BERT estándar
        - Ventajas de eficiencia
        - Explicación matemática
        
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
        
        # Generar embeddings
        embeddings = self.get_embeddings_batch([text1_processed, text2_processed])
        embedding1 = embeddings[0]
        embedding2 = embeddings[1]
        
        # Calcular similitud
        similarity_raw = self.calculate_cosine_similarity(embedding1, embedding2)
        similarity_normalized = (similarity_raw + 1) / 2
        
        # Calcular normas (para embeddings no normalizados)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        # Calcular producto punto
        dot_product = np.dot(embedding1, embedding2)
        
        # Calcular ángulo
        angle_radians = np.arccos(np.clip(similarity_raw, -1, 1))
        angle_degrees = np.degrees(angle_radians)
        
        # Generar explicación
        explanation = self._generate_explanation(
            text1_processed, text2_processed,
            embedding1, embedding2,
            dot_product, norm1, norm2,
            similarity_raw, similarity_normalized,
            angle_degrees
        )
        
        return {
            "algorithm": self.name,
            "algorithm_type": self.algorithm_type.value,
            "configuration": {
                "model": self.model_name,
                "embedding_dimension": self.embedding_dimension,
                "normalize_embeddings": self.normalize_embeddings,
                "device": str(self.device),
                "max_seq_length": self.model.max_seq_length
            },
            "inputs": {
                "text1_original": text1[:100] + "..." if len(text1) > 100 else text1,
                "text2_original": text2[:100] + "..." if len(text2) > 100 else text2,
                "text1_processed": text1_processed[:100] + "..." if len(text1_processed) > 100 else text1_processed,
                "text2_processed": text2_processed[:100] + "..." if len(text2_processed) > 100 else text2_processed
            },
            "embeddings": {
                "dimension": self.embedding_dimension,
                "normalized": self.normalize_embeddings,
                "text1": {
                    "shape": embedding1.shape,
                    "norm": float(norm1),
                    "sample_values": embedding1[:10].tolist(),
                    "statistics": {
                        "mean": float(np.mean(embedding1)),
                        "std": float(np.std(embedding1)),
                        "min": float(np.min(embedding1)),
                        "max": float(np.max(embedding1))
                    }
                },
                "text2": {
                    "shape": embedding2.shape,
                    "norm": float(norm2),
                    "sample_values": embedding2[:10].tolist(),
                    "statistics": {
                        "mean": float(np.mean(embedding2)),
                        "std": float(np.std(embedding2)),
                        "min": float(np.min(embedding2)),
                        "max": float(np.max(embedding2))
                    }
                }
            },
            "results": {
                "dot_product": float(dot_product),
                "similarity_raw": float(similarity_raw),
                "similarity_normalized": float(similarity_normalized),
                "similarity_percentage": f"{similarity_normalized * 100:.2f}%",
                "angle_radians": float(angle_radians),
                "angle_degrees": float(angle_degrees)
            },
            "performance": {
                "inference_mode": "batch",
                "suitable_for_large_scale": True,
                "speedup_vs_bert": "5-10x más rápido",
                "complexity": f"O(n) por texto, n={len(text1_processed.split())}"
            },
            "explanation": explanation
        }
    
    def _generate_explanation(
        self,
        text1: str,
        text2: str,
        embedding1: np.ndarray,
        embedding2: np.ndarray,
        dot_product: float,
        norm1: float,
        norm2: float,
        similarity_raw: float,
        similarity_normalized: float,
        angle_degrees: float
    ) -> str:
        """
        Genera explicación detallada en formato Markdown.
        
        Returns:
            Explicación completa en Markdown
        """
        explanation = f"""
# ANÁLISIS DE SIMILITUD CON SENTENCE-BERT

## Textos Analizados

**Texto 1**:
```
{text1[:200]}{"..." if len(text1) > 200 else ""}
```

**Texto 2**:
```
{text2[:200]}{"..." if len(text2) > 200 else ""}
```

## ¿Qué es Sentence-BERT?

**Sentence-BERT (SBERT)** es una modificación de BERT que utiliza
**redes siamesas (Siamese Networks)** y **triplet networks** para
generar embeddings de oraciones semánticamente significativos.

### Diferencias Clave vs BERT Estándar

| Aspecto | BERT Estándar | Sentence-BERT |
|---------|---------------|---------------|
| **Objetivo** | Clasificación de pares | Embeddings de similitud |
| **Procesamiento** | Ambos textos juntos | Cada texto independiente |
| **Velocidad** | Lento (O(n²) pares) | Rápido (O(n) textos) |
| **Optimización** | Tareas generales | Fine-tuned en similitud |
| **Uso** | Clasificación, Q&A | Búsqueda semántica, clustering |

### Arquitectura

```
Input Text → BERT Transformer → Mean Pooling → L2 Normalize → Embedding
```

- **Modelo**: {self.model_name}
- **Dimensión**: {self.embedding_dimension}
- **Normalización**: {"Sí (norma=1)" if self.normalize_embeddings else "No"}
- **Dispositivo**: {self.device}
- **Max seq length**: {self.model.max_seq_length}

### Entrenamiento con Triplet Loss

SBERT se entrena con **triplet loss** para optimizar las distancias:

```
L = max(0, ||anchor - positive||² - ||anchor - negative||² + margin)
```

Esto asegura que:
- Textos similares (anchor, positive) → distancia pequeña
- Textos diferentes (anchor, negative) → distancia grande

## Paso 1: Generación de Embeddings

Cada texto se convierte en un vector denso de {self.embedding_dimension} dimensiones.

### Embedding Texto 1

- **Dimensión**: {embedding1.shape}
- **Norma L2**: {norm1:.4f}
- **Media**: {np.mean(embedding1):.4f}
- **Desv. Estándar**: {np.std(embedding1):.4f}
- **Rango**: [{np.min(embedding1):.4f}, {np.max(embedding1):.4f}]

**Muestra** (primeras 10 dimensiones):
```
{np.array2string(embedding1[:10], precision=4, separator=', ')}
```

### Embedding Texto 2

- **Dimensión**: {embedding2.shape}
- **Norma L2**: {norm2:.4f}
- **Media**: {np.mean(embedding2):.4f}
- **Desv. Estándar**: {np.std(embedding2):.4f}
- **Rango**: [{np.min(embedding2):.4f}, {np.max(embedding2):.4f}]

**Muestra** (primeras 10 dimensiones):
```
{np.array2string(embedding2[:10], precision=4, separator=', ')}
```

## Paso 2: Similitud del Coseno

### Fórmula

"""
        
        if self.normalize_embeddings:
            explanation += """
**Para embeddings normalizados** (norma = 1):
```
cos(θ) = u · v
```

La similitud del coseno se reduce a un simple producto punto, haciendo
el cálculo extremadamente eficiente.
"""
        else:
            explanation += """
**Fórmula estándar**:
```
cos(θ) = (A · B) / (||A|| x ||B||)
```
"""
        
        explanation += f"""

### Cálculo

```
Producto punto (A · B) = {dot_product:.6f}
"""
        
        if not self.normalize_embeddings:
            explanation += f"""Norma de A (||A||)     = {norm1:.6f}
Norma de B (||B||)     = {norm2:.6f}

cos(θ) = {dot_product:.6f} / ({norm1:.6f} x {norm2:.6f})
       = {dot_product:.6f} / {norm1 * norm2:.6f}
       = {similarity_raw:.6f}
"""
        else:
            explanation += f"""
cos(θ) = {similarity_raw:.6f}  (producto punto directo)
"""
        
        explanation += f"""```

## Paso 3: Normalización

Normalizamos de [-1, 1] a [0, 1]:

```
similarity = (cos(θ) + 1) / 2
           = ({similarity_raw:.6f} + 1) / 2
           = {similarity_normalized:.6f}
```

## Resultados

- **Similitud del coseno (raw)**: {similarity_raw:.4f}
- **Similitud normalizada**: {similarity_normalized:.4f}
- **Porcentaje**: **{similarity_normalized*100:.2f}%**
- **Ángulo entre vectores**: {angle_degrees:.2f}°
- **Dimensión del espacio**: {self.embedding_dimension}D

## Interpretación

Con una similitud de **{similarity_normalized*100:.2f}%**:

"""
        
        if similarity_normalized > 0.8:
            interpretation = "✅ **MUY SIMILARES**"
            detail = "Los textos son semánticamente muy cercanos. Probablemente expresan ideas casi idénticas con palabras diferentes."
        elif similarity_normalized > 0.6:
            interpretation = "⚠️ **MODERADAMENTE SIMILARES**"
            detail = "Los textos comparten temática o conceptos relacionados, pero tienen diferencias significativas."
        elif similarity_normalized > 0.4:
            interpretation = "⚡ **PARCIALMENTE SIMILARES**"
            detail = "Los textos tienen alguna relación semántica pero son mayormente diferentes."
        else:
            interpretation = "❌ **POCO SIMILARES**"
            detail = "Los textos son semánticamente distintos, tratando temas diferentes."
        
        explanation += f"""
{interpretation}

{detail}

## Ventajas de Sentence-BERT

### 1. **Velocidad**
- **5-10x más rápido** que BERT estándar para similitud
- Genera embeddings independientemente (O(n) en lugar de O(n²))
- Ideal para búsqueda semántica en grandes corpus

### 2. **Calidad**
- Fine-tuned específicamente en datasets de similitud semántica
- Pre-entrenado en: NLI (Natural Language Inference), STSb (Semantic Textual Similarity)
- Mejor rendimiento que BERT base en tareas de similitud

### 3. **Eficiencia**
- Embeddings se pueden pre-calcular y almacenar
- Comparaciones posteriores son instantáneas (producto punto)
- Escalable a millones de textos

### 4. **Facilidad de Uso**
- API simple: `model.encode(text)`
- No requiere fine-tuning adicional
- Múltiples modelos pre-entrenados disponibles

## Caso de Uso: Bibliometría

Para análisis bibliométrico, SBERT es ideal porque:

1. **Abstracts similares**: Identifica papers relacionados semánticamente
2. **Detección de duplicados**: Encuentra papers redundantes aunque usen términos diferentes
3. **Clustering**: Agrupa papers por temas automáticamente
4. **Búsqueda semántica**: Encuentra papers relevantes sin keywords exactas

## Complejidad Algorítmica

- **Generación de embedding**: O(n) donde n = longitud del texto
- **Similitud del coseno**: O(d) donde d = {self.embedding_dimension}
- **Total por comparación**: O(n₁ + n₂ + d)

**Nota**: En práctica, n₁ y n₂ son pequeños (cientos de tokens) mientras
que d es fijo ({self.embedding_dimension}), haciendo SBERT muy eficiente.

## Modelos Recomendados

| Modelo | Params | Dim | Velocidad | Calidad | Uso |
|--------|--------|-----|-----------|---------|-----|
| all-MiniLM-L6-v2 | 23M | 384 | Muy rápido | Buena | General |
| all-mpnet-base-v2 | 110M | 768 | Rápido | Excelente | Alta precisión |
| paraphrase-multilingual | 118M | 384 | Rápido | Buena | Multilingüe |

**Modelo actual**: {self.model_name}

## Conclusión

Sentence-BERT proporciona el mejor balance entre **velocidad** y **calidad**
para tareas de similitud semántica. Es la opción recomendada para
aplicaciones en producción que requieren comparaciones a gran escala.
"""
        
        return explanation.strip()
