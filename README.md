# Proyecto Análisis de Algoritmos Aplicados a Bibliometría

Plataforma web automatizada para el análisis bibliométrico avanzado de publicaciones científicas sobre inteligencia artificial generativa, desarrollada para el curso "Análisis de Algoritmos" (2025-2), Universidad del Quindío.

## Descripción del Proyecto

Sistema integral de análisis bibliométrico que implementa algoritmos de machine learning y procesamiento de lenguaje natural para el estudio computacional de la producción científica en el dominio de "Inteligencia Artificial Generativa en Educación".

### Alcance y Dominio
- **Dominio de conocimiento:** Inteligencia Artificial Generativa
- **Cadena de búsqueda:** "generative artificial intelligence"
- **Fuentes de datos:** Bases científicas de la Universidad del Quindío (ACM, SAGE, ScienceDirect)
- **Enfoque:** Análisis bibliométrico automatizado con visualizaciones interactivas

## Requerimientos Funcionales

### 1. **Automatización de Descarga de Datos**
- Integración automatizada con múltiples bases de datos científicas
- Unificación inteligente de formatos (BibTex, RIS, CSV)
- Eliminación automática de duplicados con preservación de metadatos
- Generación de reportes de publicaciones eliminadas

### 2. **Algoritmos de Similitud Textual**
- **4 Algoritmos Clásicos:** Distancia de Levenshtein, TF-IDF + Coseno, Jaccard, N-gramas
- **2 Algoritmos de IA:** BERT Sentence Embeddings, Sentence-BERT
- Análisis matemático detallado paso a paso de cada algoritmo
- Comparación entre abstracts científicos con métricas de precisión

### 3. **Análisis de Frecuencias de Conceptos**
- Categoría predefinida: "Concepts of Generative AI in Education" (15 términos)
- Extracción automática de frecuencias en abstracts
- Generación de palabras asociadas mediante NLP avanzado
- Análisis de precisión y relevancia de nuevos términos identificados

### 4. **Clustering Jerárquico Avanzado**
- **3 Algoritmos:** Ward Linkage, Average Linkage, Complete Linkage
- Preprocesamiento avanzado de texto científico
- Generación de dendrogramas interactivos
- Evaluación comparativa de coherencia de agrupamientos

### 5. **Visualizaciones Científicas Interactivas**
- **Mapas de calor geográficos** de distribución por primer autor
- **Nubes de palabras dinámicas** con actualización automática
- **Líneas temporales interactivas** por año y revista
- **Exportación automática a PDF** de todas las visualizaciones

### 6. **Despliegue y Documentación Técnica**
- Aplicación web desplegada con interfaz profesional
- Documentación técnica completa con arquitectura del sistema
- Guías de implementación para cada algoritmo

## Arquitectura del Sistema

### **Backend**
```
📦 Backend Services
├── 🔍 Data Acquisition Service (Python + FastAPI)
│   ├── Web scrapers para bases científicas
│   ├── APIs de integración (CrossRef, Elsevier)
│   └── Procesadores de formatos bibliográficos
├── 🧠 ML & NLP Service (Python + FastAPI)
│   ├── Algoritmos de similitud textual
│   ├── Modelos de Transformers (BERT, Sentence-BERT)
│   └── Algoritmos de clustering jerárquico
├── 📊 Analytics Service (Python + FastAPI)
│   ├── Análisis de frecuencias de conceptos
│   ├── Métricas bibliométricas
│   └── Generación de reportes
└── 🗄️ Database Service (PostgreSQL + Redis)
    ├── Metadatos bibliográficos (JSON)
    ├── Embeddings vectoriales
    └── Resultados de análisis
```

### **Frontend (Aplicación Web)**
```
📦 Frontend Application
├── ⚛️ React.js 18+ con TypeScript
├── 📈 Visualizaciones Interactivas
│   ├── D3.js para dendrogramas
│   ├── Plotly.js para mapas de calor
│   ├── Leaflet para mapas geográficos
│   └── Recharts para líneas temporales
├── 🎨 UI/UX Profesional
│   ├── Material-UI (MUI)
│   ├── React Hook Form
│   └── React Router
└── 📄 Exportación y Reportes
    ├── jsPDF para generación PDF
    └── Canvas para captura de visualizaciones
```

## Stack Tecnológico Completo

### **Lenguajes y Frameworks**
- **Backend:** Python 3.11+ (FastAPI, uvicorn)
- **Frontend:** TypeScript, React.js 18+, Next.js
- **Base de Datos:** PostgreSQL 15+ con extensiones JSON y Vector
- **Caché:** Redis para optimización de consultas

### **Bibliotecas de Machine Learning & NLP**
```python
# Procesamiento de Datos
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0

# Machine Learning
scikit-learn>=1.3.0
transformers>=4.30.0
sentence-transformers>=2.2.0
torch>=2.0.0

# NLP y Texto
nltk>=3.8.0
spacy>=3.6.0
gensim>=4.3.0
python-Levenshtein>=0.21.0

# Clustering y Similitud
scipy.cluster.hierarchy
sklearn.cluster
sklearn.metrics
```

### **APIs y Conectores Científicos**
```python
# Bases de Datos Científicas
crossref-commons>=0.10.0
scholarly>=1.7.0
habanero>=1.2.0
pyElsevier>=0.8.0

# Procesamiento Bibliográfico
pybtex>=0.24.0
rispy>=0.7.0
beautifulsoup4>=4.12.0
scrapy>=2.9.0
```

### **Visualización y Frontend**
```javascript
// Core Framework
react: "^18.2.0"
typescript: "^5.1.0"
next: "^13.4.0"

// Visualizaciones
d3: "^7.8.0"
plotly.js: "^2.24.0"
react-leaflet: "^4.2.0"
recharts: "^2.7.0"

// UI/UX
@mui/material: "^5.13.0"
react-hook-form: "^7.45.0"
react-query: "^3.39.0"

// Exportación
jspdf: "^2.5.0"
html2canvas: "^1.4.0"
```

### **Base de Datos y Infraestructura**
```sql
-- PostgreSQL con extensiones especializadas
CREATE EXTENSION IF NOT EXISTS pg_trgm;    -- Búsqueda fuzzy
CREATE EXTENSION IF NOT EXISTS vector;     -- Embeddings vectoriales
CREATE EXTENSION IF NOT EXISTS btree_gin;  -- Índices optimizados
```

### **Despliegue y DevOps**
- **Contenedorización:** Docker + Docker Compose
- **Orquestación:** Kubernetes (opcional)
- **CI/CD:** GitHub Actions
- **Monitoreo:** Prometheus + Grafana
- **Cloud:** AWS/GCP con servicios gestionados

## Estructura del Proyecto

```
ProyectoAnalisisAlgoritmos/
├── 📁 backend/
│   ├── 📁 services/
│   │   ├── data_acquisition/     # Descarga y unificación de datos
│   │   ├── ml_analysis/          # Algoritmos ML y similitud
│   │   ├── analytics/            # Métricas y frecuencias
│   │   └── visualization/        # Generación de visualizaciones
│   ├── 📁 models/               # Modelos de datos
│   ├── 📁 utils/                # Utilidades compartidas
│   └── 📁 config/               # Configuraciones
├── 📁 frontend/
│   ├── 📁 components/           # Componentes React
│   ├── 📁 pages/                # Páginas de la aplicación
│   ├── 📁 hooks/                # Custom hooks
│   ├── 📁 utils/                # Utilidades frontend
│   └── 📁 styles/               # Estilos y temas
├── 📁 database/
│   ├── 📁 migrations/           # Migraciones de BD
│   ├── 📁 schemas/              # Esquemas PostgreSQL
│   └── 📁 seeds/                # Datos de prueba
├── 📁 docs/
│   ├── 📁 architecture/         # Documentación técnica
│   ├── 📁 algorithms/           # Explicaciones matemáticas
│   └── 📁 api/                  # Documentación API
├── 📁 notebooks/                # Jupyter Notebooks de análisis
├── 📁 data/                     # Datasets y resultados
├── 📁 tests/                    # Tests automatizados
├── 📁 docker/                   # Configuraciones Docker
├── requirements.txt             # Dependencias Python
├── package.json                 # Dependencias Node.js
└── docker-compose.yml           # Orquestación de servicios
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

## Instalación y Configuración

### **Prerrequisitos**
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose (opcional)
- Git

### **Instalación Rápida con Docker**
```bash
# Clonar el repositorio
git clone https://github.com/SantOvalle08/ProyectoAnalisisAlgoritmos.git
cd ProyectoAnalisisAlgoritmos

# Levantar todos los servicios
docker-compose up -d

# La aplicación estará disponible en:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Base de datos: localhost:5432
```

### **Instalación Manual**

#### Backend (Python)
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
createdb bibliometric_analysis
python manage.py migrate

# Descargar modelos de NLP
python -m spacy download es_core_news_sm
python -m spacy download en_core_web_sm

# Ejecutar servidor
uvicorn main:app --reload --port 8000
```

#### Frontend (React)
```bash
cd frontend/

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env.local

# Ejecutar en desarrollo
npm run dev

# Construir para producción
npm run build
```

#### Base de Datos (PostgreSQL)
```sql
-- Crear base de datos
CREATE DATABASE bibliometric_analysis;

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS btree_gin;

-- Ejecutar migraciones
\i database/schemas/publications.sql
\i database/schemas/analysis_results.sql
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

## Resultados y Métricas

### **Indicadores de Rendimiento**
- **Precisión de eliminación de duplicados:** >95%
- **Tiempo de procesamiento de similitud:** <2s por comparación
- **Escalabilidad:** Manejo de >10,000 abstracts
- **Precisión de clustering:** Medida por Silhouette Score

### **Métricas Bibliométricas**
- Distribución geográfica de autores
- Evolución temporal de publicaciones
- Redes de colaboración entre autores
- Análisis de impacto por revista

## Testing y Calidad

```bash
# Tests backend
pytest backend/tests/ --cov=backend/

# Tests frontend
npm test -- --coverage

# Linting y formateo
black backend/
flake8 backend/
eslint frontend/src/
prettier --write frontend/src/
```

## Documentación Técnica

La documentación completa está disponible en:
- **[Arquitectura del Sistema](docs/architecture/)** - Diseño técnico detallado
- **[Algoritmos Implementados](docs/algorithms/)** - Explicaciones matemáticas
- **[API Reference](docs/api/)** - Especificaciones de endpoints
- **[Guía de Despliegue](docs/deployment/)** - Instrucciones de producción

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

## Licencia y Autoría

Este proyecto ha sido desarrollado para fines académicos en el marco del curso "Análisis de Algoritmos", Universidad del Quindío, 2025-2.

**Autores:**
- Santiago Ovalle Cortés
- Juan Sebastián Noreña

**Supervisor Académico:** Carlos Andres Flores Villaraga 

---

*Proyecto desarrollado para el curso Análisis de Algoritmos, Universidad del Quindío, 2025-2.*
