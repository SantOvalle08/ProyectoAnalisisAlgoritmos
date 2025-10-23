# 📋 PLAN DE IMPLEMENTACIÓN - PROYECTO BIBLIOMÉTRICO# 📋 PLAN DE IMPLEMENTACIÓN - ACTUALIZADO# 📋 PLAN DE IMPLEMENTACIÓN DETALLADO



**Universidad del Quindío - Análisis de Algoritmos (2025-2)**  ## Proyecto de Análisis Bibliométrico - Universidad del Quindío## Proyecto de Análisis Bibliométrico - Universidad del Quindío

**Autores:** Santiago Ovalle Cortés, Juan Sebastián Noreña  

**Última actualización:** 23 de Enero, 2025  

**Dominio:** Inteligencia Artificial Generativa en Educación  

**Cadena de búsqueda:** "generative artificial intelligence"**Autores:** Santiago Ovalle Cortés, Juan Sebastián Noreña  **Autores:** Santiago Ovalle Cortés, Juan Sebastián Noreña  



---**Curso:** Análisis de Algoritmos (2025-2)  **Curso:** Análisis de Algoritmos (2025-2)  



## 🎯 OBJETIVO GENERAL**Última actualización:** 23 de Enero, 2025  **Fecha de inicio:** 20 de Octubre, 2025  



Implementar una plataforma web automatizada para análisis bibliométrico de publicaciones científicas sobre IA Generativa, integrando algoritmos clásicos y modernos de ML/NLP, con capacidades de visualización interactiva y exportación de resultados.**Dominio:** Inteligencia Artificial Generativa en Educación  **Dominio:** Inteligencia Artificial Generativa en Educación  



---**Cadena de búsqueda:** "generative artificial intelligence"**Cadena de búsqueda:** "generative artificial intelligence"



## 📊 ESTADO ACTUAL DEL PROYECTO (23 de Enero, 2025)



### ✅ COMPLETADO (40%)------



#### **✅ Requerimiento 2: Algoritmos de Similitud Textual** (100%)

- ✅ 6 algoritmos implementados: Levenshtein, TF-IDF + Coseno, Jaccard, N-gramas, BERT, Sentence-BERT

- ✅ 8 endpoints REST funcionales con documentación OpenAPI## 🎯 OBJETIVO GENERAL## 🎯 OBJETIVO GENERAL

- ✅ Suite de tests completa (26 tests pasando)

- ✅ Documentación matemática paso a paso para cada algoritmo

- ✅ UI capaz de comparar abstracts de publicaciones

Implementar una plataforma web automatizada para análisis bibliométrico avanzado de publicaciones científicas sobre IA Generativa, integrando algoritmos clásicos y modernos de ML/NLP, con capacidades de visualización interactiva y exportación de resultados.Implementar una plataforma web automatizada para análisis bibliométrico avanzado de publicaciones científicas sobre IA Generativa, integrando algoritmos clásicos y modernos de ML/NLP, con capacidades de visualización interactiva y exportación de resultados.

**Archivos:**

- `app/services/ml_analysis/similarity/` - 7 módulos (1,800 líneas)

- `app/api/v1/similarity.py` - 742 líneas

- `tests/test_similarity_*.py` - 26 tests------



#### **✅ Parsers Bibliográficos** (100%)

- ✅ BibTeX Parser con manejo robusto de braces anidados

- ✅ RIS Parser con soporte completo de tags## 📊 ESTADO ACTUAL DEL PROYECTO## 📊 ESTADO ACTUAL DEL PROYECTO

- ✅ CSV Parser con normalización flexible

- ✅ Unificador automático con detección de formatos

- ✅ Suite de tests completa (7 tests pasando)

### ✅ **Completado (33%)**### ✅ Infraestructura Completada

**Archivos:**

- `app/services/data_acquisition/parsers/` - 4 módulos (1,380 líneas)- [x] Estructura de directorios Backend y Frontend

- `test_parsers.py` - 7 tests

#### **Requerimiento 2: Algoritmos de Similitud Textual** ✅- [x] FastAPI configurado con CORS y middlewares

#### **⚙️ Infraestructura Base** (100%)

- ✅ FastAPI con CORS y middlewares- [x] 6 algoritmos implementados (Levenshtein, TF-IDF, Jaccard, N-gramas, BERT, Sentence-BERT)- [x] Dependencias Python instaladas (requirements.txt)

- ✅ Estructura modular Backend + Frontend

- ✅ Sistema de logging y manejo de errores- [x] 8 endpoints REST funcionales- [x] Aplicación React con TypeScript y Vite

- ✅ Dependencias instaladas (requirements.txt con 79 paquetes)

- ✅ .gitignore configurado- [x] Suite de tests completa (32/32 pasando)- [x] Dependencias frontend (MUI, D3, Plotly, Recharts)

- ✅ Tests automatizados (pytest)

### ✅ **Completado (45%)**

#### **Requerimiento 2: Algoritmos de Similitud Textual** ✅

- [x] 6 algoritmos implementados (Levenshtein, TF-IDF, Jaccard, N-gramas, BERT, Sentence-BERT)
- [x] 8 endpoints REST funcionales
- [x] Suite de tests completa (39/39 pasando)
- [x] Documentación matemática integrada
- [x] Sistema de logging y manejo de errores

- **Archivos:** 7 módulos de similitud + 3 archivos de tests (2,500 líneas)

---

#### **Requerimiento 1: Automatización de Descarga** ✅

**Implementado:**
- ✅ **ACM Digital Library Scraper** - Web scraping con BeautifulSoup (450 líneas)
- ✅ **SAGE Journals Scraper** - Multi-selector CSS (448 líneas)
- ✅ **ScienceDirect Scraper** - API de Elsevier con mock data (580 líneas)
- ✅ **CrossRefScraper** - API de CrossRef totalmente funcional
- ✅ **Sistema de deduplicación** - DOI, hash MD5, fuzzy matching
- ✅ **UnifiedDownloader** - Coordinador de múltiples fuentes
- ✅ **Suite completa de tests** - 17/18 tests pasando (1 skipped)
- ✅ **8 Endpoints API de descarga** - `/api/v1/data/*`

**Archivos:**
- `app/services/data_acquisition/*.py` - 2,400 líneas
- `test_data_acquisition.py` - 450 líneas (18 tests)

---

#### **Requerimiento 6: Parsers Bibliográficos** ✅

- [x] BibTeXParser con manejo robusto de braces anidados
- [x] RISParser con soporte completo de tags
- [x] CSVParser con normalización flexible
- [x] PublicationUnifier con auto-detección de formatos
- [x] Suite de tests completa (7/7 pasando)

- **Archivos:** 4 parsers + 1 archivo de tests (1,380 líneas)

---

### ⏳ Pendiente de Implementación (55%)

- [ ] Requerimiento 3: Análisis de frecuencias de conceptos
- [ ] Requerimiento 4: Clustering jerárquico y dendrogramas
- [ ] Requerimiento 5: Visualizaciones interactivas
- [ ] Requerimiento 6: Despliegue y documentación técnica

---

## 🗓️ CRONOGRAMA DE IMPLEMENTACIÓN

### **Fase 1: Requerimiento 1 - Automatización de Descarga** ✅ COMPLETADO

- ✅ Días 1-2: Scrapers (ACM, SAGE, ScienceDirect) y conectores API
- ✅ Día 3: Unificación y eliminación de duplicados
- ✅ Días 4-5: Testing y validación (56/57 tests pasando)

- ❌ Cálculo de precisión de palabras generadas

- ❌ Visualización de frecuencias- [ ] Endpoints REST



**Categoría a analizar:**- **Prioridad:** ALTA | **Estimado:** 6 horas### **Fase 2: Requerimiento 2 - Similitud Textual** (7 días)

```

Concepts of Generative AI in Education:- Días 6-7: Algoritmos clásicos (Levenshtein, TF-IDF, Jaccard, N-gramas)

- Generative models, Prompting, Machine learning, Multimodality

- Fine-tuning, Training data, Algorithmic bias#### **Requerimiento 4: Clustering Jerárquico**- Días 8-9: Algoritmos con IA (BERT, Sentence-BERT)

- Explainability, Transparency, Ethics, Privacy

- Personalization, Human-AI interaction, AI literacy, Co-creation- [ ] Algoritmo de clustering- Días 10-11: Documentación matemática detallada

```

- [ ] Generación de dendrogramas- Día 12: UI para comparación de abstracts

**Estimado:** 2 días (12 horas)

- [ ] Identificación automática de grupos

#### **Requerimiento 4: Clustering Jerárquico** (0%)

- ❌ Preprocesamiento de abstracts- [ ] Métricas de evaluación### **Fase 3: Requerimiento 3 - Frecuencias de Conceptos** (4 días)

- ❌ Implementación de 3 algoritmos de clustering (Ward, Average Linkage, Complete Linkage)

- ❌ Generación de dendrogramas interactivos- [ ] Endpoints REST- Día 13: Análisis de frecuencias de categorías predefinidas

- ❌ Evaluación comparativa (Silhouette Score)

- **Prioridad:** ALTA | **Estimado:** 6 horas- Día 14: Generación automática de palabras asociadas con NLP

**Estimado:** 3 días (18 horas)

- Día 15: Métricas de precisión

#### **Requerimiento 5: Visualizaciones Interactivas** (0%)

- ❌ Mapa de calor geográfico (distribución por país del primer autor)#### **Requerimiento 5: Scrapers Adicionales**- Día 16: Visualizaciones de frecuencias

- ❌ Nube de palabras dinámica (términos frecuentes en abstracts y keywords)

- ❌ Línea temporal de publicaciones por año y revista- [ ] ACM Digital Library scraper

- ❌ Exportación a PDF de visualizaciones

- [ ] SAGE Journals scraper### **Fase 4: Requerimiento 4 - Clustering Jerárquico** (5 días)

**Estimado:** 2 días (12 horas)

- [ ] ScienceDirect scraper- Días 17-18: Preprocesamiento de texto y vectorización

#### **Requerimiento 6: Despliegue y Documentación** (0%)

- ❌ Dockerización del proyecto- **Prioridad:** MEDIA | **Estimado:** 12 horas- Día 19: Implementación de 3 algoritmos de clustering

- ❌ Configuración de CI/CD

- ❌ Documentación técnica completa- Día 20: Generación de dendrogramas interactivos con D3.js

- ❌ Despliegue en producción

---- Día 21: Evaluación comparativa (Silhouette Score)

**Estimado:** 2 días (12 horas)



---

## 🧹 LIMPIEZA REALIZADA (23 de Enero, 2025)### **Fase 5: Requerimiento 5 - Visualizaciones** (4 días)

## 🗓️ PLAN DE ACCIÓN PRIORIZADO

- Día 22: Mapa de calor geográfico (Plotly/Leaflet)

### **Fase 1: Completar Requerimiento 1** (2 días)

**Prioridad: CRÍTICA** - Es la base para todos los demás requerimientos### **Archivos Eliminados**- Día 23: Nube de palabras dinámica (D3.js)



1. **Día 1: Completar Scrapers**- Día 24: Línea temporal por año y revista (Recharts)

   - ✅ Verificar y completar ACM Scraper

   - ✅ Verificar y completar SAGE Scraper#### **Debug y Temporales**- Día 25: Exportación a PDF (jsPDF + html2canvas)

   - 🆕 Implementar ScienceDirect Scraper

   - ✅ Testing de scrapers individuales- ❌ `Backend/debug_bibtex.py` - Script de debug temporal



2. **Día 2: Integración y API**- ❌ `Backend/test_debug.py` - Test de debug### **Fase 6: Requerimiento 6 - Despliegue y Documentación** (4 días)

   - 🆕 Crear endpoints API `/api/v1/data`

   - ✅ Integrar UnifiedDownloader con todos los scrapers- ❌ `Backend/test_requerimiento1.log` - Log temporal- Día 26: Documentación técnica de arquitectura

   - ✅ Implementar sistema de jobs en background (Celery/BackgroundTasks)

   - ✅ Testing de integración completa- ❌ `SESION_RESUMEN.md` - Documentación temporal- Día 27: Documentación de algoritmos implementados

   - 📝 Generar dataset unificado de prueba

- ❌ `SESION_PARSERS.md` - Documentación temporal- Día 28: Dockerización y CI/CD

**Entregables:**

- Sistema automático de descarga funcionando- ❌ `PROGRESO.md` - Duplicado (se mantiene PROGRESO_ACTUALIZADO.md)- Día 29: Despliegue en producción

- API REST para descarga (`/download`, `/status/{job_id}`, `/unified`, `/duplicates`)

- Dataset unificado en `data/downloads/unified.json`

- Reporte de duplicados en `data/downloads/duplicates_report.json`

#### **Cache y Builds**### **Fase 7: Testing Final y Optimización** (2 días)

---

- ❌ `Backend/__pycache__/` (recursivo)- Día 30: Testing integral y correcciones

### **Fase 2: Requerimiento 3 - Análisis de Frecuencias** (1.5 días)

- ❌ `Backend/.pytest_cache/`- Día 31: Optimización de rendimiento

1. **Paso 1: Análisis de Categoría Predefinida** (0.5 día)

   - Implementar `FrequencyAnalyzer` en `app/services/analytics/`- ❌ Todos los `__pycache__/` en subdirectorios

   - Buscar palabras asociadas en abstracts

   - Calcular frecuencias y generar estadísticas**TOTAL ESTIMADO: 31 días (≈ 6-7 semanas)**



2. **Paso 2: Generación Automática de Palabras** (0.5 día)#### **Datos Temporales**

   - Usar NLP (NLTK/spaCy) para extracción de términos

   - Lematización y eliminación de stopwords- ❌ `Backend/data/downloads/*.json` - Descargas de prueba---

   - Generar top 15 palabras asociadas automáticamente

- ❌ `Backend/data/downloads/*.bib`

3. **Paso 3: Métricas de Precisión** (0.5 día)

   - Calcular precisión comparando palabras generadas vs predefinidas- ❌ `Backend/data/downloads/*.ris`## 🏗️ ARQUITECTURA DEL SISTEMA

   - Implementar endpoints API

   - Testing y visualización básica- ❌ `Backend/data/downloads/*.csv`



**Entregables:**```

- `app/services/analytics/frequency_analyzer.py`

- Endpoints: `/api/v1/analytics/frequencies`, `/api/v1/analytics/associated-words`**Total eliminado:** ~35 archivos + directorios de cache┌─────────────────────────────────────────────────────────────┐

- Reporte de precisión

│                      FRONTEND (React + TS)                   │

---

### **Nuevo .gitignore Creado**│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │

### **Fase 3: Requerimiento 4 - Clustering Jerárquico** (2 días)

│  │   D3.js     │  │  Plotly.js  │  │  Recharts   │         │

1. **Paso 1: Preprocesamiento** (0.5 día)

   - Pipeline de limpieza de textoExcluye:│  │ Dendrogramas│  │ Mapas Calor │  │  Líneas     │         │

   - Vectorización (TF-IDF o embeddings)

   - Normalización- `__pycache__/`, `*.pyc`, `*.pyo`│  └─────────────┘  └─────────────┘  └─────────────┘         │



2. **Paso 2: Algoritmos de Clustering** (1 día)- `venv/`, `.venv/`, `env/`└────────────────────────┬────────────────────────────────────┘

   - Implementar Ward Linkage

   - Implementar Average Linkage- `.pytest_cache/`, `.coverage`                         │ HTTP/REST API

   - Implementar Complete Linkage

   - Métricas de evaluación (Silhouette Score)- `.env`, `.env.local`┌────────────────────────▼────────────────────────────────────┐



3. **Paso 3: Dendrogramas** (0.5 día)- `Backend/data/downloads/*` (excepto `.gitkeep`)│                   BACKEND (FastAPI)                          │

   - Generar dendrogramas con scipy/matplotlib

   - Implementar endpoints API- `Backend/logs/*.log`│  ┌──────────────────────────────────────────────────────┐   │

   - Testing

- `Backend/models/*.pkl`, `*.h5`, `*.pt`│  │            API ENDPOINTS (v1)                        │   │

**Entregables:**

- `app/services/ml_analysis/clustering/hierarchical_clustering.py`- `SESION_*.md` (archivos de sesión temporal)│  ├──────────────────────────────────────────────────────┤   │

- Endpoints: `/api/v1/clustering/hierarchical`

- Dendrogramas en formato JSON para visualización- `debug_*.py`, `test_debug.py`│  │ /api/v1/data          - Data Acquisition Service    │   │



---- `node_modules/`, `dist/`, `build/`│  │ /api/v1/ml            - ML & NLP Service             │   │



### **Fase 4: Requerimiento 5 - Visualizaciones** (2 días)- `.DS_Store`, `Thumbs.db`│  │ /api/v1/analytics     - Analytics Service            │   │



1. **Backend: Endpoints de Datos** (0.5 día)│  │ /api/v1/viz           - Visualization Service        │   │

   - `/api/v1/viz/geographic-distribution`

   - `/api/v1/viz/word-cloud-data`---│  └──────────────────────────────────────────────────────┘   │

   - `/api/v1/viz/timeline`

│                                                              │

2. **Frontend: Implementación de Visualizaciones** (1 día)

   - Mapa de calor geográfico (Plotly/Leaflet)## 🏗️ ESTRUCTURA FINAL DEL REPOSITORIO│  ┌─────────────────────────────────────────────────────┐    │

   - Nube de palabras dinámica (D3.js/react-wordcloud)

   - Línea temporal (Recharts)│  │         SERVICIOS DE NEGOCIO                        │    │



3. **Exportación PDF** (0.5 día)```│  ├─────────────────────────────────────────────────────┤    │

   - Implementar jsPDF + html2canvas

   - Endpoint `/api/v1/viz/export-pdf`ProyectoAnalisisAlgoritmos/│  │ 🔍 DataAcquisitionService                           │    │



**Entregables:**├── .gitignore                      # Control de versiones│  │    - Scrapers (ACM, SAGE, ScienceDirect)           │    │

- Componentes React en `Frontend/bibliometric-app/src/components/visualizations/`

- Sistema de exportación PDF funcional├── README.md                       # Documentación principal│  │    - Unificación y deduplicación                    │    │



---├── PLAN_IMPLEMENTACION.md         # Este archivo│  │                                                      │    │



### **Fase 5: Requerimiento 6 - Despliegue** (1.5 días)├── PROGRESO_ACTUALIZADO.md        # Estado detallado del proyecto│  │ 🤖 MLAnalysisService                                │    │



1. **Dockerización** (0.5 día)││  │    - Similitud clásica (Levenshtein, TF-IDF, etc.) │    │

   - Dockerfile para Backend

   - Dockerfile para Frontend├── Backend/│  │    - Similitud IA (BERT, Sentence-BERT)            │    │

   - docker-compose.yml

│   ├── main.py                    # Aplicación FastAPI principal│  │    - Clustering jerárquico (Ward, Average, etc.)   │    │

2. **Documentación** (0.5 día)

   - README.md completo│   ├── requirements.txt           # Dependencias Python│  │                                                      │    │

   - Documentación técnica de algoritmos

   - Guía de instalación y uso│   ├── pytest.ini                 # Configuración de pytest│  │ 📊 AnalyticsService                                 │    │



3. **Despliegue** (0.5 día)│   ├── .env.example              # Template de variables de entorno│  │    - Frecuencias de conceptos                       │    │

   - Configurar CI/CD (GitHub Actions)

   - Deploy en servidor (Heroku/Railway/DigitalOcean)│   ││  │    - Métricas bibliométricas                        │    │

   - Testing en producción

│   ├── app/│  │    - Generación de palabras asociadas               │    │

**Entregables:**

- Aplicación desplegada y accesible│   │   ├── __init__.py│  │                                                      │    │

- Documentación completa

- Repositorio limpio y profesional│   │   ├── api/│  │ 📈 VisualizationService                             │    │



---│   │   │   ├── __init__.py│  │    - Mapas de calor geográficos                     │    │



## 🏗️ ARQUITECTURA DEL SISTEMA│   │   │   └── v1/│  │    - Nubes de palabras                              │    │



```│   │   │       ├── __init__.py│  │    - Líneas temporales                              │    │

┌─────────────────────────────────────────────────────────────┐

│                  FRONTEND (React + TypeScript)               ││   │   │       ├── data_acquisition.py│  │    - Exportación PDF                                │    │

│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │

│  │   D3.js      │  │  Plotly.js   │  │  Recharts    │      ││   │   │       └── similarity.py│  └─────────────────────────────────────────────────────┘    │

│  │ Dendrogramas │  │ Mapa Calor   │  │  Timeline    │      │

│  └──────────────┘  └──────────────┘  └──────────────┘      ││   │   │└────────────────────────┬────────────────────────────────────┘

└───────────────────────────┬─────────────────────────────────┘

                            │ HTTP/REST API│   │   ├── config/                         │

┌───────────────────────────▼─────────────────────────────────┐

│                   BACKEND (FastAPI)                          ││   │   │   ├── __init__.py┌────────────────────────▼────────────────────────────────────┐

│  ┌────────────────────────────────────────────────────────┐ │

│  │         API ENDPOINTS (/api/v1)                        │ ││   │   │   └── settings.py│               CAPA DE DATOS                                  │

│  ├────────────────────────────────────────────────────────┤ │

│  │ /data/*          - Descarga y unificación (Req 1)     │ ││   │   ││  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │

│  │ /similarity/*    - Similitud textual (Req 2) ✅       │ │

│  │ /analytics/*     - Frecuencias (Req 3)                │ ││   │   ├── models/│  │  PostgreSQL  │  │    Redis     │  │  File System │      │

│  │ /clustering/*    - Clustering jerárquico (Req 4)      │ │

│  │ /viz/*           - Visualizaciones (Req 5)            │ ││   │   │   ├── __init__.py│  │  Metadatos   │  │    Cache     │  │  Archivos    │      │

│  └────────────────────────────────────────────────────────┘ │

│                                                              ││   │   │   └── publication.py│  │  Publicac.   │  │  Embeddings  │  │  CSV/BibTeX  │      │

│  ┌────────────────────────────────────────────────────────┐ │

│  │              SERVICIOS DE NEGOCIO                      │ ││   │   ││  └──────────────┘  └──────────────┘  └──────────────┘      │

│  ├────────────────────────────────────────────────────────┤ │

│  │ 📥 DataAcquisitionService (Req 1) - 40% ⏳            │ ││   │   ├── services/└─────────────────────────────────────────────────────────────┘

│  │    - Scrapers: ACM, SAGE, ScienceDirect              │ │

│  │    - Parsers: BibTeX, RIS, CSV ✅                     │ ││   │   │   ├── __init__.py```

│  │    - Deduplicador inteligente                         │ │

│  │                                                        │ ││   │   │   ├── analytics/               # Placeholder (Req. 3)

│  │ 🤖 MLAnalysisService                                  │ │

│  │    - Similitud (Req 2) ✅                             │ ││   │   │   │   └── __init__.py---

│  │    - Clustering (Req 4) - 0% ❌                       │ │

│  │                                                        │ ││   │   │   ├── data_acquisition/

│  │ 📊 AnalyticsService (Req 3) - 0% ❌                   │ │

│  │    - Frecuencias de conceptos                         │ ││   │   │   │   ├── __init__.py## 📝 REQUERIMIENTO 1: AUTOMATIZACIÓN DE DESCARGA DE DATOS

│  │    - Generación de palabras asociadas                 │ │

│  │    - Métricas de precisión                            │ ││   │   │   │   ├── base_scraper.py

│  │                                                        │ │

│  │ 📈 VisualizationService (Req 5) - 0% ❌               │ ││   │   │   │   ├── crossref_scraper.py### **Objetivo**

│  │    - Mapas de calor geográficos                       │ │

│  │    - Nubes de palabras dinámicas                      │ ││   │   │   │   ├── deduplicator.pyAutomatizar la descarga de publicaciones científicas desde ACM, SAGE y ScienceDirect, unificar los datos en un archivo único sin duplicados, y generar un reporte de productos eliminados.

│  │    - Líneas temporales                                │ │

│  │    - Exportación PDF                                  │ ││   │   │   │   ├── unified_downloader.py

│  └────────────────────────────────────────────────────────┘ │

└───────────────────────────┬─────────────────────────────────┘│   │   │   │   └── parsers/### **Componentes a Implementar**

                            │

┌───────────────────────────▼─────────────────────────────────┐│   │   │   │       ├── __init__.py

│                   CAPA DE DATOS                              │

│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      ││   │   │   │       ├── bibtex_parser.py   # ✅ 450 líneas#### 1.1. **Scrapers y Conectores API**

│  │  PostgreSQL  │  │    Redis     │  │  File System │      │

│  │  (Futuro)    │  │    Cache     │  │  JSON/CSV    │      ││   │   │   │       ├── ris_parser.py      # ✅ 420 líneas

│  └──────────────┘  └──────────────┘  └──────────────┘      │

└─────────────────────────────────────────────────────────────┘│   │   │   │       ├── csv_parser.py      # ✅ 290 líneas**Archivos a crear:**

```

│   │   │   │       └── unifier.py         # ✅ 220 líneas```

---

│   │   │   ├── ml_analysis/Backend/app/services/data_acquisition/

## 📦 ESTRUCTURA DE ARCHIVOS

│   │   │   │   ├── __init__.py├── __init__.py

```

ProyectoAnalisisAlgoritmos/│   │   │   │   └── similarity/├── base_scraper.py          # Clase base abstracta

├── .gitignore                          ✅

├── README.md                           ✅│   │   │   │       ├── __init__.py├── acm_scraper.py           # Scraper para ACM Digital Library

├── PLAN_IMPLEMENTACION.md             ✅ (este archivo)

││   │   │   │       ├── base_similarity.py       # ✅├── sage_scraper.py          # Scraper para SAGE Publications

├── Backend/

│   ├── main.py                        ✅ FastAPI app (247 líneas)│   │   │   │       ├── levenshtein.py          # ✅├── sciencedirect_scraper.py # Scraper para ScienceDirect

│   ├── requirements.txt               ✅ 79 dependencias

│   ├── pytest.ini                     ✅│   │   │   │       ├── tfidf_cosine.py         # ✅├── unified_downloader.py    # Orquestador de descargas

│   │

│   ├── app/│   │   │   │       ├── jaccard.py              # ✅└── parsers/

│   │   ├── __init__.py               ✅

│   │   ││   │   │   │       ├── ngrams.py               # ✅    ├── __init__.py

│   │   ├── api/v1/

│   │   │   ├── __init__.py           ✅│   │   │   │       ├── bert_embeddings.py      # ✅    ├── bibtex_parser.py     # Parser para formato BibTex

│   │   │   ├── similarity.py         ✅ (742 líneas) - Req 2

│   │   │   ├── data_acquisition.py   ⏳ (pendiente completar) - Req 1│   │   │   │       └── sentence_bert.py        # ✅    ├── ris_parser.py        # Parser para formato RIS

│   │   │   ├── analytics.py          ❌ (crear) - Req 3

│   │   │   ├── clustering.py         ❌ (crear) - Req 4│   │   │   └── visualization/           # Placeholder    └── csv_parser.py        # Parser para formato CSV

│   │   │   └── visualization.py      ❌ (crear) - Req 5

│   │   ││   │   │       └── __init__.py```

│   │   ├── models/

│   │   │   ├── __init__.py           ✅│   │   └── utils/

│   │   │   └── publication.py        ✅

│   │   ││   │       └── __init__.py**Funcionalidades clave:**

│   │   ├── services/

│   │   │   ├── data_acquisition/│   │

│   │   │   │   ├── base_scraper.py           ✅ (368 líneas)

│   │   │   │   ├── crossref_scraper.py       ⏳ (verificar)│   ├── data/```python

│   │   │   │   ├── acm_scraper.py            ⏳ (completar)

│   │   │   │   ├── sage_scraper.py           ⏳ (completar)│   │   └── downloads/# base_scraper.py - Clase base abstracta

│   │   │   │   ├── sciencedirect_scraper.py  ❌ (crear)

│   │   │   │   ├── deduplicator.py           ⏳ (verificar)│   │       └── .gitkeepfrom abc import ABC, abstractmethod

│   │   │   │   ├── unified_downloader.py     ✅ (431 líneas)

│   │   │   │   └── parsers/│   │from typing import List, Dict, Any

│   │   │   │       ├── bibtex_parser.py      ✅ (450 líneas)

│   │   │   │       ├── ris_parser.py         ✅ (420 líneas)│   ├── logs/

│   │   │   │       ├── csv_parser.py         ✅ (290 líneas)

│   │   │   │       └── unifier.py            ✅ (220 líneas)│   │   └── .gitkeepclass BaseScraper(ABC):

│   │   │   │

│   │   │   ├── ml_analysis/│   │    """Clase base para todos los scrapers de bases de datos científicas."""

│   │   │   │   ├── similarity/                    ✅ Req 2

│   │   │   │   │   ├── levenshtein.py            ✅│   ├── models/    

│   │   │   │   │   ├── tfidf_cosine.py           ✅

│   │   │   │   │   ├── jaccard.py                ✅│   │   └── .gitkeep    @abstractmethod

│   │   │   │   │   ├── ngrams.py                 ✅

│   │   │   │   │   ├── bert_embeddings.py        ✅│   │    async def search(self, query: str, max_results: int) -> List[Dict[str, Any]]:

│   │   │   │   │   └── sentence_bert.py          ✅

│   │   │   │   ││   └── tests/        """Busca publicaciones con la query especificada."""

│   │   │   │   └── clustering/                    ❌ Req 4

│   │   │   │       ├── __init__.py               ❌ (crear)│       ├── __init__.py        pass

│   │   │   │       ├── hierarchical.py           ❌ (crear)

│   │   │   │       └── dendrogram_generator.py   ❌ (crear)│       ├── test_similarity_endpoints.py   # ✅ 23 tests    

│   │   │   │

│   │   │   ├── analytics/                         ❌ Req 3│       ├── test_similarity_api.py         # ✅ 3 tests    @abstractmethod

│   │   │   │   ├── __init__.py                   ✅ (placeholder)

│   │   │   │   ├── frequency_analyzer.py         ❌ (crear)│       ├── test_parsers.py                # ✅ 7 tests    async def download_metadata(self, publication_id: str) -> Dict[str, Any]:

│   │   │   │   └── word_extractor.py             ❌ (crear)

│   │   │   ││       ├── test_similitud.py              # ✅ 4 tests        """Descarga metadatos completos de una publicación."""

│   │   │   └── visualization/                     ❌ Req 5

│   │   │       ├── __init__.py                   ✅ (placeholder)│       └── test_requerimiento1.py         # ✅ 2 tests        pass

│   │   │       ├── geographic_map.py             ❌ (crear)

│   │   │       └── pdf_exporter.py               ❌ (crear)│    

│   │   │

│   │   └── utils/└── Frontend/    @abstractmethod

│   │       └── __init__.py                       ✅

│   │    └── bibliometric-app/    def export_to_format(self, publications: List[Dict], format: str) -> str:

│   ├── data/downloads/                           ✅ (.gitkeep)

│   ├── logs/                                     ✅ (.gitkeep)        ├── package.json        """Exporta publicaciones al formato especificado (bibtex, ris, csv)."""

│   ├── models/                                   ✅ (.gitkeep)

│   │        ├── vite.config.ts        pass

│   └── tests/

│       ├── test_parsers.py                      ✅ (7 tests pasando)        ├── tsconfig.json```

│       ├── test_similitud.py                    ✅ (4 tests pasando)

│       ├── test_similarity_api.py               ✅ (3 tests pasando)        ├── .gitignore

│       ├── test_similarity_endpoints.py         ✅ (23 tests pasando)

│       └── test_requerimiento1.py               ✅ (2 tests pasando)        ├── public/**Tecnologías:**

│

└── Frontend/bibliometric-app/        └── src/- `scrapy` para scraping web

    ├── package.json                             ✅

    ├── vite.config.ts                           ✅            ├── main.tsx- `aiohttp` para peticiones asíncronas

    └── src/

        ├── main.tsx                             ✅            ├── App.tsx- `crossref-commons` para API de CrossRef

        ├── App.tsx                              ✅

        ├── components/                          ⏳ (pendiente)            ├── types/- `scholarly` para búsquedas académicas

        └── services/api.ts                      ✅

```            ├── services/- `habanero` para API de CrossRef



---            └── hooks/- `beautifulsoup4` para parsing HTML



## ✅ CHECKLIST DE FINALIZACIÓN```



### Requerimiento 1: Automatización de Descarga#### 1.2. **Sistema de Unificación y Deduplicación**

- [x] Parsers BibTeX, RIS, CSV ✅

- [x] BaseScraper y estructura ✅**Estadísticas:**

- [ ] ACM Scraper funcional

- [ ] SAGE Scraper funcional- **Archivos Python activos:** 35**Archivos a crear:**

- [ ] ScienceDirect Scraper funcional

- [ ] Deduplicador probado- **Líneas de código:** ~4,500```

- [ ] UnifiedDownloader integrado

- [ ] Endpoints API `/api/v1/data/*`- **Tests:** 39 totales (11 pasando)Backend/app/services/data_acquisition/

- [ ] Testing completo

- [ ] Dataset unificado generado- **Cobertura:** ~70%├── deduplicator.py          # Sistema de eliminación de duplicados

- [ ] Reporte de duplicados generado

├── unifier.py               # Unificación de formatos

### Requerimiento 2: Similitud Textual

- [x] 6 algoritmos implementados ✅---└── models/

- [x] Documentación matemática ✅

- [x] Endpoints API ✅    ├── publication.py       # Modelo de datos unificado

- [x] Testing completo ✅

- [x] UI para comparación ✅## 📦 DEPENDENCIAS    └── duplicate_report.py  # Modelo de reporte de duplicados



### Requerimiento 3: Frecuencias```

- [ ] FrequencyAnalyzer

- [ ] Análisis de categoría predefinida### **Backend (Python 3.13)**

- [ ] Generación de palabras con NLP

- [ ] Métricas de precisión**Algoritmo de deduplicación:**

- [ ] Endpoints API

- [ ] Visualizaciones```txt



### Requerimiento 4: Clustering# Web Framework```python

- [ ] 3 algoritmos de clustering

- [ ] Preprocesamiento de textofastapi==0.119.1# deduplicator.py

- [ ] Generación de dendrogramas

- [ ] Evaluación (Silhouette Score)uvicorn==0.34.0import hashlib

- [ ] Endpoints API

- [ ] Testingpydantic==2.10.3from typing import List, Tuple, Dict



### Requerimiento 5: Visualizacionesfrom difflib import SequenceMatcher

- [ ] Mapa de calor geográfico

- [ ] Nube de palabras dinámica# ML/NLP

- [ ] Línea temporal

- [ ] Exportación PDFscikit-learn==1.6.1class Deduplicator:

- [ ] Endpoints API

- [ ] Integración frontendsentence-transformers==3.4.0    """Sistema inteligente de eliminación de duplicados."""



### Requerimiento 6: Desplieguepython-Levenshtein==0.27.0    

- [ ] Dockerfile Backend

- [ ] Dockerfile Frontend    def __init__(self, similarity_threshold: float = 0.95):

- [ ] docker-compose.yml

- [ ] CI/CD configurado# Testing        self.similarity_threshold = similarity_threshold

- [ ] Documentación completa

- [ ] Aplicación desplegadapytest==8.4.2        self.duplicates_report = []



---pytest-asyncio==0.25.2    



## 📈 PROGRESO GENERALhttpx==0.28.1    def calculate_title_similarity(self, title1: str, title2: str) -> float:



``````        """Calcula similitud entre títulos usando SequenceMatcher."""

Requerimiento 1: [████████░░░░░░░░░░] 40%

Requerimiento 2: [████████████████████] 100% ✅        return SequenceMatcher(None, title1.lower(), title2.lower()).ratio()

Requerimiento 3: [░░░░░░░░░░░░░░░░░░░░]   0%

Requerimiento 4: [░░░░░░░░░░░░░░░░░░░░]   0%### **Frontend (Node.js)**    

Requerimiento 5: [░░░░░░░░░░░░░░░░░░░░]   0%

Requerimiento 6: [░░░░░░░░░░░░░░░░░░░░]   0%    def generate_hash(self, publication: Dict) -> str:



TOTAL PROYECTO: [████████░░░░░░░░░░░░] 40%```json        """Genera hash único basado en título y DOI."""

```

{        identifier = f"{publication.get('title', '')}_{publication.get('doi', '')}"

**Estimado para completar:** 9 días (54 horas de trabajo)

  "dependencies": {        return hashlib.md5(identifier.encode()).hexdigest()

---

    "react": "^18.3.1",    

## 🚀 PRÓXIMOS PASOS INMEDIATOS

    "@mui/material": "^6.3.0",    def deduplicate(

1. **Verificar estado de scrapers existentes**

   - Revisar `acm_scraper.py`, `sage_scraper.py`, `crossref_scraper.py`    "recharts": "^2.15.0"        self, 

   - Identificar qué falta completar

  }        publications: List[Dict]

2. **Completar Requerimiento 1**

   - Implementar scrapers faltantes}    ) -> Tuple[List[Dict], List[Dict]]:

   - Crear endpoints API

   - Testing completo```        """

   - Generar dataset de prueba

        Elimina duplicados y retorna:

3. **Continuar con Requerimiento 3**

   - Implementar análisis de frecuencias---        - Lista de publicaciones únicas

   - NLP para generación de palabras

        - Lista de duplicados eliminados

---

## 🎯 PRÓXIMOS PASOS        """

**Última actualización:** 23 de Enero, 2025  

**Versión:** 3.0          unique_publications = []

**Estado:** 🟢 En desarrollo activo (40% completado)

### **Inmediato**        duplicates = []

1. **Requerimiento 3:** Análisis de Frecuencias (6h)        seen_hashes = set()

2. **Requerimiento 4:** Clustering Jerárquico (6h)        

3. **Frontend:** Integración básica (8h)        for pub in publications:

            pub_hash = self.generate_hash(pub)

### **Corto Plazo**            

4. **Requerimiento 5:** Scrapers adicionales (12h)            # Verificar duplicados exactos por hash

5. **Visualizaciones:** Implementación completa (10h)            if pub_hash in seen_hashes:

                duplicates.append(pub)

### **Largo Plazo**                continue

6. **Despliegue:** Producción (4h)            

7. **Documentación:** Completa (8h)            # Verificar duplicados por similitud de título

            is_duplicate = False

---            for unique_pub in unique_publications:

                similarity = self.calculate_title_similarity(

## ✅ CHECKLIST DE CALIDAD                    pub.get('title', ''),

                    unique_pub.get('title', '')

- [x] Código limpio y documentado                )

- [x] Tests pasando                if similarity >= self.similarity_threshold:

- [x] .gitignore configurado                    duplicates.append(pub)

- [x] Estructura modular                    is_duplicate = True

- [x] Logging implementado                    break

- [ ] Cobertura >80%            

- [ ] Frontend funcional            if not is_duplicate:

- [ ] CI/CD configurado                unique_publications.append(pub)

                seen_hashes.add(pub_hash)

---        

        return unique_publications, duplicates

**Última actualización:** 23 de Enero, 2025  ```

**Versión:** 2.0  

**Estado:** 🟢 En desarrollo activo#### 1.3. **Endpoints API**


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
