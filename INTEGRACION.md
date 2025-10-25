# Integración Backend-Frontend

Este documento describe cómo conectar el frontend con el backend del proyecto.

## 🔧 Configuración

### 1. Variables de Entorno

Copia el archivo de ejemplo y ajusta la URL del backend:

```bash
cd Frontend
cp .env.example .env
```

Edita `.env` y configura:
```env
VITE_API_URL=http://localhost:8000
```

### 2. Iniciar el Proyecto Completo

**Opción A: Script Automático (Windows)**
```powershell
.\start-project.ps1
```

**Opción B: Manual**

Terminal 1 - Backend:
```bash
cd Backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 - Frontend:
```bash
cd Frontend
npm run dev
```

## 📡 Endpoints Disponibles

### Backend (http://localhost:8000)

- **Documentación Interactiva**: http://localhost:8000/docs
- **API Base**: http://localhost:8000/api

#### Adquisición de Datos
- `POST /api/download/start` - Iniciar descarga de publicaciones
- `GET /api/download/status/{job_id}` - Consultar estado de descarga
- `GET /api/download/jobs` - Listar trabajos
- `GET /api/download/file/{job_id}/{format}` - Descargar archivo

#### Similitud Textual
- `POST /api/similarity/compare` - Comparar dos textos
- `POST /api/similarity/compare-all` - Comparar con todos los algoritmos
- `GET /api/similarity/algorithms` - Listar algoritmos disponibles

#### Análisis de Frecuencia
- `POST /api/frequency/extract` - Extraer keywords de abstracts
- `POST /api/frequency/concepts` - Analizar frecuencia de conceptos

#### Clustering
- `POST /api/clustering/analyze` - Realizar clustering jerárquico
- `POST /api/clustering/recommend` - Obtener recomendaciones de clusters

#### Visualizaciones
- `POST /api/visualizations/wordcloud` - Generar nube de palabras
- `POST /api/visualizations/heatmap` - Generar mapa de calor geográfico
- `POST /api/visualizations/timeline` - Generar línea de tiempo
- `POST /api/visualizations/export-pdf` - Exportar visualizaciones a PDF

### Frontend (http://localhost:5173)

- **Home**: `/` - Página de inicio
- **Data Acquisition**: `/data-acquisition` - Descarga de publicaciones
- **Similarity**: `/similarity` - Análisis de similitud textual
- **Frequency**: `/frequency` - Análisis de frecuencia
- **Clustering**: `/clustering` - Clustering jerárquico
- **Visualizations**: `/visualizations` - Generación de visualizaciones

## 🔌 Servicios del Frontend

Todos los servicios están en `Frontend/src/services/`:

### `api.ts` - Cliente HTTP Base
```typescript
import api from './services/api';

// Ejemplo de uso
const response = await api.get('/endpoint');
const data = await api.post('/endpoint', { payload });
```

### `dataAcquisition.ts` - Adquisición de Datos
```typescript
import dataAcquisitionService from './services/dataAcquisition';

// Iniciar descarga
const job = await dataAcquisitionService.startDownload({
  query: 'machine learning',
  sources: ['crossref', 'acm'],
  max_results: 100
});

// Consultar estado
const status = await dataAcquisitionService.getJobStatus(job.job_id);
```

### `similarity.ts` - Similitud Textual
```typescript
import similarityService from './services/similarity';

// Comparar dos textos
const result = await similarityService.compare({
  text1: 'Machine learning is...',
  text2: 'AI encompasses...',
  algorithm: 'tfidf'
});

// Comparar con todos
const results = await similarityService.compareAll(text1, text2);
```

### `frequency.ts` - Análisis de Frecuencia
```typescript
import frequencyService from './services/frequency';

// Extraer keywords
const keywords = await frequencyService.extractKeywords({
  abstracts: ['Abstract 1...', 'Abstract 2...'],
  max_keywords: 10,
  use_tfidf: true
});

// Analizar conceptos
const concepts = await frequencyService.analyzeConcepts({
  abstracts: ['Abstract 1...', 'Abstract 2...'],
  concepts: ['machine learning', 'AI']
});
```

### `clustering.ts` - Clustering
```typescript
import clusteringService from './services/clustering';

// Realizar clustering
const result = await clusteringService.performClustering({
  abstracts: ['Abstract 1...', 'Abstract 2...'],
  method: 'ward',
  n_clusters: 3
});
```

### `visualization.ts` - Visualizaciones
```typescript
import visualizationService from './services/visualization';

// Generar word cloud
const wordcloud = await visualizationService.generateWordCloud({
  publications: [...],
  max_words: 50
});

// Generar heatmap
const heatmap = await visualizationService.generateHeatmap({
  publications: [...],
  map_type: 'choropleth'
});

// Generar timeline
const timeline = await visualizationService.generateTimeline({
  publications: [...],
  group_by_journal: false
});
```

## 🧪 Pruebas de Integración

### 1. Verificar Backend
```bash
curl http://localhost:8000/health
```

### 2. Verificar Conexión desde Frontend
Abre la consola del navegador en http://localhost:5173 y ejecuta:
```javascript
fetch('http://localhost:8000/api/similarity/algorithms')
  .then(r => r.json())
  .then(console.log)
```

### 3. Prueba End-to-End
1. Navega a http://localhost:5173/data-acquisition
2. Ingresa una query: "machine learning"
3. Selecciona fuentes: CrossRef, ACM
4. Haz clic en "Iniciar Descarga"
5. Observa el progreso en tiempo real
6. Descarga los resultados

## 🐛 Troubleshooting

### Error: CORS
Si ves errores de CORS, verifica que el backend tenga configurado:
```python
# Backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Error: Connection Refused
- Verifica que el backend esté corriendo en el puerto 8000
- Verifica que `.env` tenga la URL correcta

### Error: 404 Not Found
- Verifica que las rutas en los servicios coincidan con las del backend
- Revisa la documentación en http://localhost:8000/docs

## 📊 Flujo de Datos

```
Usuario (Frontend)
    ↓
React Component
    ↓
React Query (useMutation/useQuery)
    ↓
Service Layer (e.g., dataAcquisitionService)
    ↓
Axios HTTP Client (api.ts)
    ↓
Backend API (FastAPI)
    ↓
Servicios Backend
    ↓
Base de Datos / APIs Externas
```

## 🔐 Seguridad

- El backend valida todas las entradas con Pydantic
- El frontend sanitiza datos antes de enviarlos
- CORS está configurado solo para orígenes permitidos
- No se exponen credenciales en el código

## 📝 Logs

**Backend**: Los logs aparecen en la terminal del backend
**Frontend**: Usa la consola del navegador (F12)

Para habilitar logs detallados en el frontend:
```typescript
// En services/api.ts
console.log('Request:', config);
console.log('Response:', response);
```
