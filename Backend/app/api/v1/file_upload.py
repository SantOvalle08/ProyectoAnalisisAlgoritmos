"""
API Endpoints para Carga de Archivos Bibliográficos
====================================================

Endpoints REST para cargar y parsear archivos en múltiples formatos.

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Course: Análisis de Algoritmos (2025-2), Universidad del Quindío
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Any
import logging
import json

from app.services.data_acquisition.parsers.bibtex_parser import BibTeXParser
from app.services.data_acquisition.parsers.ris_parser import RISParser
from app.services.data_acquisition.parsers.csv_parser import CSVParser
from app.models.publication import Publication

logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(
    prefix="/upload",
    tags=["File Upload"]
)


@router.post("/parse")
async def parse_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Parse archivo bibliográfico en múltiples formatos.
    
    Formatos soportados:
    - JSON (.json)
    - BibTeX (.bib, .bibtex)
    - RIS (.ris)
    - CSV (.csv)
    
    Returns:
        Dict con lista de publicaciones parseadas
    """
    try:
        # Leer contenido del archivo
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Determinar formato por extensión
        filename = file.filename.lower()
        publications = []
        
        if filename.endswith('.json'):
            # Parsear JSON
            try:
                data = json.loads(content_str)
                # Si es una lista de publicaciones
                if isinstance(data, list):
                    publications = [Publication(**pub) if isinstance(pub, dict) else pub for pub in data]
                # Si es un objeto con key 'publications' o similar
                elif isinstance(data, dict):
                    if 'publications' in data:
                        publications = [Publication(**pub) if isinstance(pub, dict) else pub for pub in data['publications']]
                    elif 'results' in data:
                        publications = [Publication(**pub) if isinstance(pub, dict) else pub for pub in data['results']]
                    else:
                        # Intentar usar el objeto directamente
                        publications = [Publication(**data)]
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error parseando JSON: {str(e)}")
                
        elif filename.endswith(('.bib', '.bibtex')):
            # Parsear BibTeX
            parser = BibTeXParser()
            publications = parser.parse_string(content_str)
            
        elif filename.endswith('.ris'):
            # Parsear RIS
            parser = RISParser()
            publications = parser.parse_string(content_str)
            
        elif filename.endswith('.csv'):
            # Parsear CSV
            parser = CSVParser()
            publications = parser.parse_string(content_str)
            
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Formato de archivo no soportado. Use: .json, .bib, .bibtex, .ris, o .csv"
            )
        
        # Convertir publicaciones a diccionarios
        publications_data = []
        for pub in publications:
            if isinstance(pub, Publication):
                publications_data.append(pub.model_dump())
            elif isinstance(pub, dict):
                publications_data.append(pub)
            else:
                publications_data.append(pub.__dict__)
        
        logger.info(f"Archivo '{file.filename}' parseado exitosamente: {len(publications_data)} publicaciones")
        
        return {
            "success": True,
            "filename": file.filename,
            "format": filename.split('.')[-1],
            "total_publications": len(publications_data),
            "publications": publications_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error procesando archivo '{file.filename}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error procesando archivo: {str(e)}")
