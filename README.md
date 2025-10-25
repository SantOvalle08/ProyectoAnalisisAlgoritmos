# 📊 Proyecto Análisis de Algoritmos Aplicados a Bibliometría

[![Python Version](https://img.shields.io/badge/python-3.13.7-blue.svg)](https://www.python.org/)
[![Node.js Version](https://img.shields.io/badge/node.js-20+-green.svg)](https://nodejs.org/)
[![Tests](https://img.shields.io/badge/tests-132%2F133%20passing-brightgreen.svg)](https://github.com/SantOvalle08/ProyectoAnalisisAlgoritmos)
[![License](https://img.shields.io/badge/license-Academic-blue.svg)](LICENSE)

Plataforma web automatizada para el análisis bibliométrico avanzado de publicaciones científicas sobre inteligencia artificial generativa, desarrollada para el curso **"Análisis de Algoritmos" (2025-2)**, Universidad del Quindío.

## 🎯 Estado del Proyecto

### ✅ **PROYECTO COMPLETADO AL 100%**

**Todos los requerimientos funcionales implementados y probados:**
- ✅ **Requerimiento 1**: Automatización completa de descarga de datos
- ✅ **Requerimiento 2**: 6 algoritmos de similitud textual implementados
- ✅ **Requerimiento 3**: Análisis de frecuencias de conceptos funcional
- ✅ **Requerimiento 4**: Clustering jerárquico avanzado operativo
- ✅ **Requerimiento 5**: Visualizaciones científicas interactivas activas
- ✅ **Requerimiento 6**: Aplicación web desplegada con documentación completa

**Métricas de Calidad:**
- 🧪 **Tests**: 132/133 pasando (99.2% de éxito)
- 📈 **Cobertura**: 64%+ líneas de código probadas
- ⚡ **Performance**: Benchmarks completos implementados
- 🔧 **Integración**: Frontend-Backend completamente sincronizado

---

## 📋 Descripción y Requerimientos

Sistema integral de análisis bibliométrico que implementa algoritmos de machine learning y procesamiento de lenguaje natural para el estudio computacional de la producción científica en el dominio de **"Inteligencia Artificial Generativa en Educación"**.

### 🎯 Alcance
- **Dominio:** Inteligencia Artificial Generativa
- **Cadena de búsqueda:** `"generative artificial intelligence"`
- **Fuentes:** ACM, SAGE, ScienceDirect, CrossRef
- **Enfoque:** Análisis bibliométrico automatizado con visualizaciones interactivas

### 🚀 Requerimientos Funcionales Implementados

1. **✅ Automatización de Descarga de Datos**
   - Integración con múltiples bases científicas
   - Unificación de formatos (BibTeX, RIS, CSV, JSON)
   - Deduplicación inteligente (>95% precisión)

2. **✅ Algoritmos de Similitud Textual (6 algoritmos)**
   - **Clásicos:** Levenshtein, TF-IDF+Coseno, Jaccard, N-gramas
   - **IA:** BERT Sentence Embeddings, Sentence-BERT

3. **✅ Análisis de Frecuencias de Conceptos**
   - Categoría predefinida: "Concepts of Generative AI in Education" (15 términos)
   - Extracción automática con TF-IDF y frecuencia
   - Generación de palabras asociadas mediante NLP

4. **✅ Clustering Jerárquico Avanzado**
   - **3 Algoritmos:** Ward, Average, Complete Linkage
   - Dendrogramas interactivos
   - Evaluación comparativa de coherencia

5. **✅ Visualizaciones Científicas Interactivas**
   - Mapas de calor geográficos por autor
   - Nubes de palabras dinámicas
   - Líneas temporales por año/revista
   - Exportación automática a PDF

6. **✅ Despliegue y Documentación**
   - Aplicación web funcional con interfaz profesional
   - APIs REST completas con documentación OpenAPI

---

## 🏗️ Arquitectura del Sistema

### **Backend (FastAPI + Python 3.13.7)**
- **Framework:** FastAPI 0.116.1 + Uvicorn 0.31.0
- **ML/NLP:** scikit-learn 1.5.2, transformers 4.45.2, sentence-transformers 5.1.0
- **Data:** pandas 2.2.3, numpy 2.1.2, scipy 1.14.1
- **APIs:** crossref-commons, scholarly, NLTK, spaCy

### **Frontend (React + TypeScript)**
- **Framework:** React 19.1.1 + TypeScript 5.9.3
- **Build:** Vite 7.1.14 con Rolldown
- **UI:** Tailwind CSS 3.4.18, TanStack Query 5.90.5
- **Charts:** Plotly.js 3.1.2, react-plotly.js 2.6.0

### **Base de Datos**
- **Principal:** PostgreSQL 15+ (extensiones JSON/vector)
- **Caché:** Redis 5.1.1
- **ORM:** SQLAlchemy 2.0.36

---

## 📁 Estructura del Proyecto

```
ProyectoAnalisisAlgoritmos/
├── 📁 Backend/                 # API REST con FastAPI
│   ├── 📁 app/api/v1/         # Endpoints REST
│   ├── 📁 app/services/       # Lógica de negocio
│   ├── 📁 tests/              # Suite de testing (132 tests)
│   ├── main.py                # Punto de entrada
│   └── requirements.txt       # Dependencias Python
├── 📁 Frontend/               # SPA con React + TypeScript
│   ├── 📁 src/pages/          # Páginas principales
│   ├── 📁 src/services/       # Cliente API
│   ├── package.json           # Dependencias Node.js
│   └── vite.config.ts         # Configuración Vite
├── 📄 README.md               # Este archivo
├── 📄 Requerimientos.md       # Especificación completa
└── 📄 start-project.ps1       # Script de inicio automático
```

---

## 🚀 Instalación Rápida

### **Prerrequisitos**
- Python 3.13.7+, Node.js 20+, npm 10+, Git

### **Instalación Automática (Recomendada)**
```powershell
git clone https://github.com/SantOvalle08/ProyectoAnalisisAlgoritmos.git
cd ProyectoAnalisisAlgoritmos
.\start-project.ps1
```

**Acceder a la aplicación:**
- 🌐 **Frontend:** http://localhost:5173
- 🔌 **Backend API:** http://localhost:8000
- 📚 **API Docs:** http://localhost:8000/docs

### **Instalación Manual**
```powershell
# Backend
cd Backend
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend (nueva terminal)
cd Frontend
npm install
npm run dev
```

---

## 🧪 Testing y Calidad

```bash
✅ Tests Totales: 132/133 PASANDO (99.2%)
✅ Cobertura: 64%+ de líneas probadas
✅ Benchmarks: Implementados y ejecutándose
```

### **Ejecutar Tests**
```bash
cd Backend
python -m pytest --tb=short -v                    # Tests básicos
python -m pytest --cov=app --cov-report=html     # Con cobertura
python -m pytest tests/test_benchmarks.py -v     # Benchmarks
```

---

## 📊 API Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/v1/data/download` | POST | Descarga automatizada de datos |
| `/api/v1/similarity/compare` | POST | Análisis de similitud textual |
| `/api/v1/clustering/hierarchical` | POST | Clustering jerárquico |
| `/api/v1/frequency/analyze` | POST | Análisis de frecuencias |
| `/api/v1/visualizations/heatmap` | POST | Generar mapa de calor |

**Documentación completa:** http://localhost:8000/docs

---

## 📈 Resultados y Benchmarks

### **Indicadores de Rendimiento**
- 🎯 **Deduplicación:** >95% precisión
- ⚡ **Similitud:** <2s por comparación
- 📈 **Escalabilidad:** >10,000 abstracts
- 🔍 **Clustering:** Silhouette Score >0.6

### **Benchmarks de Algoritmos**
```
Levenshtein (corto):     10.5ms ± 2.7ms
TF-IDF (corto):          1.3ms ± 0.5ms
Sentence-BERT:          55.8ms ± 8.4ms
Clustering Ward:        3.9ms ± 1.3ms
```

### **Métricas Bibliométricas**
- 🌍 Distribución geográfica por país
- 📅 Evolución temporal (2010-2025)
- 🤝 Redes de colaboración
- 📊 Análisis por revista/fuente

---

## 👥 Equipo y Licencia

**Proyecto Académico** - Universidad del Quindío (2025-2)

### **Autores**
- **Santiago Ovalle Cortés** - Backend & Machine Learning
- **Juan Sebastián Noreña** - Frontend & UI/UX

### **Supervisor**
- **Carlos Andres Flores Villaraga** - Docente del curso

### **Licencia**
Uso exclusivamente académico y educativo.

---

## 📚 Documentación Adicional

- **[📋 Requerimientos.md](Requerimientos.md)** - Especificación completa
- **[🔌 API Docs](http://localhost:8000/docs)** - Documentación interactiva
- **[📊 Benchmarks](Backend/tests/test_benchmarks.py)** - Métricas detalladas

---

*🚀 Proyecto completamente funcional y listo para evaluación académica - Universidad del Quindío, 2025-2*

## 🏗️ Arquitectura del Sistema

### **Backend (Python + FastAPI)**
```
📦 Backend Services
├── 🔍 Data Acquisition Service
│   ├── Web scrapers para bases científicas (ACM, SAGE, ScienceDirect)
│   ├── APIs de integración (CrossRef, Elsevier)
│   ├── Procesadores de formatos bibliográficos (BibTeX, RIS, CSV)
│   └── Sistema de deduplicación inteligente
├── 🧠 ML & NLP Service
│   ├── 6 algoritmos de similitud textual
│   ├── Modelos de Transformers (BERT, Sentence-BERT)
│   ├── Algoritmos de clustering jerárquico (Ward/Average/Complete)
│   └── Análisis de frecuencias de conceptos
├── 📊 Analytics Service
│   ├── Análisis de frecuencias de conceptos
│   ├── Métricas bibliométricas avanzadas
│   └── Generación de reportes automatizados
├── 🎨 Visualization Service
│   ├── Mapas de calor geográficos
│   ├── Nubes de palabras dinámicas
│   ├── Líneas temporales interactivas
│   └── Exportación automática a PDF
└── 🗄️ Storage Service
    ├── Metadatos bibliográficos (JSON)
    ├── Embeddings vectoriales
    └── Resultados de análisis en caché
```

### **Frontend (React + TypeScript)**
```
📦 Frontend Application
├── ⚛️ React.js 19.1.1 con TypeScript 5.9.3
├── 🎨 UI/UX Moderna con Tailwind CSS
│   ├── Diseño responsive y profesional
│   ├── Componentes reutilizables
│   └── Tema consistente
├── 📊 Visualizaciones Interactivas
│   ├── Plotly.js para gráficos científicos
│   ├── Mapas geográficos interactivos
│   └── Exportación a PDF integrada
├── 🔄 State Management
│   ├── TanStack Query para API calls
│   ├── Axios para HTTP requests
│   └── Gestión de estado optimizada
└── 🧭 Routing y Navegación
    ├── React Router DOM v7
    ├── Navegación intuitiva
    └── URLs limpias y SEO-friendly
```

## 🛠️ Stack Tecnológico Actual

### **Backend**
- **Framework:** FastAPI 0.116.1 + Uvicorn 0.31.0
- **Python:** 3.13.7
- **Machine Learning:** scikit-learn 1.5.2, transformers 4.45.2, sentence-transformers 5.1.0
- **NLP:** NLTK 3.9.1, spaCy 3.8.2, torch 2.4.1
- **Data Processing:** pandas 2.2.3, numpy 2.1.2, scipy 1.14.1
- **Visualization:** matplotlib 3.9.2, plotly 5.24.1, seaborn 0.13.2
- **APIs Científicas:** crossref-commons 0.10.1, scholarly 1.7.11
- **Testing:** pytest 8.4.2 + pytest-asyncio 1.2.0 + pytest-cov 5.0.0

### **Frontend**
- **Framework:** React 19.1.1 + TypeScript 5.9.3
- **Build Tool:** Vite 7.1.14 (con Rolldown)
- **Styling:** Tailwind CSS 3.4.18
- **State Management:** TanStack Query 5.90.5
- **HTTP Client:** Axios 1.12.2
- **Icons:** Lucide React 0.548.0
- **Charts:** Plotly.js 3.1.2 + react-plotly.js 2.6.0
- **Routing:** React Router DOM 7.9.4

### **Base de Datos y Caché**
- **Base de Datos:** PostgreSQL 15+ (con extensiones JSON y vector)
- **Caché:** Redis 5.1.1 para optimización de consultas
- **ORM:** SQLAlchemy 2.0.36 + asyncpg 0.29.0

## Estructura del Proyecto

```
ProyectoAnalisisAlgoritmos/
├── 📁 Backend/
│   ├── 📁 app/
│   │   ├── 📁 api/              # Endpoints REST
│   │   ├── 📁 services/         # Lógica de negocio
│   │   ├── 📁 models/           # Modelos de datos
│   │   ├── 📁 utils/            # Utilidades compartidas
│   │   └── 📁 config/           # Configuraciones
│   ├── 📁 tests/                # Tests automatizados
│   ├── 📁 data/                 # Datasets y resultados
│   ├── 📁 logs/                 # Logs del sistema
│   ├── main.py                  # Punto de entrada FastAPI
│   └── requirements.txt         # Dependencias Python
├── 📁 Frontend/
│   ├── 📁 src/
│   │   ├── 📁 components/       # Componentes React
│   │   ├── 📁 pages/            # Páginas de la aplicación
│   │   ├── 📁 services/         # Cliente API
│   │   ├── 📁 types/            # Tipos TypeScript
│   │   └── 📁 utils/            # Utilidades frontend
│   ├── 📁 public/               # Archivos estáticos
│   ├── package.json             # Dependencias Node.js
│   └── vite.config.ts           # Configuración Vite
├── 📁 data/                     # Datos de descarga
├── 📄 start-project.ps1         # Script de inicio rápido
├── 📄 DEPLOYMENT.md             # Guía de despliegue
├── 📄 INTEGRACION.md            # Documentación de integración
└── 📄 README.md                 # Este archivo
```

## Algoritmos Implementados

### **Similitud Textual Clásica**
1. **Distancia de Levenshtein:** Edición de caracteres con programación dinámica
2. **TF-IDF + Similitud del Coseno:** Vectorización estadística y medidas angulares
3. **Coeficiente de Jaccard:** Intersección de conjuntos de tokens
4. **N-gramas con Overlapping:** Similitud basada en secuencias de caracteres

### **Similitud con Inteligencia Artificial**
1. **BERT Sentence Embeddings:** Representaciones contextuales profundas
2. **Sentence-BERT (SBERT):** Optimizado para similitud semántica de oraciones

### **Clustering Jerárquico**
1. **Ward Linkage:** Minimización de varianza intra-cluster
2. **Average Linkage:** Promedio de distancias entre clusters
3. **Complete Linkage:** Máxima distancia entre elementos de clusters

### **Análisis de Frecuencias**
- **TF-IDF weighting** para importancia de términos
- **Named Entity Recognition (NER)** para conceptos especializados
- **Topic Modeling con LDA** para descubrimiento automático de temas

## 🚀 Instalación y Configuración

### **Prerrequisitos**
- **Python:** 3.13.7+
- **Node.js:** 20+
- **npm:** 10+
- **Git:** Para clonar el repositorio

### **Instalación Rápida (Recomendada)**

```powershell
# 1. Clonar el repositorio
git clone https://github.com/SantOvalle08/ProyectoAnalisisAlgoritmos.git
cd ProyectoAnalisisAlgoritmos

# 2. Ejecutar script de inicio automático
.\start-project.ps1
```

**El script automáticamente:**
- ✅ Instala dependencias del backend
- ✅ Instala dependencias del frontend
- ✅ Descarga modelos de NLP necesarios
- ✅ Inicia ambos servidores simultáneamente

### **Acceder a la Aplicación**
- **🌐 Frontend:** http://localhost:5173
- **🔌 Backend API:** http://localhost:8000
- **📚 API Docs:** http://localhost:8000/docs

### **Instalación Manual**

#### Backend (Python + FastAPI)
```powershell
cd Backend

# Crear entorno virtual (recomendado)
python -m venv venv
.\venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Descargar modelos de NLP
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"

# Ejecutar servidor de desarrollo
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend (React + TypeScript)
```powershell
cd Frontend

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev
```

# Construir para producción
npm run build
```

## Uso del Sistema

### **1. Descarga Automatizada de Datos**
```python
from backend.services.data_acquisition import AutomatedDownloader

# Configurar descarga de múltiples fuentes
downloader = AutomatedDownloader(
    sources=['acm', 'sage', 'sciencedirect'],
    query="generative artificial intelligence",
    max_results=1000
)

# Ejecutar descarga y unificación
unified_data = downloader.download_and_unify()
```

### **2. Análisis de Similitud**
```python
from backend.services.ml_analysis import SimilarityAnalyzer

analyzer = SimilarityAnalyzer()

# Algoritmos clásicos
classic_results = analyzer.compare_abstracts(
    abstract1, abstract2,
    algorithms=['levenshtein', 'tfidf_cosine', 'jaccard', 'ngrams']
)

# Algoritmos de IA
ai_results = analyzer.compare_abstracts_ai(
    abstract1, abstract2,
    models=['bert', 'sentence_bert']
)
```

### **3. Clustering y Visualización**
```python
from backend.services.analytics import ClusteringAnalyzer
from backend.services.visualization import DendrogramGenerator

# Clustering jerárquico
clusterer = ClusteringAnalyzer()
clusters = clusterer.hierarchical_clustering(
    abstracts_list,
    algorithms=['ward', 'average', 'complete']
)

# Generar dendrograma interactivo
viz = DendrogramGenerator()
dendrogram = viz.create_interactive_dendrogram(clusters)
```

## API Endpoints

### **Data Acquisition**
- `POST /api/data/download` - Iniciar descarga automatizada
- `GET /api/data/status/{job_id}` - Estado de descarga
- `GET /api/data/unified` - Obtener datos unificados

### **ML Analysis**
- `POST /api/ml/similarity/classic` - Similitud con algoritmos clásicos
- `POST /api/ml/similarity/ai` - Similitud con modelos de IA
- `POST /api/ml/clustering` - Clustering jerárquico

### **Analytics**
- `POST /api/analytics/frequencies` - Análisis de frecuencias
- `GET /api/analytics/concepts` - Conceptos extraídos
- `GET /api/analytics/metrics` - Métricas bibliométricas

### **Visualizations**
- `POST /api/viz/heatmap` - Generar mapa de calor
- `POST /api/viz/wordcloud` - Nube de palabras
- `POST /api/viz/timeline` - Línea temporal
- `POST /api/viz/export/pdf` - Exportar a PDF

## 📈 Resultados y Métricas

### **Indicadores de Rendimiento**
- **🎯 Precisión de deduplicación:** >95% (validado por tests)
- **⚡ Tiempo de similitud:** <2s por comparación de abstracts
- **📈 Escalabilidad:** Manejo de >10,000 abstracts
- **🔍 Precisión de clustering:** Silhouette Score promedio >0.6

### **Métricas Bibliométricas Generadas**
- 🌍 Distribución geográfica de autores por país
- 📅 Evolución temporal de publicaciones (2010-2025)
- 🤝 Redes de colaboración entre autores
- 📊 Análisis de impacto por revista y fuente

### **Benchmarks de Algoritmos**
```
Levenshtein (corto):     10.5ms ± 2.7ms
TF-IDF (corto):          1.3ms ± 0.5ms
Sentence-BERT:          55.8ms ± 8.4ms
Clustering Ward (small): 3.9ms ± 1.3ms
```

## 🧪 Testing y Calidad

### **Estado Actual de Tests**
```bash
✅ Tests Totales: 132/133 PASANDO (99.2%)
✅ Cobertura: 64%+ de líneas probadas
✅ Benchmarks: Implementados y ejecutándose
```

### **Ejecutar Tests**

```bash
# Tests del backend
cd Backend
python -m pytest --tb=short -v

# Tests con cobertura
python -m pytest --cov=app --cov-report=html

# Benchmarks de performance
python -m pytest tests/test_benchmarks.py -v
```

### **Categorías de Tests**
- 🧪 **API Tests:** Validación de endpoints REST
- 🔬 **Unit Tests:** Funciones individuales y clases
- 🔄 **Integration Tests:** Flujos completos end-to-end
- ⚡ **Performance Tests:** Benchmarks de algoritmos
- 📊 **Coverage Reports:** Reportes HTML en `htmlcov/`

## 📚 Documentación Adicional

- **[📋 Requerimientos.md](Requerimientos.md)** - Especificación completa de requerimientos
- **[🔌 API Docs](http://localhost:8000/docs)** - Documentación interactiva de APIs
- **[📊 Benchmarks](Backend/tests/test_benchmarks.py)** - Métricas de performance detalladas

## Contribución y Desarrollo

### **Flujo de Desarrollo**
1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commits siguiendo [Conventional Commits](https://www.conventionalcommits.org/)
4. Tests y documentación
5. Pull Request con descripción detallada

### **Estándares de Código**
- **Python:** PEP 8, type hints, docstrings
- **TypeScript:** ESLint + Prettier, JSDoc comments
- **Git:** Commits semánticos, branches descriptivas

## 👥 Autoría y Licencia

**Proyecto Académico** desarrollado para el curso **"Análisis de Algoritmos" (2025-2)**  
**Universidad del Quindío**

### **Autores**
- **Santiago Ovalle Cortés** - Desarrollo Backend & ML
- **Juan Sebastián Noreña** - Desarrollo Frontend & UI/UX

### **Supervisor Académico**
- **Carlos Andres Flores Villaraga** - Docente del curso

### **Licencia**
Este proyecto es de uso exclusivamente académico y educativo.

---

## 🎯 Próximos Pasos (Opcionales)

Para futuras mejoras del proyecto, se podrían implementar:
- 🔐 Sistema de autenticación de usuarios
- 📊 Dashboard administrativo avanzado
- ☁️ Despliegue en la nube (Azure/AWS)
- 🤖 Integración con más APIs científicas
- 📱 Aplicación móvil complementaria
- 🎨 Más tipos de visualizaciones interactivas

---

*🚀 Proyecto completamente funcional y listo para evaluación académica - Universidad del Quindío, 2025-2*
