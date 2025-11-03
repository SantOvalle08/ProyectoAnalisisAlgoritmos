# 🤖 Guía de Implementación de Selenium para Bypass de Cloudflare

## 📋 **¿Qué Problema Resuelve Esto?**

Los sitios web modernos como **ACM**, **SAGE**, **IEEE** y otros usan protecciones anti-bot:
- **Cloudflare** → Bloquea peticiones HTTP directas
- **Rate limiting agresivo** → Detecta comportamiento automatizado
- **JavaScript challenges** → Requiere navegador real

**Solución:** Usar **Selenium con undetected-chromedriver** para simular un navegador real.

---

## 🚀 **Pasos de Instalación**

### **1. Instalar las Nuevas Dependencias**

Ejecuta en el directorio `Backend`:

```powershell
pip install selenium==4.26.1 webdriver-manager==4.0.2 undetected-chromedriver==3.5.5
```

O instala todo desde requirements.txt actualizado:

```powershell
pip install -r requirements.txt
```

### **2. Crear archivo `.env` con Credenciales**

Copia `.env.example` a `.env`:

```powershell
copy .env.example .env
```

Luego edita `.env` y agrega tus credenciales:

```bash
# Credenciales para scrapers con autenticación
# ACM Digital Library
ACM_USERNAME="tu_usuario_acm"
ACM_PASSWORD="tu_contraseña_acm"

# SAGE Publications
SAGE_USERNAME="tu_usuario_sage"
SAGE_PASSWORD="tu_contraseña_sage"

# Configuración de Selenium
SELENIUM_HEADLESS=false  # Cambia a false para ver el navegador en acción
SELENIUM_IMPLICIT_WAIT=10
SELENIUM_PAGE_LOAD_TIMEOUT=30
```

**⚠️ IMPORTANTE:** Si no tienes credenciales, déjalas vacías. El scraper funcionará en modo público (sin autenticación institucional).

---

## 🔧 **Cómo Funciona**

### **Arquitectura:**

```
Usuario → API Request
    ↓
UnifiedDownloader
    ↓
ACMSeleniumScraper → undetected-chromedriver
    ↓                       ↓
SeleniumBaseScraper → ChromeDriver → Chrome Browser
    ↓
Cloudflare detecta navegador REAL (✓ PASA)
    ↓
Descarga exitosa de publicaciones
```

### **Ventajas de undetected-chromedriver:**

- ✅ **Bypasea Cloudflare** automáticamente
- ✅ **No es detectado** como bot
- ✅ **Maneja JavaScript** dinámico
- ✅ **Soporte para cookies** y sesiones

### **Desventajas:**

- ⚠️ Más **lento** que requests (pero funciona)
- ⚠️ Mayor **consumo de recursos** (RAM, CPU)
- ⚠️ Requiere **Chrome instalado** en el sistema

---

## 📝 **Uso del Nuevo Scraper**

### **Opción 1: Usar desde la API (Recomendado)**

El `unified_downloader.py` necesita actualizarse para usar el scraper de Selenium:

```python
# En unified_downloader.py, cambiar:
from .acm_scraper import ACMScraper  # Viejo

# Por:
from .acm_selenium_scraper import ACMSeleniumScraper  # Nuevo

# Y actualizar el diccionario:
self.available_scrapers = {
    'crossref': CrossRefScraper,
    'acm': ACMSeleniumScraper,  # ← Cambio aquí
    'sage': SAGEScraper,
    'sciencedirect': ScienceDirectScraper
}
```

### **Opción 2: Probar Manualmente**

Crea un script de prueba `test_selenium_scraper.py`:

```python
import asyncio
from app.services.data_acquisition.acm_selenium_scraper import ACMSeleniumScraper

async def test_acm_selenium():
    # Crear scraper (usa credenciales de .env automáticamente)
    scraper = ACMSeleniumScraper(
        headless=False  # Ver el navegador en acción
    )
    
    try:
        # Buscar publicaciones
        results = await scraper.search(
            query="machine learning",
            max_results=10
        )
        
        print(f"✓ Encontradas {len(results)} publicaciones:")
        for i, pub in enumerate(results, 1):
            print(f"{i}. {pub.title[:60]}...")
            print(f"   DOI: {pub.doi}")
            print(f"   URL: {pub.url}")
            print()
    
    finally:
        # Cerrar navegador
        await scraper.close()

# Ejecutar
if __name__ == "__main__":
    asyncio.run(test_acm_selenium())
```

Ejecutar:
```powershell
cd Backend
python test_selenium_scraper.py
```

---

## 🔍 **Debugging**

### **Ver el Navegador en Acción:**

En `.env`, cambia:
```bash
SELENIUM_HEADLESS=false
```

Ahora verás Chrome abrirse y navegar automáticamente.

### **Errores Comunes:**

**1. "ChromeDriver not found"**
```
Solución: undetected-chromedriver lo instala automáticamente.
Si falla, instala Chrome en tu sistema.
```

**2. "Timeout waiting for element"**
```
Solución: Aumenta SELENIUM_PAGE_LOAD_TIMEOUT en .env
O verifica que el sitio no cambió su HTML.
```

**3. "Cloudflare still blocking"**
```
Solución: Asegúrate de usar undetected-chromedriver (no selenium normal).
Verifica que headless=True (modo headless a veces es detectado).
```

**4. "Authentication failed"**
```
Solución: Verifica credenciales en .env
ACM puede requerir acceso institucional.
```

---

## 🎯 **Próximos Pasos**

### **1. Actualizar unified_downloader.py**
Cambiar `ACMScraper` por `ACMSeleniumScraper`

### **2. Implementar SAGE con Selenium**
Crear `sage_selenium_scraper.py` similar a ACM

### **3. Probar Descarga Completa**
Usar la API con ACM habilitado

### **4. Optimizar Rendimiento**
- Reutilizar driver entre búsquedas
- Implementar pool de drivers
- Caché de cookies para sesiones

---

## 📚 **Recursos Adicionales**

- **Selenium Docs:** https://selenium-python.readthedocs.io/
- **undetected-chromedriver:** https://github.com/ultrafunkamsterdam/undetected-chromedriver
- **ChromeDriver:** https://chromedriver.chromium.org/

---

## ⚠️ **Consideraciones Legales y Éticas**

- ✅ Respeta `robots.txt` de cada sitio
- ✅ Implementa rate limiting apropiado
- ✅ No sobrecargues los servidores
- ✅ Usa credenciales institucionales legítimas
- ❌ No uses para scraping masivo comercial
- ❌ No evadas términos de servicio maliciosamente

---

## 🆘 **¿Necesitas Ayuda?**

Si encuentras problemas:
1. Revisa los logs en `Backend/logs/`
2. Verifica credenciales en `.env`
3. Prueba con `SELENIUM_HEADLESS=false` para debugging visual
4. Consulta documentación de Selenium y undetected-chromedriver