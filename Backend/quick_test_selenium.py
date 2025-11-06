"""
Prueba rápida de ACMSeleniumScraper - Verifica descarga de datos
================================================================

Esta prueba verifica que:
1. El scraper se inicializa correctamente
2. Puede buscar en ACM (con bypass de Cloudflare)
3. Extrae publicaciones con los selectores correctos (h3, ul.rlist--inline, etc.)
4. Los datos tienen la estructura esperada

Author: Testing Quick Script
Date: Noviembre 2025
"""

import sys
from pathlib import Path

# Agregar el directorio backend al path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.services.data_acquisition.acm_selenium_scraper import ACMSeleniumScraper
from app.models.publication import Publication
import asyncio

async def test_selenium_scraper():
    """
    Prueba básica del scraper de Selenium.
    NOTA: Requiere intervención manual para resolver captcha.
    """
    print("=" * 70)
    print("PRUEBA RÁPIDA DE ACM SELENIUM SCRAPER")
    print("=" * 70)
    print()
    
    # Inicializar scraper
    print("✓ Inicializando scraper...")
    scraper = ACMSeleniumScraper(headless=False, timeout=30)
    print(f"  - Base URL: {scraper.base_url}")
    print(f"  - Headless: {scraper.headless}")
    print()
    
    # Buscar publicaciones
    query = "artificial intelligence"
    max_results = 3  # Solo 3 para prueba rápida
    
    print(f"✓ Buscando '{query}' en ACM Digital Library...")
    print(f"  - Max resultados: {max_results}")
    print(f"  - ATENCIÓN: Resuelve el captcha si aparece")
    print()
    
    try:
        publications = await scraper.search(query=query, max_results=max_results)
        
        print("\n" + "=" * 70)
        print(f"RESULTADOS: {len(publications)} publicaciones encontradas")
        print("=" * 70)
        print()
        
        if publications:
            for i, pub in enumerate(publications, 1):
                print(f"📄 Publicación {i}:")
                print(f"   Título: {pub.title[:80]}...")
                print(f"   Autores: {len(pub.authors)} autor(es)")
                if pub.authors:
                    print(f"   - {', '.join([a.name for a in pub.authors[:3]])}...")
                print(f"   DOI: {pub.doi}")
                print(f"   URL: {pub.url}")
                print(f"   Año: {pub.year}")
                print()
            
            print("✅ PRUEBA EXITOSA: Se extrajeron publicaciones correctamente")
            print(f"✅ Selectores funcionando (h3, ul.rlist--inline, etc.)")
            
            # Validar estructura
            first_pub = publications[0]
            assert first_pub.title, "❌ ERROR: Título vacío"
            assert first_pub.authors, "❌ ERROR: Sin autores"
            assert first_pub.doi or first_pub.url, "❌ ERROR: Sin DOI ni URL"
            
            print("✅ Estructura de datos validada correctamente")
            
        else:
            print("⚠️ ADVERTENCIA: No se extrajeron publicaciones")
            print("   - Verifica que resolviste el captcha")
            print("   - Revisa los logs para ver si hay errores en el parsing")
            
    except Exception as e:
        print(f"❌ ERROR en la prueba: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cerrar navegador
        if hasattr(scraper, 'driver') and scraper.driver:
            scraper.driver.quit()
            print("\n✓ Navegador cerrado")

if __name__ == "__main__":
    asyncio.run(test_selenium_scraper())
