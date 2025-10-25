# 🚀 Guía de Despliegue Local - BiblioAnalysis

Este documento describe cómo ejecutar y desplegar el proyecto **BiblioAnalysis** en un entorno de desarrollo local.

---

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#1-requisitos-previos)
2. [Configuración del Backend](#2-configuración-del-backend)
3. [Configuración del Frontend](#3-configuración-del-frontend)
4. [Ejecución del Proyecto](#4-ejecución-del-proyecto)
5. [Testing](#5-testing)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Requisitos Previos

### Software Necesario

- **Python 3.13+** - Para el backend FastAPI
- **Node.js 20+** - Para el frontend React
- **npm 10+** - Gestor de paquetes de Node.js
- **Git** - Control de versiones

### Verificar Instalación

```powershell
# Verificar Python
python --version

# Verificar Node.js
node --version

# Verificar npm
npm --version
```

---

## 2. Configuración del Backend

### 2.1 Instalar Dependencias

```powershell
cd Backend
pip install -r requirements.txt
```

### 2.2 Descargar Modelos de NLP

```powershell
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
```

### 2.3 Variables de Entorno (Opcional)

El backend funciona con configuración por defecto. Si deseas personalizar:

```env
# Backend/.env
ENVIRONMENT=development
LOG_LEVEL=INFO
DUPLICATE_THRESHOLD=0.95
```

---

## 3. Configuración del Frontend

### 3.1 Instalar Dependencias

```powershell
cd Frontend
npm install
```

### 3.2 Variables de Entorno

Crea un archivo `.env` en `Frontend/`:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=BiblioAnalysis
VITE_ENVIRONMENT=development
```

---

## 4. Ejecución del Proyecto

### 4.1 Opción Automática (Recomendada)

Usa el script de inicio que lanza ambos servidores:

```powershell
# Desde la raíz del proyecto
.\start-project.ps1
```

Este script:
- ✅ Inicia el backend en `http://localhost:8000`
- ✅ Inicia el frontend en `http://localhost:5173`
- ✅ Abre ambos servidores en ventanas separadas de PowerShell

### 4.2 Opción Manual

**Terminal 1 - Backend:**
```powershell
cd Backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd Frontend
npm run dev
```

### 4.3 URLs de Acceso

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

---

## 5. Testing

### 5.1 Tests del Backend

```powershell
cd Backend

# Ejecutar todos los tests
pytest tests/ -v

# Tests específicos
pytest tests/test_similarity_api.py -v
pytest tests/test_api_clustering.py -v
pytest tests/test_api_frequency.py -v

# Con cobertura
pytest tests/ -v --cov=app --cov-report=html
```

### 5.2 Tests del Frontend

```powershell
cd Frontend

# Linter
npm run lint

# Build de producción (verifica errores de TypeScript)
npm run build
```

### 5.3 Tests de Integración

Ver `PRUEBAS_INTEGRACION.md` para el plan completo de tests.

**Checklist rápido:**
1. ✅ Backend responde en `/health`
2. ✅ Frontend carga correctamente
3. ✅ API de similitud funciona
4. ✅ API de clustering funciona
5. ✅ API de frecuencias funciona
6. ✅ Visualizaciones se generan correctamente

---

## 6. Troubleshooting

### 6.1 Puerto 8000 ya en uso

```powershell
# Windows - Encontrar proceso usando el puerto
netstat -ano | findstr :8000

# Matar proceso (reemplaza PID)
taskkill /PID <PID> /F
```

### 6.2 Puerto 5173 ya en uso

```powershell
# Windows - Encontrar y matar proceso
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### 6.3 Error de CORS

Asegúrate de que el backend esté configurado correctamente:

```python
# Backend/main.py debe tener:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 6.4 Módulos de Python faltantes

```powershell
cd Backend
pip install -r requirements.txt --upgrade
```

### 6.5 Dependencias de Node.js desactualizadas

```powershell
cd Frontend
npm ci  # Instalación limpia según package-lock.json
```

### 6.6 Error "Cannot find module"

```powershell
# Reiniciar TypeScript Server en VS Code
# Presiona Ctrl+Shift+P -> "TypeScript: Restart TS Server"

# O reconstruir
cd Frontend
npm run build
```

---

## 📚 Documentación Adicional

- **[README.md](./README.md)** - Información general del proyecto
- **[INTEGRACION.md](./INTEGRACION.md)** - Documentación de integración Backend-Frontend
- **[PRUEBAS_INTEGRACION.md](./PRUEBAS_INTEGRACION.md)** - Plan de pruebas
- **[ESTADO_ACTUAL_PROYECTO.md](./ESTADO_ACTUAL_PROYECTO.md)** - Estado del desarrollo

---

## 🎯 Quick Start

```powershell
# 1. Clonar repositorio
git clone <repo-url>
cd ProyectoAnalisisAlgoritmos

# 2. Instalar dependencias del backend
cd Backend
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
cd ..

# 3. Instalar dependencias del frontend
cd Frontend
npm install
cd ..

# 4. Iniciar proyecto
.\start-project.ps1
```

---

## 👥 Autores

- **Santiago Ovalle Cortés**
- **Juan Sebastián Noreña**

**Universidad del Quindío** - 2025
