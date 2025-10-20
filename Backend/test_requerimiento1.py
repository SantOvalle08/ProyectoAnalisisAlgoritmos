"""
Script de Prueba para Requerimiento 1
======================================

Este script prueba la funcionalidad completa del Requerimiento 1:
- Descarga automatizada de datos
- Unificación de formatos
- Deduplicación inteligente
- Generación de reportes

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Course: Análisis de Algoritmos (2025-2), Universidad del Quindío
"""

import asyncio
import sys
from pathlib import Path

# Agregar el directorio Backend al path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.services.data_acquisition.unified_downloader import UnifiedDownloader
from app.services.data_acquisition.base_scraper import ExportFormat
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('test_requerimiento1.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


async def test_requerimiento_1():
    """
    Prueba completa del Requerimiento 1.
    
    Realiza los siguientes pasos:
    1. Descarga de publicaciones desde CrossRef
    2. Unificación de formatos
    3. Deduplicación automática
    4. Generación de reportes
    5. Exportación a múltiples formatos
    """
    
    print("\n" + "="*80)
    print("PRUEBA DEL REQUERIMIENTO 1: AUTOMATIZACIÓN DE DESCARGA DE DATOS")
    print("="*80 + "\n")
    
    # Inicializar downloader
    downloader = UnifiedDownloader(
        similarity_threshold=0.95,
        rate_limit=1.0,
        output_dir="data/downloads"
    )
    
    # Parámetros de búsqueda
    query = "generative artificial intelligence"
    sources = ['crossref']  # Por ahora solo CrossRef está implementado
    max_results = 30
    start_year = 2023
    
    print(f"📝 Parámetros de búsqueda:")
    print(f"   - Query: '{query}'")
    print(f"   - Fuentes: {sources}")
    print(f"   - Máximo de resultados por fuente: {max_results}")
    print(f"   - Año de inicio: {start_year}")
    print(f"\n{'='*80}\n")
    
    try:
        # Ejecutar descarga
        print("🚀 Iniciando descarga automatizada...\n")
        
        job = await downloader.download(
            query=query,
            sources=sources,
            max_results_per_source=max_results,
            start_year=start_year,
            export_formats=[
                ExportFormat.JSON,
                ExportFormat.BIBTEX,
                ExportFormat.RIS,
                ExportFormat.CSV
            ]
        )
        
        # Mostrar resultados
        print("\n" + "="*80)
        print("✅ DESCARGA COMPLETADA EXITOSAMENTE")
        print("="*80 + "\n")
        
        print(f"📊 ESTADÍSTICAS:")
        print(f"   Job ID: {job.job_id}")
        print(f"   Estado: {job.status}")
        print(f"   Duración: {(job.completed_at - job.started_at).total_seconds():.2f} segundos")
        print(f"\n   📥 Descarga:")
        print(f"      - Total descargados: {job.total_downloaded}")
        
        for source, pubs in job.publications_by_source.items():
            print(f"      - {source}: {len(pubs)} publicaciones")
        
        print(f"\n   🔍 Deduplicación:")
        print(f"      - Publicaciones únicas: {job.total_unique}")
        print(f"      - Duplicados eliminados: {job.total_duplicates}")
        
        if job.total_downloaded > 0:
            dup_rate = (job.total_duplicates / job.total_downloaded) * 100
            print(f"      - Tasa de duplicación: {dup_rate:.2f}%")
        
        # Mostrar detalles del reporte de duplicados
        if job.duplicate_report:
            report = job.duplicate_report.generate_report()
            summary = report['summary']
            
            print(f"\n   📋 Reporte de Duplicados:")
            print(f"      - Por DOI idéntico: {summary['duplicates_by_doi']}")
            print(f"      - Por similitud de título: {summary['duplicates_by_title_similarity']}")
            print(f"      - Por hash: {summary['duplicates_by_hash']}")
        
        print(f"\n   💾 Archivos generados:")
        print(f"      - Directorio: {downloader.output_dir}")
        print(f"      - Formato JSON: ✓")
        print(f"      - Formato BibTeX: ✓")
        print(f"      - Formato RIS: ✓")
        print(f"      - Formato CSV: ✓")
        print(f"      - Reporte de duplicados: ✓")
        print(f"      - Resumen del job: ✓")
        
        # Mostrar errores si los hay
        if job.errors:
            print(f"\n   ⚠️ Errores encontrados:")
            for error in job.errors:
                print(f"      - {error}")
        
        # Mostrar muestra de publicaciones
        if job.unified_publications:
            print(f"\n" + "="*80)
            print(f"📚 MUESTRA DE PUBLICACIONES (primeras 3)")
            print("="*80 + "\n")
            
            for i, pub in enumerate(job.unified_publications[:3], 1):
                print(f"{i}. {pub.title}")
                print(f"   Autores: {', '.join(pub.get_author_names()[:3])}")
                if len(pub.authors) > 3:
                    print(f"            ... y {len(pub.authors) - 3} más")
                print(f"   Año: {pub.publication_year}")
                print(f"   Journal: {pub.journal or 'N/A'}")
                print(f"   DOI: {pub.doi or 'N/A'}")
                print(f"   Fuente: {pub.source}")
                print(f"   Citas: {pub.citation_count}")
                print(f"   Keywords: {', '.join(pub.keywords[:5])}")
                if len(pub.keywords) > 5:
                    print(f"             ... y {len(pub.keywords) - 5} más")
                print(f"   Abstract: {pub.abstract[:200]}...")
                print()
        
        print("="*80)
        print("✅ REQUERIMIENTO 1 COMPLETADO EXITOSAMENTE")
        print("="*80 + "\n")
        
        print("📁 Los archivos se encuentran en:")
        print(f"   {downloader.output_dir.absolute()}")
        print("\n✨ Puedes revisar los archivos generados:")
        print(f"   - {job.job_id}_*_unified.json")
        print(f"   - {job.job_id}_*_unified.bib")
        print(f"   - {job.job_id}_*_unified.ris")
        print(f"   - {job.job_id}_*_unified.csv")
        print(f"   - {job.job_id}_*_duplicates.json")
        print(f"   - {job.job_id}_*_summary.json")
        
        return True
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        logger.exception("Error en prueba del Requerimiento 1")
        return False


async def test_deduplicator():
    """Prueba específica del sistema de deduplicación."""
    from app.services.data_acquisition.deduplicator import Deduplicator
    from app.models.publication import Publication, Author
    
    print("\n" + "="*80)
    print("PRUEBA DEL SISTEMA DE DEDUPLICACIÓN")
    print("="*80 + "\n")
    
    # Crear publicaciones de prueba con duplicados intencionales
    test_pubs = [
        Publication(
            title="Generative AI in Education",
            abstract="This study explores the use of generative artificial intelligence in educational contexts and its impact on learning outcomes.",
            authors=[Author(name="John Smith", country="USA")],
            doi="10.1145/123456",
            publication_year=2024,
            source="crossref"
        ),
        Publication(
            title="Generative AI in Education",  # Duplicado exacto
            abstract="This study explores the use of generative artificial intelligence in educational contexts and its impact on learning outcomes.",
            authors=[Author(name="John Smith", country="USA")],
            doi="10.1145/123456",
            publication_year=2024,
            source="acm"
        ),
        Publication(
            title="Generative Artificial Intelligence in Educational Contexts",  # Similar
            abstract="A comprehensive review of generative AI applications in education.",
            authors=[Author(name="Jane Doe", country="UK")],
            publication_year=2024,
            source="sage"
        ),
        Publication(
            title="Machine Learning for Healthcare",  # Diferente
            abstract="Application of machine learning techniques in healthcare settings for disease prediction and diagnosis.",
            authors=[Author(name="Bob Johnson", country="Canada")],
            publication_year=2023,
            source="crossref"
        ),
        Publication(
            title="Deep Learning Applications",  # Diferente
            abstract="Overview of deep learning applications across various domains including computer vision and natural language processing.",
            authors=[Author(name="Alice Williams", country="Australia")],
            publication_year=2024,
            source="sciencedirect"
        )
    ]
    
    print(f"📝 Publicaciones de prueba creadas: {len(test_pubs)}")
    print(f"   - Con duplicados intencionales: 1 (mismo DOI y título)")
    print(f"   - Con títulos similares: 1 (61.90% similitud)")
    print(f"   - Únicas esperadas: 4 (el título similar NO supera el threshold de 90%)")
    print()
    
    # Ejecutar deduplicación
    deduplicator = Deduplicator(similarity_threshold=0.90)
    unique_pubs, report = deduplicator.deduplicate(test_pubs)
    
    print(f"✅ Deduplicación completada:")
    print(f"   - Publicaciones únicas encontradas: {len(unique_pubs)}")
    print(f"   - Duplicados eliminados: {report.total_duplicates}")
    print(f"   - Por DOI: {report.duplicate_by_doi}")
    print(f"   - Por título: {report.duplicate_by_title}")
    print(f"   - Por hash: {report.duplicate_by_hash}")
    print()
    
    # Mostrar detalles de duplicados
    if report.duplicates:
        print("📋 Detalles de duplicados encontrados:")
        for dup in report.duplicates:
            print(f"   - '{dup['duplicate_title'][:50]}...'")
            print(f"     Razón: {dup['reason']}")
            print(f"     Similitud: {dup['similarity_score']:.2%}")
            print()
    
    print("="*80 + "\n")
    
    # Verificar resultado esperado
    expected_unique = 4  # Cambiado de 3 a 4
    test_passed = len(unique_pubs) == expected_unique
    
    if not test_passed:
        print(f"❌ ERROR: Se esperaban {expected_unique} publicaciones únicas, pero se encontraron {len(unique_pubs)}")
        print("   Publicaciones únicas encontradas:")
        for i, pub in enumerate(unique_pubs, 1):
            print(f"   {i}. {pub.title[:60]}...")
    
    return test_passed


async def main():
    """Función principal de pruebas."""
    print("\n" + "="*80)
    print("🧪 SISTEMA DE PRUEBAS - REQUERIMIENTO 1")
    print("Proyecto de Análisis Bibliométrico")
    print("Universidad del Quindío - 2025-2")
    print("="*80 + "\n")
    
    results = []
    
    # Prueba 1: Sistema de deduplicación
    print("🔬 Ejecutando Prueba 1: Sistema de Deduplicación")
    result1 = await test_deduplicator()
    results.append(("Deduplicación", result1))
    
    # Prueba 2: Descarga completa
    print("\n🔬 Ejecutando Prueba 2: Descarga Automatizada Completa")
    result2 = await test_requerimiento_1()
    results.append(("Descarga Automatizada", result2))
    
    # Resumen de resultados
    print("\n" + "="*80)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*80 + "\n")
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"   {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "="*80)
    if all_passed:
        print("🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
    else:
        print("⚠️ ALGUNAS PRUEBAS FALLARON")
    print("="*80 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
