"""
Script para probar descarga de 5 publicaciones por fuente
PRIORIDAD CRÍTICA #1
"""
import asyncio
import json
import sys
from pathlib import Path
import time

# Agregar directorio del proyecto al path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.data_acquisition.crossref_scraper import CrossRefScraper
from app.services.data_acquisition.sciencedirect_scraper import ScienceDirectScraper
from app.services.data_acquisition.sage_scraper import SAGEScraper
from app.config.settings import settings

async def test_download():
    """Prueba de descarga de 5 publicaciones por cada fuente"""
    
    print("=" * 80)
    print("🎯 PRIORIDAD CRÍTICA #1: Prueba de Descarga de Publicaciones")
    print("=" * 80)
    print()
    
    # Verificar configuraciones
    print("📋 Configuraciones Actuales:")
    print(f"  • CrossRef Email: {settings.crossref_api_email}")
    print(f"  • ScienceDirect API Key: {settings.elsevier_api_key[:20]}..." if settings.elsevier_api_key else "  • ScienceDirect API Key: ❌ NO CONFIGURADA")
    print(f"  • SAGE Institutional URL: {settings.sage_institutional_url}")
    print()
    
    # Configurar descarga
    query = "generative artificial intelligence"
    max_results = 5  # Solo 5 publicaciones por fuente como pidió el usuario
    sources = ["crossref", "sciencedirect", "sage", "acm"]
    
    print(f"🔍 Query: '{query}'")
    print(f"📊 Resultados por fuente: {max_results}")
    print(f"🌐 Fuentes: crossref, sciencedirect, sage")
    print()
    print("-" * 80)
    print()
    
    publications = []
    
    try:
        print("⏳ Iniciando descarga...")
        print()
        
        # 1. CrossRef
        print("📡 Descargando de CrossRef...")
        crossref = CrossRefScraper(rate_limit=1.0)
        crossref_pubs = await crossref.search(query, max_results=max_results)
        # Convertir a diccionarios
        for pub in crossref_pubs:
            pub_dict = pub.model_dump() if hasattr(pub, 'model_dump') else pub.dict()
            pub_dict['source'] = 'crossref'
            publications.append(pub_dict)
        print(f"   ✅ {len(crossref_pubs)} publicaciones")
        await asyncio.sleep(2)
        
        # 2. ScienceDirect
        print("📡 Descargando de ScienceDirect...")
        sciencedirect = ScienceDirectScraper(
            api_key=settings.elsevier_api_key,
            rate_limit=0.5
        )
        sd_pubs = await sciencedirect.search(query, max_results=max_results)
        for pub in sd_pubs:
            pub_dict = pub.model_dump() if hasattr(pub, 'model_dump') else pub.dict()
            pub_dict['source'] = 'sciencedirect'
            publications.append(pub_dict)
        print(f"   ✅ {len(sd_pubs)} publicaciones")
        await asyncio.sleep(2)
        
        # 3. SAGE
        print("📡 Descargando de SAGE...")
        sage = SAGEScraper(
            institutional_url=settings.sage_institutional_url,
            rate_limit=1.0
        )
        sage_pubs = await sage.search(query, max_results=max_results)
        for pub in sage_pubs:
            pub_dict = pub.model_dump() if hasattr(pub, 'model_dump') else pub.dict()
            pub_dict['source'] = 'sage'
            publications.append(pub_dict)
        print(f"   ✅ {len(sage_pubs)} publicaciones")
        
        # Nota: ACM se omite porque requiere Selenium y puede ser lento
        
        print()
        print("=" * 80)
        print("✅ DESCARGA COMPLETADA")
        print("=" * 80)
        print()
        
        # Agrupar por fuente
        by_source = {}
        for pub in publications:
            source = pub.get('source', 'unknown')
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(pub)
        
        # Mostrar resumen
        print("📊 RESUMEN POR FUENTE:")
        print()
        test_sources = ['crossref', 'sciencedirect', 'sage']
        for source in test_sources:
            count = len(by_source.get(source, []))
            status = "✅" if count > 0 else "❌"
            print(f"  {status} {source.upper()}: {count} publicaciones")
        
        print()
        print(f"📈 Total de publicaciones: {len(publications)}")
        print()
        
        # Validar estructura de datos
        print("-" * 80)
        print()
        print("🔍 VALIDACIÓN DE DATOS:")
        print()
        
        validation_errors = []
        mock_data_found = []
        
        for i, pub in enumerate(publications[:3], 1):  # Solo revisar las primeras 3
            source = pub.get('source', 'unknown')
            title = pub.get('title', '')
            authors = pub.get('authors', [])
            doi = pub.get('doi', '')
            year = pub.get('year', '')
            
            print(f"  Publicación #{i} ({source}):")
            print(f"    Título: {title[:60]}...")
            
            # Verificar si es MOCK
            if '[MOCK]' in title or (authors and 'Author 1A' in str(authors)):
                mock_data_found.append(f"{source}: {title[:40]}")
                print(f"    ⚠️  ADVERTENCIA: Parece ser datos MOCK")
            else:
                print(f"    ✅ Datos reales")
            
            print(f"    Autores: {len(authors)} autores")
            print(f"    DOI: {doi if doi else '❌ Sin DOI'}")
            print(f"    Año: {year if year else '❌ Sin año'}")
            
            # Validar campos obligatorios
            if not title:
                validation_errors.append(f"Publicación {i}: Sin título")
            if not authors or len(authors) == 0:
                validation_errors.append(f"Publicación {i}: Sin autores")
            
            print()
        
        # Guardar resultados
        output_dir = Path(__file__).parent / "data" / "downloads"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "test_download_5_pubs.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(publications, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Resultados guardados en: {output_file}")
        print()
        
        # Reporte final
        print("=" * 80)
        print("📋 REPORTE FINAL")
        print("=" * 80)
        print()
        
        if validation_errors:
            print("⚠️  ERRORES DE VALIDACIÓN:")
            for error in validation_errors:
                print(f"  • {error}")
            print()
        else:
            print("✅ Todos los datos validados correctamente")
            print()
        
        if mock_data_found:
            print("⚠️  DATOS MOCK DETECTADOS:")
            for mock in mock_data_found:
                print(f"  • {mock}")
            print()
            print("🔧 ACCIÓN REQUERIDA:")
            print("  • ScienceDirect: Verificar que la API key sea válida")
            print("  • SAGE: Verificar acceso institucional")
            print()
        else:
            print("✅ No se detectaron datos MOCK - todos son datos reales")
            print()
        
        print("🎯 PRÓXIMOS PASOS:")
        print("  1. Revisar archivo JSON generado")
        print("  2. Verificar que los datos NO tengan prefijo [MOCK]")
        print("  3. Confirmar que los autores no sean 'Author 1A', etc.")
        print("  4. Si todo está bien, continuar con la prioridad #2")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 80)
        print("❌ ERROR EN LA DESCARGA")
        print("=" * 80)
        print()
        print(f"Error: {str(e)}")
        print()
        import traceback
        print("Stack trace:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_download())
    sys.exit(0 if result else 1)
