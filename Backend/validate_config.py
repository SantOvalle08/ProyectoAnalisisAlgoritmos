"""
Script de Validación de Configuración
======================================

Verifica que todas las configuraciones necesarias estén correctamente establecidas
antes de iniciar las descargas.

Author: Sistema de Análisis Bibliométrico
Date: Noviembre 2025
"""

import sys
from pathlib import Path

# Agregar el directorio backend al path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.config.settings import settings

def validate_configuration():
    """Valida todas las configuraciones críticas."""
    
    print("=" * 70)
    print("VALIDACIÓN DE CONFIGURACIÓN DEL SISTEMA")
    print("=" * 70)
    print()
    
    issues = []
    warnings = []
    success = []
    
    # 1. Verificar ScienceDirect (Elsevier)
    print("1️⃣  ScienceDirect (Elsevier)")
    if settings.elsevier_api_key and settings.elsevier_api_key != "your-elsevier-api-key":
        print(f"   ✅ API Key configurada: {settings.elsevier_api_key[:8]}...{settings.elsevier_api_key[-4:]}")
        success.append("ScienceDirect API Key")
    else:
        print("   ❌ API Key NO configurada o usa valor por defecto")
        issues.append("ScienceDirect: Configurar ELSEVIER_API_KEY en .env")
    print()
    
    # 2. Verificar SAGE
    print("2️⃣  SAGE Publications")
    if settings.sage_institutional_url:
        print(f"   ✅ URL institucional: {settings.sage_institutional_url}")
        success.append("SAGE Proxy Institucional")
    else:
        print("   ⚠️  URL institucional no configurada (usará acceso público)")
        warnings.append("SAGE: Considerar configurar SAGE_INSTITUTIONAL_URL para acceso institucional")
    print()
    
    # 3. Verificar CrossRef
    print("3️⃣  CrossRef")
    if settings.crossref_api_email and settings.crossref_api_email != "your-email@example.com":
        print(f"   ✅ Email configurado: {settings.crossref_api_email}")
        print("   ℹ️  Mejor rate limit con email registrado")
        success.append("CrossRef Email")
    else:
        print("   ⚠️  Email no configurado (rate limit reducido)")
        warnings.append("CrossRef: Configurar CROSSREF_API_EMAIL para mejor rendimiento")
    print()
    
    # 4. Verificar ACM (Selenium)
    print("4️⃣  ACM Digital Library (Selenium)")
    print(f"   ℹ️  Headless: {settings.selenium_headless}")
    print(f"   ℹ️  Timeout: {settings.selenium_page_load_timeout}s")
    if settings.acm_username and settings.acm_password:
        print("   ✅ Credenciales configuradas")
        success.append("ACM Credenciales")
    else:
        print("   ⚠️  Sin credenciales (usará acceso público con captcha)")
        warnings.append("ACM: Credenciales opcionales para evitar captchas")
    print()
    
    # 5. Verificar Selenium/ChromeDriver
    print("5️⃣  Selenium/ChromeDriver")
    if settings.chromedriver_path:
        print(f"   ℹ️  Path: {settings.chromedriver_path}")
    else:
        print("   ✅ Auto-instalación habilitada")
        success.append("ChromeDriver Auto-install")
    print()
    
    # 6. Verificar configuración del proyecto
    print("6️⃣  Configuración del Proyecto")
    print(f"   ℹ️  Query: '{settings.search_query}'")
    print(f"   ℹ️  Max resultados por fuente: {settings.max_results_per_source}")
    print()
    
    # Resumen
    print("=" * 70)
    print("RESUMEN DE VALIDACIÓN")
    print("=" * 70)
    print()
    
    if success:
        print(f"✅ Configuraciones correctas ({len(success)}):")
        for item in success:
            print(f"   • {item}")
        print()
    
    if warnings:
        print(f"⚠️  Advertencias ({len(warnings)}):")
        for item in warnings:
            print(f"   • {item}")
        print()
    
    if issues:
        print(f"❌ Problemas críticos ({len(issues)}):")
        for item in issues:
            print(f"   • {item}")
        print()
        print("❌ NO se puede proceder con la descarga hasta resolver los problemas críticos")
        return False
    else:
        print("✅ Todas las configuraciones críticas están correctas")
        print()
        print("📊 FUENTES DISPONIBLES:")
        print("   • CrossRef: ✅ Listo")
        print(f"   • ScienceDirect: {'✅ Listo' if settings.elsevier_api_key else '❌ Requiere API Key'}")
        print(f"   • SAGE: {'✅ Acceso institucional' if settings.sage_institutional_url else '⚠️ Acceso público'}")
        print("   • ACM: ✅ Listo (Selenium)")
        print()
        print("🚀 Sistema listo para descargar publicaciones")
        return True

if __name__ == "__main__":
    try:
        is_valid = validate_configuration()
        sys.exit(0 if is_valid else 1)
    except Exception as e:
        print(f"\n❌ Error durante la validación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
