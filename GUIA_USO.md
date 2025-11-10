# 📖 GUÍA DE USO - Sistema de Análisis Bibliométrico

## Universidad del Quindío - Análisis de Algoritmos (2025-2)
**Autores:** Santiago Ovalle Cortés, Juan Sebastián Noreña, Santiago Londoño

---

## 🎯 ¿Qué hace este sistema?

Este sistema permite realizar **análisis bibliométrico automatizado** de publicaciones académicas sobre inteligencia artificial generativa. Incluye:

- 📥 **Descarga automática** de publicaciones desde fuentes académicas
- 🔍 **Análisis de similitud** con 6 algoritmos diferentes
- 🌳 **Clustering jerárquico** para agrupar publicaciones relacionadas
- 📊 **Análisis de frecuencias** de términos y conceptos clave
- 📈 **Visualizaciones** (nubes de palabras, mapas de calor, líneas de tiempo)

---

## 🚀 1. INSTALACIÓN

### Requisitos Previos
- Python 3.13+
- Node.js 18+
- Git

### Paso 1: Clonar el Repositorio
```powershell
git clone https://github.com/SantOvalle08/ProyectoAnalisisAlgoritmos.git
cd ProyectoAnalisisAlgoritmos
```

### Paso 2: Instalar Dependencias

**Backend (Python):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r Backend/requirements.txt
```

**Frontend (Node.js):**
```powershell
cd Frontend
npm install
cd ..
```

### Paso 3: Configurar Variables de Entorno

Crear archivo `.env` en la carpeta `Backend/` con:
```env
# APIs
ELSEVIER_API_KEY=tu_api_key_aqui
CROSSREF_API_EMAIL=tu_email@universidad.edu.co

# URLs institucionales
SAGE_INSTITUTIONAL_URL=https://search-sagepub-com.crai.referencistas.com/

# Selenium
SELENIUM_HEADLESS=True
```

---

## 🎮 2. EJECUCIÓN

### Opción 1: Inicio Automático (Recomendado)
```powershell
.\start-project.ps1
```

Esto iniciará automáticamente:
- Backend en http://localhost:8000
- Frontend en http://localhost:5173

### Opción 2: Inicio Manual

**Terminal 1 - Backend:**
```powershell
cd Backend
..\.venv\Scripts\uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```powershell
cd Frontend
npm run dev
```

---

## 📚 3. USAR EL SISTEMA

### 3.1 Adquisición de Datos

**Objetivo**: Descargar publicaciones académicas desde múltiples fuentes

1. Abrir: http://localhost:5173
2. Ir a **"Adquisición de Datos"**
3. Configurar búsqueda:
   - **Query**: `"generative artificial intelligence"`
   - **Fuentes**: CrossRef (recomendado)
   - **Máximo de resultados**: 50
4. Click en **"Descargar"**
5. Esperar a que se descarguen (aparecerá progreso)
6. Las publicaciones se guardan automáticamente

**Fuentes disponibles:**
- ✅ **CrossRef** (140M+ publicaciones, gratis, rápido)
- ⚠️ **ScienceDirect** (requiere API key válida)
- ⚠️ **SAGE** (requiere acceso institucional)
- ⚠️ **ACM** (requiere Selenium, más lento)

---

### 3.2 Análisis de Similitud

**Objetivo**: Comparar qué tan similares son las publicaciones entre sí

1. Ir a **"Análisis de Similitud"**
2. Seleccionar publicaciones a comparar
3. Elegir algoritmo:
   - **Levenshtein** - Distancia de edición (simple)
   - **TF-IDF** - Términos importantes (rápido)
   - **Jaccard** - Palabras en común (básico)
   - **N-gramas** - Secuencias de caracteres (bueno)
   - **BERT** - Inteligencia artificial (muy preciso, lento)
   - **Sentence-BERT** - IA optimizada (preciso, rápido)
4. Click en **"Calcular Similitud"**
5. Ver resultados:
   - **Matriz de similitud** (valores de 0 a 1)
   - **Pares más similares**
   - **Tiempo de ejecución**

**¿Cómo interpretar?**
- `0.0 = Completamente diferentes`
- `0.5 = Medianamente similares`
- `1.0 = Idénticas`

---

### 3.3 Clustering Jerárquico

**Objetivo**: Agrupar publicaciones por temática

1. Ir a **"Clustering"**
2. Seleccionar publicaciones a agrupar (mínimo 5)
3. Elegir método de linkage:
   - **Ward** - Varianza mínima (recomendado)
   - **Average** - Promedio de distancias
   - **Complete** - Máxima distancia
   - **Single** - Mínima distancia
4. Elegir número de clusters (2-10)
5. Click en **"Generar Clustering"**
6. Ver resultados:
   - **Dendrograma** - Árbol jerárquico
   - **Clusters identificados** - Grupos temáticos
   - **Publicaciones por cluster**

**Dendrograma:**
- El eje vertical muestra la distancia/similitud
- Mientras más cerca estén dos ramas, más similares son
- Puedes "cortar" el árbol a diferentes alturas para obtener diferentes números de clusters

---

### 3.4 Análisis de Frecuencias

**Objetivo**: Identificar términos y conceptos clave

1. Ir a **"Análisis de Frecuencias"**
2. Seleccionar publicaciones a analizar
3. Configurar parámetros:
   - **Top N términos**: 20 (cuántos términos mostrar)
   - **N-gramas**: 1, 2, 3 (palabras individuales, bigramas, trigramas)
   - **Stopwords**: Activado (eliminar palabras comunes como "el", "la", etc.)
4. Click en **"Analizar"**
5. Ver resultados:
   - **Términos más frecuentes** (con conteos)
   - **TF-IDF** (términos importantes)
   - **Conceptos clave** identificados
   - **Precisión** del análisis

**Ejemplo de resultado:**
```
Términos más frecuentes:
1. artificial intelligence (45 menciones)
2. generative AI (32 menciones)
3. machine learning (28 menciones)
...
```

---

### 3.5 Visualizaciones

**Objetivo**: Crear gráficos profesionales de los resultados

#### 📊 Nube de Palabras (WordCloud)
1. Ir a **"Visualizaciones"** → **"WordCloud"**
2. Seleccionar publicaciones
3. Elegir método: Frecuencia o TF-IDF
4. Click en **"Generar"**
5. Ver y descargar imagen

**Uso:** Identificar rápidamente temas principales

---

#### 🗺️ Mapa de Calor Geográfico
1. Ir a **"Visualizaciones"** → **"Heatmap"**
2. Seleccionar publicaciones
3. Elegir tipo:
   - **Choropleth** - Mapa mundial coloreado
   - **Bar Chart** - Gráfico de barras por país
4. Click en **"Generar"**
5. Ver distribución geográfica

**Uso:** Ver de qué países provienen las publicaciones

---

#### 📅 Línea de Tiempo
1. Ir a **"Visualizaciones"** → **"Timeline"**
2. Seleccionar publicaciones
3. Elegir agrupación:
   - **Por año** - Tendencia temporal
   - **Por revista** - Comparar fuentes
4. Click en **"Generar"**
5. Ver evolución temporal

**Uso:** Identificar tendencias en el tiempo

---

#### 📄 Exportar a PDF
1. Generar todas las visualizaciones deseadas
2. Ir a **"Exportar"** → **"PDF"**
3. Seleccionar visualizaciones a incluir
4. Click en **"Generar PDF"**
5. Descargar archivo

**Uso:** Crear reportes profesionales para presentación

---

## 🧪 4. SCRIPTS DE PRUEBA (Para Desarrollo)

### Probar Similitud
```powershell
.\.venv\Scripts\python.exe .\Backend\quick_test_similarity.py
```
**Resultado:** Prueba los 6 algoritmos con 5 publicaciones

### Probar Clustering
```powershell
.\.venv\Scripts\python.exe .\Backend\quick_test_clustering_standalone.py
```
**Resultado:** Genera dendrogramas con 4 métodos diferentes

### Descargar Publicaciones
```powershell
.\.venv\Scripts\python.exe .\Backend\test_download_priority.py
```
**Resultado:** Descarga 5 publicaciones de CrossRef

### Ejecutar Tests
```powershell
cd Backend
..\.venv\Scripts\pytest tests/ -v
```
**Resultado:** Ejecuta todos los tests automatizados

---

## 🔧 5. SOLUCIÓN DE PROBLEMAS

### Problema: Backend no inicia
**Síntomas:** Error al acceder a http://localhost:8000

**Soluciones:**
```powershell
# 1. Verificar que el entorno virtual esté activado
.\.venv\Scripts\Activate.ps1

# 2. Reinstalar dependencias
pip install -r Backend/requirements.txt

# 3. Verificar puerto ocupado
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess
```

---

### Problema: Frontend no carga
**Síntomas:** Página en blanco en http://localhost:5173

**Soluciones:**
```powershell
# 1. Limpiar caché y reinstalar
cd Frontend
Remove-Item -Recurse -Force node_modules
npm install

# 2. Verificar puerto
Get-Process -Id (Get-NetTCPConnection -LocalPort 5173).OwningProcess
```

---

### Problema: Descarga falla
**Síntomas:** Error "API key inválida" o "No results"

**Soluciones:**
1. **ScienceDirect:** Verificar API key en `.env`
2. **SAGE:** Verificar URL institucional
3. **CrossRef:** Verificar email en `.env`
4. **Usar solo CrossRef** (más confiable)

---

### Problema: BERT/Sentence-BERT no funciona
**Síntomas:** "torch" o "transformers" no encontrado

**Solución:**
```powershell
.\.venv\Scripts\pip install torch transformers sentence-transformers
```

**Nota:** Estos son opcionales. Los algoritmos clásicos (Levenshtein, TF-IDF, Jaccard, N-gramas) son suficientes para el proyecto académico.

---

## 📊 6. CASOS DE USO

### Caso 1: Análisis Básico de 50 Publicaciones
```
1. Descargar 50 publicaciones de CrossRef
2. Ejecutar análisis de similitud (TF-IDF)
3. Generar clustering (Ward, 3 clusters)
4. Analizar frecuencias de términos
5. Crear WordCloud
6. Exportar todo a PDF
```
**Tiempo estimado:** 10 minutos

---

### Caso 2: Comparación de Algoritmos
```
1. Descargar 10 publicaciones
2. Ejecutar TODOS los 6 algoritmos de similitud
3. Comparar resultados y tiempos
4. Identificar algoritmo más apropiado
5. Documentar hallazgos
```
**Tiempo estimado:** 15 minutos

---

### Caso 3: Análisis Completo para Tesis
```
1. Descargar 100+ publicaciones
2. Limpiar y deduplicar
3. Análisis de similitud (Sentence-BERT)
4. Clustering jerárquico (Ward, múltiples niveles)
5. Análisis de frecuencias por cluster
6. Visualizaciones completas
7. Identificar brechas de investigación
8. Generar reportes PDF profesionales
```
**Tiempo estimado:** 1-2 horas

---

## 🎓 7. PARA LA PRESENTACIÓN ACADÉMICA

### Qué mostrar:
1. ✅ **Demo en vivo** del sistema funcionando
2. ✅ **Descarga** de publicaciones reales
3. ✅ **Comparación** de algoritmos (resultados + tiempos)
4. ✅ **Clustering** con dendrograma
5. ✅ **Visualizaciones** profesionales (WordCloud, Timeline)
6. ✅ **Resultados** interpretados

### Qué preparar:
- 📸 Screenshots de cada funcionalidad
- 📊 Gráficos de comparación de algoritmos
- 📈 Dendrogramas de ejemplo
- 📄 PDF con visualizaciones
- 🎥 Video demo (3-5 minutos)

---

## 📞 8. SOPORTE

### Documentación adicional:
- **README.md** - Información general del proyecto
- **Backend/REPORTE_PRUEBAS.md** - Resultados de tests
- **Backend/REPORTE_FINAL_TODAS_PRIORIDADES.md** - Resumen completo

### APIs:
- **Swagger UI:** http://localhost:8000/docs (cuando el backend esté corriendo)
- **ReDoc:** http://localhost:8000/redoc

### Contacto:
- Santiago Ovalle Cortés - santiago.ovallec@uqvirtual.edu.co
- Universidad del Quindío
- Análisis de Algoritmos (2025-2)

---

## ✅ 9. CHECKLIST DE VERIFICACIÓN

Antes de presentar, verificar que:

- [ ] El sistema inicia correctamente (`.\start-project.ps1`)
- [ ] Backend responde en http://localhost:8000
- [ ] Frontend carga en http://localhost:5173
- [ ] Se pueden descargar publicaciones de CrossRef
- [ ] Los 6 algoritmos de similitud funcionan
- [ ] El clustering genera dendrogramas
- [ ] Las visualizaciones se generan correctamente
- [ ] El PDF se exporta sin errores
- [ ] Todos los tests pasan (`pytest`)
- [ ] Tienes screenshots de todas las funcionalidades

---

**Última actualización:** Noviembre 10, 2025  
**Versión:** 1.0  
**Estado:** ✅ Sistema completamente funcional
