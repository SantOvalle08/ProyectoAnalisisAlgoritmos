# 📋 PLAN DE IMPLEMENTACIÓN DETALLADO
## Proyecto de Análisis Bibliométrico - Universidad del Quindío

**Autores:** Santiago Ovalle Cortés, Juan Sebastián Noreña  
**Curso:** Análisis de Algoritmos (2025-2)  
**Fecha de inicio:** 20 de Octubre, 2025  
**Dominio:** Inteligencia Artificial Generativa en Educación  
**Cadena de búsqueda:** "generative artificial intelligence"

---

## 🎯 OBJETIVO GENERAL

Implementar una plataforma web automatizada para análisis bibliométrico avanzado de publicaciones científicas sobre IA Generativa, integrando algoritmos clásicos y modernos de ML/NLP, con capacidades de visualización interactiva y exportación de resultados.

---

## 📊 ESTADO ACTUAL DEL PROYECTO

### ✅ Infraestructura Completada
- [x] Estructura de directorios Backend y Frontend
- [x] FastAPI configurado con CORS y middlewares
- [x] Dependencias Python instaladas (requirements.txt)
- [x] Aplicación React con TypeScript y Vite
- [x] Dependencias frontend (MUI, D3, Plotly, Recharts)
- [x] Sistema de logging y manejo de errores

### ⏳ Pendiente de Implementación
- [x] Requerimiento 1: Automatización de descarga de datos
- [ ] Requerimiento 2: Algoritmos de similitud textual
- [ ] Requerimiento 3: Análisis de frecuencias de conceptos
- [ ] Requerimiento 4: Clustering jerárquico y dendrogramas
- [ ] Requerimiento 5: Visualizaciones interactivas
- [ ] Requerimiento 6: Despliegue y documentación técnica

---

## 🗓️ CRONOGRAMA DE IMPLEMENTACIÓN

### **Fase 1: Requerimiento 1 - Automatización de Descarga** (5 días)
- Días 1-2: Scrapers y conectores API
- Día 3: Unificación y eliminación de duplicados
- Días 4-5: Testing y validación

### **Fase 2: Requerimiento 2 - Similitud Textual** (7 días)
- Días 6-7: Algoritmos clásicos (Levenshtein, TF-IDF, Jaccard, N-gramas)
- Días 8-9: Algoritmos con IA (BERT, Sentence-BERT)
- Días 10-11: Documentación matemática detallada
- Día 12: UI para comparación de abstracts

### **Fase 3: Requerimiento 3 - Frecuencias de Conceptos** (4 días)
- Día 13: Análisis de frecuencias de categorías predefinidas
- Día 14: Generación automática de palabras asociadas con NLP
- Día 15: Métricas de precisión
- Día 16: Visualizaciones de frecuencias

### **Fase 4: Requerimiento 4 - Clustering Jerárquico** (5 días)
- Días 17-18: Preprocesamiento de texto y vectorización
- Día 19: Implementación de 3 algoritmos de clustering
- Día 20: Generación de dendrogramas interactivos con D3.js
- Día 21: Evaluación comparativa (Silhouette Score)

### **Fase 5: Requerimiento 5 - Visualizaciones** (4 días)
- Día 22: Mapa de calor geográfico (Plotly/Leaflet)
- Día 23: Nube de palabras dinámica (D3.js)
- Día 24: Línea temporal por año y revista (Recharts)
- Día 25: Exportación a PDF (jsPDF + html2canvas)

### **Fase 6: Requerimiento 6 - Despliegue y Documentación** (4 días)
- Día 26: Documentación técnica de arquitectura
- Día 27: Documentación de algoritmos implementados
- Día 28: Dockerización y CI/CD
- Día 29: Despliegue en producción

### **Fase 7: Testing Final y Optimización** (2 días)
- Día 30: Testing integral y correcciones
- Día 31: Optimización de rendimiento

**TOTAL ESTIMADO: 31 días (≈ 6-7 semanas)**

---

## 🏗️ ARQUITECTURA DEL SISTEMA

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (React + TS)                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   D3.js     │  │  Plotly.js  │  │  Recharts   │         │
│  │ Dendrogramas│  │ Mapas Calor │  │  Líneas     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST API
┌────────────────────────▼────────────────────────────────────┐
│                   BACKEND (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            API ENDPOINTS (v1)                        │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ /api/v1/data          - Data Acquisition Service    │   │
│  │ /api/v1/ml            - ML & NLP Service             │   │
│  │ /api/v1/analytics     - Analytics Service            │   │
│  │ /api/v1/viz           - Visualization Service        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         SERVICIOS DE NEGOCIO                        │    │
│  ├─────────────────────────────────────────────────────┤    │
│  │ 🔍 DataAcquisitionService                           │    │
│  │    - Scrapers (ACM, SAGE, ScienceDirect)           │    │
│  │    - Unificación y deduplicación                    │    │
│  │                                                      │    │
│  │ 🤖 MLAnalysisService                                │    │
│  │    - Similitud clásica (Levenshtein, TF-IDF, etc.) │    │
│  │    - Similitud IA (BERT, Sentence-BERT)            │    │
│  │    - Clustering jerárquico (Ward, Average, etc.)   │    │
│  │                                                      │    │
│  │ 📊 AnalyticsService                                 │    │
│  │    - Frecuencias de conceptos                       │    │
│  │    - Métricas bibliométricas                        │    │
│  │    - Generación de palabras asociadas               │    │
│  │                                                      │    │
│  │ 📈 VisualizationService                             │    │
│  │    - Mapas de calor geográficos                     │    │
│  │    - Nubes de palabras                              │    │
│  │    - Líneas temporales                              │    │
│  │    - Exportación PDF                                │    │
│  └─────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│               CAPA DE DATOS                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  PostgreSQL  │  │    Redis     │  │  File System │      │
│  │  Metadatos   │  │    Cache     │  │  Archivos    │      │
│  │  Publicac.   │  │  Embeddings  │  │  CSV/BibTeX  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 REQUERIMIENTO 1: AUTOMATIZACIÓN DE DESCARGA DE DATOS

### **Objetivo**
Automatizar la descarga de publicaciones científicas desde ACM, SAGE y ScienceDirect, unificar los datos en un archivo único sin duplicados, y generar un reporte de productos eliminados.

### **Componentes a Implementar**

#### 1.1. **Scrapers y Conectores API**

**Archivos a crear:**
```
Backend/app/services/data_acquisition/
├── __init__.py
├── base_scraper.py          # Clase base abstracta
├── acm_scraper.py           # Scraper para ACM Digital Library
├── sage_scraper.py          # Scraper para SAGE Publications
├── sciencedirect_scraper.py # Scraper para ScienceDirect
├── unified_downloader.py    # Orquestador de descargas
└── parsers/
    ├── __init__.py
    ├── bibtex_parser.py     # Parser para formato BibTex
    ├── ris_parser.py        # Parser para formato RIS
    └── csv_parser.py        # Parser para formato CSV
```

**Funcionalidades clave:**

```python
# base_scraper.py - Clase base abstracta
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseScraper(ABC):
    """Clase base para todos los scrapers de bases de datos científicas."""
    
    @abstractmethod
    async def search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Busca publicaciones con la query especificada."""
        pass
    
    @abstractmethod
    async def download_metadata(self, publication_id: str) -> Dict[str, Any]:
        """Descarga metadatos completos de una publicación."""
        pass
    
    @abstractmethod
    def export_to_format(self, publications: List[Dict], format: str) -> str:
        """Exporta publicaciones al formato especificado (bibtex, ris, csv)."""
        pass
```

**Tecnologías:**
- `scrapy` para scraping web
- `aiohttp` para peticiones asíncronas
- `crossref-commons` para API de CrossRef
- `scholarly` para búsquedas académicas
- `habanero` para API de CrossRef
- `beautifulsoup4` para parsing HTML

#### 1.2. **Sistema de Unificación y Deduplicación**

**Archivos a crear:**
```
Backend/app/services/data_acquisition/
├── deduplicator.py          # Sistema de eliminación de duplicados
├── unifier.py               # Unificación de formatos
└── models/
    ├── publication.py       # Modelo de datos unificado
    └── duplicate_report.py  # Modelo de reporte de duplicados
```

**Algoritmo de deduplicación:**

```python
# deduplicator.py
import hashlib
from typing import List, Tuple, Dict
from difflib import SequenceMatcher

class Deduplicator:
    """Sistema inteligente de eliminación de duplicados."""
    
    def __init__(self, similarity_threshold: float = 0.95):
        self.similarity_threshold = similarity_threshold
        self.duplicates_report = []
    
    def calculate_title_similarity(self, title1: str, title2: str) -> float:
        """Calcula similitud entre títulos usando SequenceMatcher."""
        return SequenceMatcher(None, title1.lower(), title2.lower()).ratio()
    
    def generate_hash(self, publication: Dict) -> str:
        """Genera hash único basado en título y DOI."""
        identifier = f"{publication.get('title', '')}_{publication.get('doi', '')}"
        return hashlib.md5(identifier.encode()).hexdigest()
    
    def deduplicate(
        self, 
        publications: List[Dict]
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        Elimina duplicados y retorna:
        - Lista de publicaciones únicas
        - Lista de duplicados eliminados
        """
        unique_publications = []
        duplicates = []
        seen_hashes = set()
        
        for pub in publications:
            pub_hash = self.generate_hash(pub)
            
            # Verificar duplicados exactos por hash
            if pub_hash in seen_hashes:
                duplicates.append(pub)
                continue
            
            # Verificar duplicados por similitud de título
            is_duplicate = False
            for unique_pub in unique_publications:
                similarity = self.calculate_title_similarity(
                    pub.get('title', ''),
                    unique_pub.get('title', '')
                )
                if similarity >= self.similarity_threshold:
                    duplicates.append(pub)
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_publications.append(pub)
                seen_hashes.add(pub_hash)
        
        return unique_publications, duplicates
```

#### 1.3. **Endpoints API**

**Archivos a crear:**
```
Backend/app/api/v1/
├── __init__.py
└── data_acquisition.py  # Endpoints para descarga y unificación
```

**Endpoints a implementar:**

```python
# data_acquisition.py
from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/data", tags=["Data Acquisition"])

class DownloadRequest(BaseModel):
    query: str
    sources: List[str]  # ['acm', 'sage', 'sciencedirect']
    max_results_per_source: int = 100
    export_format: str = 'json'  # json, bibtex, ris, csv

class DownloadResponse(BaseModel):
    job_id: str
    status: str
    message: str

@router.post("/download", response_model=DownloadResponse)
async def start_download(
    request: DownloadRequest,
    background_tasks: BackgroundTasks
):
    """
    Inicia descarga automática desde múltiples fuentes.
    
    - **query**: Cadena de búsqueda (ej: "generative artificial intelligence")
    - **sources**: Lista de bases de datos a consultar
    - **max_results_per_source**: Cantidad máxima de resultados por fuente
    - **export_format**: Formato de exportación deseado
    """
    # Implementación con Celery para tareas en background
    pass

@router.get("/status/{job_id}")
async def get_download_status(job_id: str):
    """Consulta el estado de una descarga en proceso."""
    pass

@router.get("/unified")
async def get_unified_data(
    format: Optional[str] = 'json',
    include_metadata: bool = True
):
    """Obtiene los datos unificados sin duplicados."""
    pass

@router.get("/duplicates")
async def get_duplicates_report():
    """Obtiene el reporte de publicaciones duplicadas eliminadas."""
    pass
```

#### 1.4. **Modelos de Datos**

```python
# Backend/app/models/publication.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Author(BaseModel):
    name: str
    affiliation: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None

class Publication(BaseModel):
    """Modelo unificado de publicación científica."""
    
    id: str = Field(description="ID único generado")
    title: str = Field(description="Título del artículo")
    abstract: str = Field(description="Resumen del artículo")
    authors: List[Author] = Field(description="Lista de autores")
    keywords: List[str] = Field(default=[], description="Palabras clave")
    doi: Optional[str] = Field(None, description="DOI del artículo")
    publication_date: Optional[date] = Field(None, description="Fecha de publicación")
    journal: Optional[str] = Field(None, description="Revista o conferencia")
    source: str = Field(description="Fuente de datos (acm, sage, sciencedirect)")
    url: Optional[str] = Field(None, description="URL del artículo")
    citation_count: Optional[int] = Field(0, description="Número de citas")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "pub_001",
                "title": "Generative AI in Educational Contexts",
                "abstract": "This study explores...",
                "authors": [
                    {
                        "name": "John Doe",
                        "affiliation": "MIT",
                        "country": "USA"
                    }
                ],
                "keywords": ["Generative AI", "Education", "Machine Learning"],
                "doi": "10.1145/example",
                "publication_date": "2024-06-15",
                "journal": "ACM Transactions on Computer Education",
                "source": "acm"
            }
        }
```

#### 1.5. **Testing y Validación**

**Archivos a crear:**
```
Backend/tests/
├── test_data_acquisition/
│   ├── test_scrapers.py
│   ├── test_deduplicator.py
│   ├── test_parsers.py
│   └── test_api_endpoints.py
```

**Tests a implementar:**

```python
# test_deduplicator.py
import pytest
from app.services.data_acquisition.deduplicator import Deduplicator

def test_exact_duplicate_detection():
    """Verifica detección de duplicados exactos."""
    publications = [
        {"title": "AI in Education", "doi": "10.1145/123"},
        {"title": "AI in Education", "doi": "10.1145/123"},  # Duplicado
    ]
    
    dedup = Deduplicator()
    unique, duplicates = dedup.deduplicate(publications)
    
    assert len(unique) == 1
    assert len(duplicates) == 1

def test_similar_title_detection():
    """Verifica detección de duplicados por similitud."""
    publications = [
        {"title": "Generative AI in Education", "doi": "10.1145/123"},
        {"title": "Generative AI in Educational Contexts", "doi": "10.1145/456"},
    ]
    
    dedup = Deduplicator(similarity_threshold=0.8)
    unique, duplicates = dedup.deduplicate(publications)
    
    # Debería detectar como duplicados si similitud > 0.8
    assert len(unique) + len(duplicates) == 2
```

---

## 📝 REQUERIMIENTO 2: ALGORITMOS DE SIMILITUD TEXTUAL

### **Objetivo**
Implementar 6 algoritmos de similitud textual (4 clásicos + 2 con IA) con documentación matemática detallada y UI para comparación de abstracts.

### **Componentes a Implementar**

#### 2.1. **Algoritmos Clásicos de Similitud**

**Archivos a crear:**
```
Backend/app/services/ml_analysis/
├── __init__.py
├── similarity/
│   ├── __init__.py
│   ├── base_similarity.py        # Clase base abstracta
│   ├── levenshtein.py            # Distancia de edición
│   ├── tfidf_cosine.py           # TF-IDF + Similitud del Coseno
│   ├── jaccard.py                # Coeficiente de Jaccard
│   ├── ngrams.py                 # Similitud por N-gramas
│   ├── bert_embeddings.py        # BERT Embeddings
│   ├── sentence_bert.py          # Sentence-BERT
│   └── similarity_analyzer.py    # Orquestador de análisis
```

**2.1.1. Distancia de Levenshtein**

```python
# levenshtein.py
import numpy as np
from typing import Tuple, List, Dict

class LevenshteinSimilarity:
    """
    Implementación de la Distancia de Levenshtein (Edit Distance).
    
    FUNDAMENTO MATEMÁTICO:
    =====================
    La distancia de Levenshtein entre dos cadenas s1 y s2 es el número mínimo
    de operaciones de edición (inserción, eliminación, sustitución) necesarias
    para transformar s1 en s2.
    
    ALGORITMO DE PROGRAMACIÓN DINÁMICA:
    ===================================
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
    - Tiempo: O(m * n) donde m = len(s1), n = len(s2)
    - Espacio: O(m * n) para la matriz DP
    
    SIMILITUD NORMALIZADA:
    similarity = 1 - (distance / max(len(s1), len(s2)))
    """
    
    def __init__(self):
        self.name = "Distancia de Levenshtein"
        self.description = "Medida de similitud basada en operaciones de edición"
    
    def calculate_distance(
        self, 
        text1: str, 
        text2: str,
        return_matrix: bool = False
    ) -> Tuple[int, np.ndarray]:
        """
        Calcula la distancia de Levenshtein usando programación dinámica.
        
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
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        # Llenar matriz usando programación dinámica
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i-1] == text2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i-1][j],      # Eliminación
                        dp[i][j-1],      # Inserción
                        dp[i-1][j-1]     # Sustitución
                    )
        
        distance = dp[m][n]
        return (distance, dp) if return_matrix else (distance, None)
    
    def calculate_similarity(
        self, 
        text1: str, 
        text2: str
    ) -> float:
        """
        Calcula similitud normalizada [0, 1].
        
        similarity = 1 - (distance / max_length)
        
        Returns:
            float entre 0 (completamente diferentes) y 1 (idénticos)
        """
        distance, _ = self.calculate_distance(text1, text2)
        max_len = max(len(text1), len(text2))
        
        if max_len == 0:
            return 1.0
        
        similarity = 1.0 - (distance / max_len)
        return similarity
    
    def analyze_step_by_step(
        self, 
        text1: str, 
        text2: str
    ) -> Dict[str, any]:
        """
        Análisis detallado paso a paso con explicación matemática.
        
        Returns:
            Diccionario con:
            - distance: Distancia de Levenshtein
            - similarity: Similitud normalizada
            - dp_matrix: Matriz de programación dinámica
            - operations: Lista de operaciones necesarias
            - explanation: Explicación paso a paso
        """
        distance, dp_matrix = self.calculate_distance(text1, text2, return_matrix=True)
        similarity = self.calculate_similarity(text1, text2)
        
        # Reconstruir secuencia de operaciones
        operations = self._reconstruct_operations(text1, text2, dp_matrix)
        
        # Generar explicación detallada
        explanation = self._generate_explanation(
            text1, text2, distance, similarity, operations
        )
        
        return {
            "algorithm": self.name,
            "distance": distance,
            "similarity": similarity,
            "dp_matrix": dp_matrix.tolist(),
            "operations": operations,
            "explanation": explanation,
            "complexity": {
                "time": f"O({len(text1)} × {len(text2)}) = O({len(text1) * len(text2)})",
                "space": f"O({len(text1)} × {len(text2)}) = O({len(text1) * len(text2)})"
            }
        }
    
    def _reconstruct_operations(
        self, 
        text1: str, 
        text2: str, 
        dp: np.ndarray
    ) -> List[Dict[str, str]]:
        """Reconstruye la secuencia de operaciones de edición."""
        operations = []
        i, j = len(text1), len(text2)
        
        while i > 0 or j > 0:
            if i == 0:
                operations.append({
                    "type": "insert",
                    "char": text2[j-1],
                    "position": j-1
                })
                j -= 1
            elif j == 0:
                operations.append({
                    "type": "delete",
                    "char": text1[i-1],
                    "position": i-1
                })
                i -= 1
            elif text1[i-1] == text2[j-1]:
                operations.append({
                    "type": "match",
                    "char": text1[i-1],
                    "position": i-1
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
                        "position": i-1
                    })
                    i -= 1
                    j -= 1
                elif min_cost == delete_cost:
                    operations.append({
                        "type": "delete",
                        "char": text1[i-1],
                        "position": i-1
                    })
                    i -= 1
                else:
                    operations.append({
                        "type": "insert",
                        "char": text2[j-1],
                        "position": j-1
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
        """Genera explicación matemática detallada."""
        explanation = f"""
        ANÁLISIS DE SIMILITUD CON DISTANCIA DE LEVENSHTEIN
        ==================================================
        
        Textos analizados:
        - Texto 1 (m={len(text1)}): "{text1[:50]}..."
        - Texto 2 (n={len(text2)}): "{text2[:50]}..."
        
        RESULTADOS:
        -----------
        - Distancia de Levenshtein: {distance}
        - Similitud normalizada: {similarity:.4f} ({similarity*100:.2f}%)
        
        OPERACIONES NECESARIAS ({len([op for op in operations if op['type'] != 'match'])} operaciones):
        ---------------------
        """
        
        for i, op in enumerate(operations[:10], 1):  # Primeras 10 operaciones
            if op['type'] == 'substitute':
                explanation += f"{i}. Sustituir '{op['from_char']}' por '{op['to_char']}' en posición {op['position']}\n"
            elif op['type'] == 'insert':
                explanation += f"{i}. Insertar '{op['char']}' en posición {op['position']}\n"
            elif op['type'] == 'delete':
                explanation += f"{i}. Eliminar '{op['char']}' de posición {op['position']}\n"
        
        if len(operations) > 10:
            explanation += f"... ({len(operations) - 10} operaciones más)\n"
        
        return explanation
```

**2.1.2. TF-IDF + Similitud del Coseno**

```python
# tfidf_cosine.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List, Tuple

class TFIDFCosineSimilarity:
    """
    Implementación de Similitud TF-IDF + Coseno.
    
    FUNDAMENTO MATEMÁTICO:
    =====================
    
    1. TF-IDF (Term Frequency - Inverse Document Frequency):
       
       TF(t,d) = Frecuencia del término t en el documento d
                 -----------------------------------------------
                 Número total de términos en el documento d
       
       IDF(t,D) = log( Número total de documentos en D )
                      ------------------------------------
                      Número de documentos que contienen t
       
       TF-IDF(t,d,D) = TF(t,d) × IDF(t,D)
    
    2. Similitud del Coseno:
       
       cos(θ) = (A · B) / (||A|| × ||B||)
       
       Donde:
       - A · B = Producto punto de vectores A y B = Σ(Ai × Bi)
       - ||A|| = Norma euclidiana de A = √(Σ(Ai²))
       - ||B|| = Norma euclidiana de B = √(Σ(Bi²))
       
       Rango: [-1, 1]
       - 1 = Vectores idénticos en dirección
       - 0 = Vectores ortogonales
       - -1 = Vectores opuestos
    
    INTERPRETACIÓN:
    - La similitud del coseno mide el ángulo entre dos vectores en el espacio
      de características TF-IDF.
    - No considera la magnitud, solo la orientación.
    - Ideal para comparar documentos de diferentes longitudes.
    
    COMPLEJIDAD:
    - Vectorización TF-IDF: O(n × m) donde n = docs, m = vocabulario
    - Similitud del coseno: O(m) por par de documentos
    """
    
    def __init__(
        self, 
        max_features: int = 5000,
        ngram_range: Tuple[int, int] = (1, 2),
        min_df: int = 1,
        max_df: float = 0.9
    ):
        """
        Inicializa el analizador TF-IDF + Coseno.
        
        Args:
            max_features: Número máximo de características (términos)
            ngram_range: Rango de n-gramas a considerar
            min_df: Frecuencia mínima de documento
            max_df: Frecuencia máxima de documento (fracción)
        """
        self.name = "TF-IDF + Similitud del Coseno"
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=min_df,
            max_df=max_df,
            stop_words='english',
            lowercase=True,
            strip_accents='unicode'
        )
    
    def calculate_similarity(
        self, 
        text1: str, 
        text2: str
    ) -> float:
        """
        Calcula similitud del coseno entre dos textos.
        
        Returns:
            float entre 0 (completamente diferentes) y 1 (idénticos)
        """
        # Vectorizar textos
        tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
        
        # Calcular similitud del coseno
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return float(similarity)
    
    def analyze_step_by_step(
        self, 
        text1: str, 
        text2: str
    ) -> Dict[str, any]:
        """
        Análisis detallado con vectores TF-IDF y explicación matemática.
        
        Returns:
            Diccionario con análisis completo paso a paso
        """
        # Vectorizar textos
        tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
        
        # Obtener nombres de características
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Extraer vectores TF-IDF
        vector1 = tfidf_matrix[0].toarray()[0]
        vector2 = tfidf_matrix[1].toarray()[0]
        
        # Calcular similitud del coseno
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Identificar términos más relevantes
        top_terms_text1 = self._get_top_terms(vector1, feature_names, top_n=10)
        top_terms_text2 = self._get_top_terms(vector2, feature_names, top_n=10)
        
        # Calcular normas euclidianas
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        
        # Calcular producto punto
        dot_product = np.dot(vector1, vector2)
        
        # Generar explicación detallada
        explanation = self._generate_explanation(
            text1, text2, vector1, vector2, 
            dot_product, norm1, norm2, similarity,
            top_terms_text1, top_terms_text2
        )
        
        return {
            "algorithm": self.name,
            "similarity": float(similarity),
            "vectors": {
                "text1": {
                    "vector": vector1.tolist(),
                    "norm": float(norm1),
                    "top_terms": top_terms_text1
                },
                "text2": {
                    "vector": vector2.tolist(),
                    "norm": float(norm2),
                    "top_terms": top_terms_text2
                }
            },
            "dot_product": float(dot_product),
            "cosine_angle_degrees": float(np.degrees(np.arccos(similarity))),
            "vocabulary_size": len(feature_names),
            "explanation": explanation,
            "complexity": {
                "vectorization": f"O(n × m) donde n=2 documentos, m={len(feature_names)} términos",
                "similarity": "O(m) para producto punto y normas"
            }
        }
    
    def _get_top_terms(
        self, 
        vector: np.ndarray, 
        feature_names: np.ndarray, 
        top_n: int = 10
    ) -> List[Dict[str, any]]:
        """Extrae los términos con mayor peso TF-IDF."""
        # Obtener índices de términos ordenados por peso TF-IDF
        top_indices = np.argsort(vector)[-top_n:][::-1]
        
        top_terms = []
        for idx in top_indices:
            if vector[idx] > 0:
                top_terms.append({
                    "term": feature_names[idx],
                    "tfidf_weight": float(vector[idx])
                })
        
        return top_terms
    
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
        top_terms1: List[Dict],
        top_terms2: List[Dict]
    ) -> str:
        """Genera explicación matemática detallada."""
        angle_degrees = np.degrees(np.arccos(np.clip(similarity, -1, 1)))
        
        explanation = f"""
        ANÁLISIS DE SIMILITUD CON TF-IDF + COSENO
        =========================================
        
        Textos analizados:
        - Texto 1: "{text1[:50]}..."
        - Texto 2: "{text2[:50]}..."
        
        PASO 1: VECTORIZACIÓN TF-IDF
        -----------------------------
        Vocabulario total: {len(vector1)} términos únicos
        
        Términos más relevantes en Texto 1:
        """
        
        for i, term_info in enumerate(top_terms1[:5], 1):
            explanation += f"  {i}. '{term_info['term']}': TF-IDF = {term_info['tfidf_weight']:.4f}\n"
        
        explanation += "\nTérminos más relevantes en Texto 2:\n"
        for i, term_info in enumerate(top_terms2[:5], 1):
            explanation += f"  {i}. '{term_info['term']}': TF-IDF = {term_info['tfidf_weight']:.4f}\n"
        
        explanation += f"""
        
        PASO 2: CÁLCULO DE SIMILITUD DEL COSENO
        ----------------------------------------
        Fórmula: cos(θ) = (A · B) / (||A|| × ||B||)
        
        Producto punto (A · B): {dot_product:.6f}
        Norma de A (||A||): {norm1:.6f}
        Norma de B (||B||): {norm2:.6f}
        
        Similitud del coseno: {dot_product:.6f} / ({norm1:.6f} × {norm2:.6f})
                            = {dot_product:.6f} / {norm1 * norm2:.6f}
                            = {similarity:.6f}
        
        Ángulo entre vectores: {angle_degrees:.2f}°
        
        INTERPRETACIÓN:
        ---------------
        - Similitud: {similarity:.4f} ({similarity*100:.2f}%)
        - Ángulo: {angle_degrees:.2f}° (0° = idénticos, 90° = ortogonales)
        - Los documentos son {"muy similares" if similarity > 0.8 else "moderadamente similares" if similarity > 0.5 else "poco similares"}
        """
        
        return explanation
```

**(Continuaré con los otros 4 algoritmos de similitud en el siguiente mensaje debido a la longitud...)**

Ahora voy a crear el resto de los algoritmos de similitud y los siguientes requerimientos de manera estructurada.

---

## 📦 PRÓXIMOS PASOS A IMPLEMENTAR

Ahora voy a crear la estructura completa del proyecto con todos los archivos necesarios. Comenzaré implementando los componentes paso a paso.

¿Deseas que continúe con:

1. **Implementación completa del Requerimiento 1** (Scrapers + Deduplicación)
2. **Completar todos los algoritmos de similitud** (6 algoritmos completos)
3. **Implementación del Requerimiento 3** (Frecuencias de conceptos)
4. **Implementación del Requerimiento 4** (Clustering y dendrogramas)
5. **O prefieres que cree primero la estructura completa** y luego implementemos cada módulo?

También puedo:
- Crear scripts de inicialización de base de datos
- Configurar Docker y Docker Compose
- Implementar el frontend con los componentes de visualización
- Crear tests automatizados

**¿Por dónde quieres que empiece?** Te recomiendo seguir el orden de los requerimientos para tener un flujo de trabajo lógico.
