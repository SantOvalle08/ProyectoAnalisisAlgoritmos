"""
Implementación de BERT Embeddings + Similitud del Coseno
========================================================

BERT (Bidirectional Encoder Representations from Transformers) es un modelo
de lenguaje pre-entrenado que genera representaciones contextualizadas de
palabras y oraciones, capturando relaciones semánticas profundas.

FUNDAMENTO MATEMÁTICO:
=====================

1. **Arquitectura Transformer**:
   - Mecanismo de atención multi-cabeza (Multi-Head Attention)
   - Codificación posicional
   - Feed-forward layers
   - Layer normalization

2. **Pre-entrenamiento Bidireccional**:
   - Masked Language Model (MLM)
   - Next Sentence Prediction (NSP)

3. **Embeddings**:
   - Token embeddings: Representación de cada token
   - Segment embeddings: Diferencia entre oraciones
   - Position embeddings: Información posicional

4. **Extracción de Representación**:
   Dos enfoques principales:
   
   a) **[CLS] Token**: Usar el embedding del token especial [CLS]
      ```
      sentence_embedding = hidden_states[0]  # Primera posición
      ```
   
   b) **Mean Pooling**: Promedio de todos los tokens
      ```
      sentence_embedding = mean(hidden_states[1:])  # Excluir [CLS]
      ```

5. **Similitud del Coseno**:
   ```
   cos(θ) = (A · B) / (||A|| x ||B||)
   ```

VENTAJAS:
- Captura semántica profunda y contexto
- Pre-entrenado en grandes corpus
- Maneja polisemia y ambigüedad
- Funciona bien en múltiples idiomas

DESVENTAJAS:
- Computacionalmente costoso
- Requiere hardware potente (GPU recomendada)
- Modelos grandes (110M+ parámetros)
- Puede ser lento para grandes volúmenes

COMPLEJIDAD:
- Tiempo: O(n²) por el mecanismo de atención
- Espacio: O(n x d) donde d = dimensión del modelo (768 para BERT-base)

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

import torch
from transformers import BertTokenizer, BertModel
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
import logging

from .base_similarity import BaseSimilarity, SimilarityAlgorithmType

logger = logging.getLogger(__name__)


class BERTEmbeddingsSimilarity(BaseSimilarity):
    """
    Implementación de similitud usando BERT Embeddings.
    
    Este algoritmo utiliza el modelo BERT pre-entrenado para generar
    embeddings contextualizados de textos y calcula similitud del coseno
    entre estos embeddings.
    
    Características:
    - Modelo BERT pre-entrenado (bert-base-uncased por defecto)
    - Dos modos de pooling: CLS token o mean pooling
    - Caché de modelo para eficiencia
    - Soporte para GPU si está disponible
    
    Attributes:
        name: "BERT Embeddings + Similitud del Coseno"
        description: Descripción del algoritmo
        algorithm_type: BERT
        model: Modelo BERT cargado
        tokenizer: Tokenizador BERT
        device: Dispositivo de cómputo (cuda o cpu)
        pooling_strategy: 'cls' o 'mean'
    """
    
    def __init__(
        self,
        model_name: str = 'bert-base-uncased',
        pooling_strategy: str = 'mean',
        max_length: int = 512,
        use_gpu: bool = True
    ):
        """
        Inicializa el algoritmo BERT Embeddings.
        
        Args:
            model_name: Nombre del modelo BERT pre-entrenado
                       ('bert-base-uncased', 'bert-large-uncased', etc.)
            pooling_strategy: Estrategia de pooling ('cls' o 'mean')
            max_length: Longitud máxima de secuencia (máx 512 para BERT)
            use_gpu: Si True, usa GPU si está disponible
        """
        super().__init__(
            name=f"BERT Embeddings ({model_name}, {pooling_strategy} pooling)",
            description=f"Similitud semántica profunda con embeddings contextualizados de BERT",
            algorithm_type=SimilarityAlgorithmType.BERT
        )
        
        if pooling_strategy not in ['cls', 'mean']:
            raise ValueError("pooling_strategy debe ser 'cls' o 'mean'")
        
        self.model_name = model_name
        self.pooling_strategy = pooling_strategy
        self.max_length = min(max_length, 512)  # BERT máximo es 512
        
        # Configurar dispositivo (GPU o CPU)
        self.device = torch.device('cuda' if use_gpu and torch.cuda.is_available() else 'cpu')
        
        logger.info(f"Inicializando BERT: modelo={model_name}, dispositivo={self.device}")
        
        try:
            # Cargar tokenizador y modelo
            self.tokenizer = BertTokenizer.from_pretrained(model_name)
            self.model = BertModel.from_pretrained(model_name)
            
            # Mover modelo al dispositivo
            self.model.to(self.device)
            
            # Poner modelo en modo evaluación (desactiva dropout)
            self.model.eval()
            
            logger.info(f"BERT cargado exitosamente en {self.device}")
            
        except Exception as e:
            logger.error(f"Error cargando BERT: {str(e)}")
            raise
    
    def get_embedding(
        self,
        text: str,
        return_attention: bool = False
    ) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Genera embedding BERT para un texto.
        
        Proceso:
        1. Tokenizar texto
        2. Pasar por modelo BERT
        3. Aplicar estrategia de pooling
        4. Retornar embedding normalizado
        
        Args:
            text: Texto para generar embedding
            return_attention: Si True, retorna también los pesos de atención
        
        Returns:
            Tupla (embedding, attention_weights)
            - embedding: Vector numpy de dimensión [hidden_size]
            - attention_weights: Matriz de atención (opcional)
        """
        # Tokenizar
        inputs = self.tokenizer(
            text,
            return_tensors='pt',
            max_length=self.max_length,
            truncation=True,
            padding=True,
            return_attention_mask=True
        )
        
        # Mover inputs al dispositivo
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Inferencia sin gradientes (más eficiente)
        with torch.no_grad():
            outputs = self.model(
                **inputs,
                output_attentions=return_attention
            )
        
        # Extraer hidden states (última capa)
        hidden_states = outputs.last_hidden_state  # [batch_size, seq_len, hidden_size]
        
        # Aplicar estrategia de pooling
        if self.pooling_strategy == 'cls':
            # Usar el token [CLS] (primera posición)
            embedding = hidden_states[:, 0, :].squeeze()
        else:  # mean
            # Promediar todos los tokens (excluyendo padding)
            attention_mask = inputs['attention_mask']
            # Expandir attention_mask para broadcasting
            mask_expanded = attention_mask.unsqueeze(-1).expand(hidden_states.size()).float()
            # Sumar embeddings ponderados por mask
            sum_embeddings = torch.sum(hidden_states * mask_expanded, dim=1)
            # Dividir por número de tokens reales
            sum_mask = torch.clamp(mask_expanded.sum(dim=1), min=1e-9)
            embedding = (sum_embeddings / sum_mask).squeeze()
        
        # Convertir a numpy
        embedding_np = embedding.cpu().numpy()
        
        # Extraer attention weights si se solicitan
        attention_weights = None
        if return_attention and outputs.attentions is not None:
            # Promediar atención de todas las capas y cabezas
            attention_weights = torch.stack(outputs.attentions).mean(dim=(0, 1))
            attention_weights = attention_weights.squeeze().cpu().numpy()
        
        return embedding_np, attention_weights
    
    def calculate_cosine_similarity(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray
    ) -> float:
        """
        Calcula similitud del coseno entre dos embeddings.
        
        Fórmula: cos(θ) = (A · B) / (||A|| × ||B||)
        
        Args:
            embedding1: Primer embedding
            embedding2: Segundo embedding
        
        Returns:
            Similitud del coseno entre -1 y 1
        """
        # Calcular producto punto
        dot_product = np.dot(embedding1, embedding2)
        
        # Calcular normas
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        # Evitar división por cero
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Calcular similitud
        similarity = dot_product / (norm1 * norm2)
        
        # Asegurar rango [-1, 1]
        similarity = np.clip(similarity, -1.0, 1.0)
        
        return float(similarity)
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula similitud entre dos textos usando BERT embeddings.
        
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
        
        # Preprocesar textos
        text1 = self.preprocess_text(text1)
        text2 = self.preprocess_text(text2)
        
        # Caso especial: textos vacíos
        if len(text1) == 0 and len(text2) == 0:
            return 1.0
        if len(text1) == 0 or len(text2) == 0:
            return 0.0
        
        try:
            # Generar embeddings
            embedding1, _ = self.get_embedding(text1)
            embedding2, _ = self.get_embedding(text2)
            
            # Calcular similitud del coseno
            similarity = self.calculate_cosine_similarity(embedding1, embedding2)
            
            # Normalizar de [-1, 1] a [0, 1]
            similarity_normalized = (similarity + 1) / 2
            
            logger.debug(f"BERT similarity: raw={similarity:.4f}, normalized={similarity_normalized:.4f}")
            
            return float(similarity_normalized)
            
        except Exception as e:
            logger.error(f"Error en calculate_similarity: {str(e)}")
            return 0.0
    
    def analyze_step_by_step(self, text1: str, text2: str) -> Dict[str, Any]:
        """
        Análisis detallado paso a paso con explicación completa.
        
        Retorna información sobre:
        - Embeddings generados
        - Tokens procesados
        - Similitud calculada
        - Pesos de atención (visualización)
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
        
        # Tokenizar para obtener información
        tokens1 = self.tokenizer.tokenize(text1_processed)[:self.max_length - 2]
        tokens2 = self.tokenizer.tokenize(text2_processed)[:self.max_length - 2]
        
        # Generar embeddings con atención
        embedding1, attention1 = self.get_embedding(text1_processed, return_attention=True)
        embedding2, attention2 = self.get_embedding(text2_processed, return_attention=True)
        
        # Calcular similitud
        similarity_raw = self.calculate_cosine_similarity(embedding1, embedding2)
        similarity_normalized = (similarity_raw + 1) / 2
        
        # Calcular normas
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        # Calcular producto punto
        dot_product = np.dot(embedding1, embedding2)
        
        # Calcular ángulo
        angle_radians = np.arccos(np.clip(similarity_raw, -1, 1))
        angle_degrees = np.degrees(angle_radians)
        
        # Generar explicación detallada
        explanation = self._generate_explanation(
            text1_processed, text2_processed,
            tokens1, tokens2,
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
                "pooling_strategy": self.pooling_strategy,
                "max_length": self.max_length,
                "device": str(self.device),
                "embedding_dimension": len(embedding1)
            },
            "inputs": {
                "text1_original": text1[:100] + "..." if len(text1) > 100 else text1,
                "text2_original": text2[:100] + "..." if len(text2) > 100 else text2,
                "text1_processed": text1_processed[:100] + "..." if len(text1_processed) > 100 else text1_processed,
                "text2_processed": text2_processed[:100] + "..." if len(text2_processed) > 100 else text2_processed
            },
            "tokenization": {
                "tokens_text1": tokens1[:30],  # Primeros 30 tokens
                "tokens_text2": tokens2[:30],
                "total_tokens_text1": len(tokens1),
                "total_tokens_text2": len(tokens2),
                "truncated_text1": len(tokens1) >= self.max_length - 2,
                "truncated_text2": len(tokens2) >= self.max_length - 2
            },
            "embeddings": {
                "dimension": len(embedding1),
                "text1": {
                    "shape": embedding1.shape,
                    "norm": float(norm1),
                    "sample_values": embedding1[:10].tolist(),  # Primeras 10 dimensiones
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
            "complexity": {
                "attention": f"O(n²) donde n={max(len(tokens1), len(tokens2))} tokens",
                "embedding": f"O(n x d) donde d={len(embedding1)} dimensiones",
                "similarity": "O(d) para producto punto y normas"
            },
            "explanation": explanation
        }
    
    def _generate_explanation(
        self,
        text1: str,
        text2: str,
        tokens1: List[str],
        tokens2: List[str],
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
        Genera explicación matemática detallada en formato Markdown.
        
        Returns:
            Explicación completa en Markdown
        """
        explanation = f"""
# ANÁLISIS DE SIMILITUD CON BERT EMBEDDINGS

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

**BERT** (Bidirectional Encoder Representations from Transformers) genera
representaciones contextualizadas que capturan semántica profunda.

### Arquitectura

- **Modelo**: {self.model_name}
- **Parámetros**: ~110M (base) o ~340M (large)
- **Dimensión de embedding**: {len(embedding1)}
- **Estrategia de pooling**: {self.pooling_strategy}
- **Dispositivo de cómputo**: {self.device}

### Mecanismo de Atención

BERT usa **Multi-Head Self-Attention** para capturar relaciones entre palabras:

```
Attention(Q, K, V) = softmax(QK^T / √d_k) × V
```

Donde:
- Q (Query), K (Key), V (Value) son proyecciones lineales
- d_k = dimensión de las claves
- Softmax normaliza los pesos de atención

## Paso 1: Tokenización

**Texto 1**:
- Tokens: {len(tokens1)}
- Ejemplo: {tokens1[:15]}{"..." if len(tokens1) > 15 else ""}

**Texto 2**:
- Tokens: {len(tokens2)}
- Ejemplo: {tokens2[:15]}{"..." if len(tokens2) > 15 else ""}

## Paso 2: Generación de Embeddings

Cada texto se convierte en un vector denso de {len(embedding1)} dimensiones que
captura su significado semántico en el espacio latente aprendido por BERT.

### Estrategia de Pooling: **{self.pooling_strategy.upper()}**

"""
        
        if self.pooling_strategy == 'cls':
            explanation += """
**[CLS] Token Pooling**:
- Se usa el embedding del token especial [CLS]
- BERT pre-entrena este token para representar la oración completa
- Ubicado en la primera posición del output
"""
        else:
            explanation += """
**Mean Pooling**:
- Se promedian los embeddings de todos los tokens
- Excluye tokens de padding
- Más robusto para textos largos
- Fórmula: embedding = Σ(hidden_states x mask) / Σ(mask)
"""
        
        explanation += f"""

### Estadísticas de Embeddings

**Embedding Texto 1**:
- Norma L2: {norm1:.4f}
- Media: {np.mean(embedding1):.4f}
- Desviación estándar: {np.std(embedding1):.4f}
- Rango: [{np.min(embedding1):.4f}, {np.max(embedding1):.4f}]

**Embedding Texto 2**:
- Norma L2: {norm2:.4f}
- Media: {np.mean(embedding2):.4f}
- Desviación estándar: {np.std(embedding2):.4f}
- Rango: [{np.min(embedding2):.4f}, {np.max(embedding2):.4f}]

## Paso 3: Similitud del Coseno

**Fórmula**:
```
cos(θ) = (A · B) / (||A|| x ||B||)
```

**Cálculo**:
```
Producto punto (A · B) = {dot_product:.6f}
Norma de A (||A||)     = {norm1:.6f}
Norma de B (||B||)     = {norm2:.6f}

cos(θ) = {dot_product:.6f} / ({norm1:.6f} × {norm2:.6f})
       = {dot_product:.6f} / {norm1 * norm2:.6f}
       = {similarity_raw:.6f}
```

## Paso 4: Normalización

BERT puede producir similitudes en rango [-1, 1]. Normalizamos a [0, 1]:

```
similarity_normalized = (cos(θ) + 1) / 2
                      = ({similarity_raw:.6f} + 1) / 2
                      = {similarity_normalized:.6f}
```

## Resultados

- **Similitud del coseno (raw)**: {similarity_raw:.4f}
- **Similitud normalizada**: {similarity_normalized:.4f} ({similarity_normalized*100:.2f}%)
- **Ángulo entre vectores**: {angle_degrees:.2f}°
- **Dimensión del espacio**: {len(embedding1)}D

## Interpretación

Con una similitud de **{similarity_normalized*100:.2f}%**:

- ✅ **Muy similares** (>80%) si similarity > 0.80
- ⚠️ **Moderadamente similares** (50-80%) si 0.50 ≤ similarity ≤ 0.80
- ❌ **Poco similares** (<50%) si similarity < 0.50

**Conclusión**: Los textos son **{"muy similares" if similarity_normalized > 0.8 else "moderadamente similares" if similarity_normalized > 0.5 else "poco similares"}** semánticamente.

## Ventajas de BERT

1. **Semántica Contextual**: Captura significado según contexto
2. **Bidireccional**: Considera palabras anteriores y posteriores
3. **Pre-entrenado**: Aprendió de millones de textos
4. **Polisemia**: Diferencia sentidos de palabras ambiguas
5. **Robustez**: Funciona bien incluso con errores ortográficos

## Complejidad Algorítmica

- **Atención**: O(n² x d) donde n={max(len(tokens1), len(tokens2))}, d={len(embedding1)}
- **Embedding**: O(n x d)
- **Similitud**: O(d)
- **Total por inferencia**: O(n² x d)

**Nota**: BERT es computacionalmente costoso pero proporciona la mejor
comprensión semántica entre todos los algoritmos implementados.
"""
        
        return explanation.strip()
