"""
Configuración de la aplicación FastAPI.

Este módulo contiene todas las configuraciones, variables de entorno
y constantes utilizadas en la aplicación.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os

class Settings(BaseSettings):
    """
    Configuración principal de la aplicación usando Pydantic Settings.
    """
    
    # Configuración básica de la aplicación
    app_name: str = Field(default="Análisis Bibliométrico API", description="Nombre de la aplicación")
    debug: bool = Field(default=True, description="Modo debug")
    version: str = Field(default="1.0.0", description="Versión de la API")
    
    # Configuración del servidor
    host: str = Field(default="127.0.0.1", description="Host del servidor")
    port: int = Field(default=8000, description="Puerto del servidor")
    
    # Configuración de CORS
    cors_origins: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000", 
            "http://localhost:5173",
            "http://127.0.0.1:5173"
        ],
        description="Orígenes permitidos para CORS"
    )
    
    # Configuración de base de datos PostgreSQL
    database_url: str = Field(
        default="postgresql://user:password@localhost:5432/bibliometric_analysis",
        description="URL de conexión a PostgreSQL"
    )
    database_user: str = Field(default="postgres", description="Usuario de la base de datos")
    database_password: str = Field(default="password", description="Contraseña de la base de datos")
    database_host: str = Field(default="localhost", description="Host de la base de datos")
    database_port: int = Field(default=5432, description="Puerto de la base de datos")
    database_name: str = Field(default="bibliometric_analysis", description="Nombre de la base de datos")
    
    # Configuración de Redis
    redis_url: str = Field(default="redis://localhost:6379", description="URL de conexión a Redis")
    redis_host: str = Field(default="localhost", description="Host de Redis")
    redis_port: int = Field(default=6379, description="Puerto de Redis")
    redis_db: int = Field(default=0, description="Base de datos de Redis")
    
    # Configuración de autenticación
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="Clave secreta para JWT"
    )
    algorithm: str = Field(default="HS256", description="Algoritmo para JWT")
    access_token_expire_minutes: int = Field(default=30, description="Expiración del token en minutos")
    
    # Configuración de APIs externas
    crossref_api_email: Optional[str] = Field(default=None, description="Email para API de CrossRef")
    elsevier_api_key: Optional[str] = Field(default=None, description="API Key de Elsevier")
    
    # Configuración de modelos ML/NLP
    model_cache_dir: str = Field(default="./models", description="Directorio de caché de modelos")
    default_sentence_model: str = Field(
        default="all-MiniLM-L6-v2", 
        description="Modelo por defecto para sentence embeddings"
    )
    spacy_model: str = Field(default="en_core_web_sm", description="Modelo de spaCy")
    
    # Configuración de logging
    log_level: str = Field(default="INFO", description="Nivel de logging")
    log_file: str = Field(default="app.log", description="Archivo de log")
    
    # Configuración de límites
    max_file_size: int = Field(default=10 * 1024 * 1024, description="Tamaño máximo de archivo (10MB)")
    max_concurrent_requests: int = Field(default=10, description="Máximo de requests concurrentes")
    request_timeout: int = Field(default=30, description="Timeout de requests en segundos")
    
    # Configuración específica del proyecto
    search_query: str = Field(
        default="generative artificial intelligence",
        description="Query principal de búsqueda bibliográfica"
    )
    max_results_per_source: int = Field(
        default=1000,
        description="Máximo número de resultados por fuente"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Crear instancia global de configuración
settings = Settings()

# Conceptos predefinidos para análisis de frecuencias
GENERATIVE_AI_CONCEPTS = [
    "artificial intelligence",
    "generative ai",
    "machine learning",
    "deep learning",
    "neural networks",
    "natural language processing",
    "computer vision",
    "large language models",
    "transformer models",
    "gpt",
    "bert",
    "generative adversarial networks",
    "diffusion models",
    "text generation",
    "image generation"
]

# Configuración de fuentes de datos bibliográficas
DATA_SOURCES = {
    "acm": {
        "name": "ACM Digital Library",
        "base_url": "https://dl.acm.org",
        "api_endpoint": "/api/search",
        "rate_limit": 10  # requests per minute
    },
    "sage": {
        "name": "SAGE Publications", 
        "base_url": "https://journals.sagepub.com",
        "api_endpoint": "/api/search",
        "rate_limit": 15
    },
    "sciencedirect": {
        "name": "ScienceDirect",
        "base_url": "https://api.elsevier.com",
        "api_endpoint": "/content/search/sciencedirect",
        "rate_limit": 5
    },
    "crossref": {
        "name": "CrossRef",
        "base_url": "https://api.crossref.org",
        "api_endpoint": "/works",
        "rate_limit": 50
    }
}

# Configuración de algoritmos de similitud
SIMILARITY_ALGORITHMS = {
    "classic": [
        "levenshtein",
        "tfidf_cosine", 
        "jaccard",
        "ngrams"
    ],
    "ai": [
        "bert_embeddings",
        "sentence_bert"
    ]
}

# Configuración de clustering
CLUSTERING_ALGORITHMS = [
    "ward",
    "average", 
    "complete"
]