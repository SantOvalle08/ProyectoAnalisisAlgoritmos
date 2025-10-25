# 🧪 Plan de Pruebas de Integración Backend-Frontend

## ✅ Paso 2: Integración Backend-Frontend - COMPLETADO

### Servicios Implementados

- ✅ `frequency.ts` - Servicio de análisis de frecuencia
- ✅ `clustering.ts` - Servicio de clustering jerárquico  
- ✅ Actualización de `FrequencyPage.tsx` - Conexión con API real
- ✅ Actualización de `ClusteringPage.tsx` - Conexión con API real
- ✅ Actualización de `VisualizationsPage.tsx` - Conexión con API real
- ✅ Script `start-project.ps1` - Inicio automatizado del proyecto
- ✅ Archivo `.env.example` - Configuración de variables de entorno
- ✅ Documentación `INTEGRACION.md` - Guía completa de integración

### Estado de los Servidores

✅ **Backend**: http://localhost:8000
- Servidor FastAPI ejecutándose correctamente
- Uvicorn en modo reload
- Logs activos y funcionales

⏳ **Frontend**: http://localhost:5173
- Servidor Vite ya configurado y funcionando
- Todas las páginas implementadas
- Servicios conectados a la API

## 📋 Checklist de Integración

### Backend
- [x] Servidor corriendo en puerto 8000
- [x] CORS configurado para http://localhost:5173
- [x] Endpoints documentados en /docs
- [x] Todos los servicios implementados
- [x] Base de datos configurada

### Frontend  
- [x] Archivo .env con VITE_API_URL configurado
- [x] Cliente Axios configurado en services/api.ts
- [x] Servicios implementados:
  - [x] dataAcquisition.ts
  - [x] similarity.ts
  - [x] frequency.ts
  - [x] clustering.ts
  - [x] visualization.ts
- [x] Páginas conectadas a servicios reales:
  - [x] DataAcquisitionPage
  - [x] SimilarityPage
  - [x] FrequencyPage
  - [x] ClusteringPage
  - [x] VisualizationsPage

### Conexión
- [x] Variables de entorno configuradas
- [x] Script de inicio creado
- [x] Documentación de integración completa

## 🧪 Pruebas a Realizar (Paso 1)

### 1. Pruebas de Conexión Básica

#### Test 1.1: Health Check del Backend
```bash
curl http://localhost:8000/health
```
**Resultado Esperado**: `{"status": "healthy"}`

#### Test 1.2: Listar Algoritmos de Similitud
```bash
curl http://localhost:8000/api/similarity/algorithms
```
**Resultado Esperado**: Lista de 6 algoritmos

#### Test 1.3: Listar Fuentes de Datos
```bash
curl http://localhost:8000/api/download/sources
```
**Resultado Esperado**: Lista de fuentes (CrossRef, ACM, etc.)

### 2. Pruebas End-to-End por Página

#### Test 2.1: Data Acquisition Page
**Pasos**:
1. Navegar a http://localhost:5173/data-acquisition
2. Ingresar query: "machine learning"
3. Seleccionar fuente: CrossRef
4. Max results: 10
5. Hacer clic en "Iniciar Descarga"
6. Observar progreso en tiempo real
7. Descargar archivo JSON

**Resultado Esperado**: 
- Job ID generado
- Progreso actualizado cada 2 segundos
- Descarga exitosa de archivo

#### Test 2.2: Similarity Page
**Pasos**:
1. Navegar a http://localhost:5173/similarity
2. Cargar textos de ejemplo
3. Seleccionar algoritmo: TF-IDF
4. Hacer clic en "Comparar Textos"
5. Verificar resultado de similitud

**Resultado Esperado**:
- Similitud entre 0 y 1
- Tiempo de ejecución mostrado
- Detalles técnicos disponibles

#### Test 2.3: Frequency Page
**Pasos**:
1. Navegar a http://localhost:5173/frequency
2. Cargar datos de ejemplo
3. Modo: Extracción de Keywords
4. Max keywords: 10
5. Usar TF-IDF: activado
6. Hacer clic en "Extraer Keywords"

**Resultado Esperado**:
- Tabla con keywords y frecuencias
- Gráfico de barras
- Opción de descarga CSV

#### Test 2.4: Clustering Page
**Pasos**:
1. Navegar a http://localhost:5173/clustering
2. Cargar datos de ejemplo
3. Método: Ward
4. Auto-detectar clusters: activado
5. Hacer clic en "Realizar Clustering"

**Resultado Esperado**:
- Número de clusters detectado
- Silhouette score calculado
- Asignación de documentos a clusters

#### Test 2.5: Visualizations Page
**Pasos**:
1. Navegar a http://localhost:5173/visualizations
2. Cargar JSON de ejemplo
3. Tipo: Nube de Palabras
4. Max words: 50
5. Hacer clic en "Generar Visualización"

**Resultado Esperado**:
- Preview de word cloud
- Top términos mostrados
- Opción de descarga HTML

### 3. Pruebas de Manejo de Errores

#### Test 3.1: Request Inválido
**Acción**: Enviar datos incompletos desde el frontend
**Resultado Esperado**: Mensaje de error claro en UI

#### Test 3.2: Backend No Disponible
**Acción**: Detener backend y hacer request desde frontend
**Resultado Esperado**: Mensaje "Error al conectar con el servidor"

#### Test 3.3: Timeout
**Acción**: Iniciar descarga muy grande (>1000 results)
**Resultado Esperado**: Progreso mostrado, no timeout prematuro

### 4. Pruebas de Performance

#### Test 4.1: Carga de Página
**Métrica**: Tiempo de carga inicial < 2 segundos

#### Test 4.2: Request-Response
**Métrica**: Similitud simple < 500ms

#### Test 4.3: Descarga de Datos
**Métrica**: 100 publicaciones < 10 segundos

### 5. Pruebas de UI/UX

#### Test 5.1: Estados de Carga
**Verificar**: Spinners aparecen durante requests

#### Test 5.2: Estados de Error
**Verificar**: Mensajes de error son claros y útiles

#### Test 5.3: Responsive Design
**Verificar**: UI funciona en diferentes tamaños de pantalla

## 📊 Resultados de Pruebas

### Backend Status
```
✅ Servidor corriendo en http://0.0.0.0:8000
✅ UnifiedDownloader inicializado
✅ Reloader activo
✅ Sin errores en startup
```

### Frontend Status
```
⏳ Listo para iniciar pruebas
⏳ Todas las páginas implementadas
⏳ Servicios conectados
```

## 🔄 Próximos Pasos

### Inmediato (Paso 1)
1. [ ] Ejecutar batería completa de pruebas de integración
2. [ ] Verificar cada endpoint con datos reales
3. [ ] Documentar cualquier issue encontrado
4. [ ] Ajustar tipos TypeScript si es necesario
5. [ ] Validar manejo de errores

### Después (Paso 3 - Deployment)
1. [ ] Optimizar bundle del frontend
2. [ ] Configurar variables de entorno de producción
3. [ ] Preparar scripts de inicio
4. [ ] Documentación de deployment
5. [ ] Validación de tests completa

## 📝 Notas

- Backend iniciado exitosamente en puerto 8000
- Frontend ya funcionando en puerto 5173
- Todos los servicios del frontend ahora usan API real
- Documentación de integración completa en INTEGRACION.md
- Script de inicio automatizado creado (start-project.ps1)
