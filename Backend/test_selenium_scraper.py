"""
Script de Prueba para ACM Selenium Scraper
===========================================

Este script prueba el scraper de ACM con Selenium para verificar
que puede bypassear Cloudflare y descargar publicaciones.

Uso:
    python test_selenium_scraper.py (desde directorio Backend)
    O desde raíz: python Backend\test_selenium_scraper.py
"""

import asyncio
import sys
import logging
import os
from pathlib import Path

# Cambiar al directorio Backend si no estamos ahí
backend_dir = Path(__file__).parent
if backend_dir.name == "Backend":
    os.chdir(backend_dir)
    sys.path.insert(0, str(backend_dir))
else:
    # Estamos en raíz, cambiar a Backend
    backend_path = Path(__file__).parent / "Backend"
    os.chdir(backend_path)
    sys.path.insert(0, str(backend_path))

from app.services.data_acquisition.acm_selenium_scraper import ACMSeleniumScraper

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def test_acm_selenium():
    """Prueba el scraper de ACM con Selenium."""
    
    print("=" * 70)
    print("PRUEBA DE ACM SELENIUM SCRAPER")
    print("=" * 70)
    print()
    
    # Crear scraper
    print("Inicializando scraper...")
    scraper = ACMSeleniumScraper(
        headless=False,  # Ver el navegador en acción (cambia a True para producción)
        rate_limit=1.0,   # 1 petición por segundo
        timeout=30
    )
    
    try:
        # Configurar búsqueda
        query = "machine learning"
        max_results = 5  # Pocas para prueba rápida
        
        print(f"Buscando '{query}' en ACM Digital Library...")
        print(f"   Max resultados: {max_results}")
        print()
        
        # Realizar búsqueda
        results = await scraper.search(
            query=query,
            max_results=max_results
        )
        
        # Mostrar resultados
        print()
        print("=" * 70)
        print(f"BUSQUEDA COMPLETADA: {len(results)} publicaciones encontradas")
        print("=" * 70)
        print()
        
        if results:
            for i, pub in enumerate(results, 1):
                print(f"Publicacion {i}:")
                print(f"   Titulo: {pub.title}")
                print(f"   Autores: {', '.join([a.name for a in pub.authors[:3]])}")
                if len(pub.authors) > 3:
                    print(f"            ...y {len(pub.authors) - 3} mas")
                print(f"   Anio: {pub.publication_date or 'N/A'}")
                print(f"   DOI: {pub.doi or 'N/A'}")
                print(f"   URL: {pub.url or 'N/A'}")
                if pub.abstract:
                    abstract_preview = pub.abstract[:150] + "..." if len(pub.abstract) > 150 else pub.abstract
                    print(f"   Abstract: {abstract_preview}")
                print()
        else:
            print("WARNING: No se encontraron resultados. Posibles razones:")
            print("   - Cloudflare bloqueo la peticion")
            print("   - El query no devolvio resultados")
            print("   - Error de red o timeout")
            print()
        
        print("=" * 70)
        print("PRUEBA COMPLETADA EXITOSAMENTE")
        print("=" * 70)
        
    except Exception as e:
        print()
        print("=" * 70)
        print(f"ERROR EN LA PRUEBA")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        print("Soluciones posibles:")
        print("   1. Verifica que Chrome este instalado")
        print("   2. Verifica conexion a internet")
        print("   3. Revisa logs para mas detalles")
        print("   4. Intenta con SELENIUM_HEADLESS=false en .env")
        print()
        import traceback
        traceback.print_exc()
        
    finally:
        # Cerrar navegador
        print()
        print("Cerrando navegador...")
        await scraper.close()
        print("Navegador cerrado")
        print()


def main():
    """Función principal."""
    try:
        asyncio.run(test_acm_selenium())
    except KeyboardInterrupt:
        print("\nPrueba interrumpida por usuario")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
