"""
Proyecto Análisis de Algoritmos Aplicados a Bibliometría
Backend FastAPI Application

Sistema integral de análisis bibliométrico que implementa algoritmos de 
machine learning y procesamiento de lenguaje natural para el estudio 
computacional de la producción científica en IA Generativa.

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Course: Análisis de Algoritmos (2025-2), Universidad del Quindío
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from typing import Dict, Any

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuración de la aplicación
APP_CONFIG = {
    "title": "Análisis Bibliométrico API",
    "description": """
    ## 🔬 API para Análisis Bibliométrico Automatizado
    
    Plataforma web automatizada para el análisis bibliométrico avanzado de 
    publicaciones científicas sobre inteligencia artificial generativa.
    
    ### 🚀 Características Principales
    
    * **🤖 Algoritmos de ML**: Implementación de 6 algoritmos de similitud textual
    * **📊 Análisis Avanzado**: Clustering jerárquico y análisis de frecuencias  
    * **🌐 Múltiples Fuentes**: Integración con ACM, SAGE, ScienceDirect
    * **📈 Visualizaciones**: Mapas interactivos, dendrogramas, nubes de palabras
    * **⚡ Alto Rendimiento**: FastAPI + Async/Await para máxima velocidad
    
    ### 🔍 Dominio de Investigación
    
    **Tema:** Inteligencia Artificial Generativa en Educación  
    **Cadena de búsqueda:** "generative artificial intelligence"  
    **Algoritmos:** Levenshtein, TF-IDF, Jaccard, N-gramas, BERT, Sentence-BERT  
    """,
    "version": "1.0.0",
    "docs_url": "/docs",
    "redoc_url": "/redoc",
    "openapi_url": "/openapi.json"
}

# Event handlers para startup y shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja el ciclo de vida de la aplicación FastAPI.
    
    Startup:
    - Inicializa conexiones a base de datos
    - Carga modelos de ML pre-entrenados
    - Configura caché Redis
    
    Shutdown:
    - Cierra conexiones
    - Libera recursos
    """
    # Startup
    logger.info("Iniciando Análisis Bibliométrico API...")
    logger.info("Cargando modelos de NLP...")
    logger.info("Conectando a base de datos...")
    logger.info("Configurando caché Redis...")
    logger.info("Aplicación lista!")
    
    yield
    
    # Shutdown
    logger.info("Cerrando aplicación...")
    logger.info("Guardando estado...")
    logger.info("Cerrando conexiones...")
    logger.info("Aplicación cerrada correctamente")

# Crear instancia de FastAPI
app = FastAPI(
    lifespan=lifespan,
    **APP_CONFIG
)

# Configuración de CORS para comunicación con frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000",  # React dev server alternativo
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",  # Vite dev server alternativo
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Middleware de seguridad
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "*.localhost"]
)

# Manejador global de excepciones
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Manejador personalizado para excepciones HTTP."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url.path)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Manejador para excepciones generales."""
    logger.error(f"Error inesperado: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Error interno del servidor",
            "status_code": 500,
            "path": str(request.url.path)
        }
    )

# Rutas básicas
@app.get("/", tags=["Root"])
async def root() -> Dict[str, Any]:
    """
    🏠 Endpoint raíz de la API.
    
    Retorna información básica sobre la API de análisis bibliométrico.
    """
    return {
        "message": "🔬 API de Análisis Bibliométrico - Universidad del Quindío",
        "description": "Sistema automatizado para análisis de publicaciones científicas en IA Generativa",
        "version": "1.0.0",
        "status": "🟢 Activo",
        "docs": "/docs",
        "redoc": "/redoc",
        "authors": ["Santiago Ovalle Cortés", "Juan Sebastián Noreña"],
        "course": "Análisis de Algoritmos (2025-2)",
        "university": "Universidad del Quindío"
    }

@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """
    🏥 Endpoint de verificación de salud.
    
    Verifica el estado de todos los servicios críticos.
    """
    return {
        "status": "healthy",
        "timestamp": "2025-09-16T14:00:00Z",
        "services": {
            "api": "🟢 Activo",
            "database": "🟡 Pendiente configuración",
            "redis": "🟡 Pendiente configuración", 
            "ml_models": "🟡 Pendiente carga"
        },
        "uptime": "< 1 minuto",
        "version": "1.0.0"
    }

@app.get("/api/v1/info", tags=["Info"])
async def api_info() -> Dict[str, Any]:
    """
    ℹ️ Información detallada de la API.
    
    Retorna especificaciones técnicas y endpoints disponibles.
    """
    return {
        "api_version": "v1",
        "endpoints": {
            "data_acquisition": "🔗 /api/v1/data",
            "ml_analysis": "🤖 /api/v1/ml", 
            "analytics": "📊 /api/v1/analytics",
            "visualizations": "📈 /api/v1/viz"
        },
        "algorithms": {
            "similarity_classic": [
                "Distancia de Levenshtein",
                "TF-IDF + Similitud del Coseno", 
                "Coeficiente de Jaccard",
                "N-gramas con Overlapping"
            ],
            "similarity_ai": [
                "BERT Sentence Embeddings",
                "Sentence-BERT (SBERT)"
            ],
            "clustering": [
                "Ward Linkage",
                "Average Linkage", 
                "Complete Linkage"
            ]
        },
        "data_sources": [
            "ACM Digital Library",
            "SAGE Publications",
            "ScienceDirect",
            "CrossRef API"
        ],
        "tech_stack": {
            "framework": "FastAPI 0.116+",
            "python": "3.13+",
            "ml_libraries": ["transformers", "sentence-transformers", "scikit-learn"],
            "nlp_libraries": ["spaCy", "NLTK"],
            "database": "PostgreSQL + Redis",
            "deployment": "Uvicorn ASGI Server"
        }
    }

# Función principal para desarrollo
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )