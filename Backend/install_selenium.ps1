# Script de Instalación de Selenium para Bypass de Cloudflare
# ============================================================

Write-Host "🤖 Instalando dependencias de Selenium..." -ForegroundColor Cyan
Write-Host ""

# Verificar si estamos en el directorio Backend
if (-not (Test-Path "requirements.txt")) {
    Write-Host "❌ Error: Debes ejecutar este script desde el directorio Backend" -ForegroundColor Red
    Write-Host "   cd Backend" -ForegroundColor Yellow
    Write-Host "   .\install_selenium.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host "📦 Instalando setuptools (requerido para Python 3.12+)..." -ForegroundColor Green
pip install setuptools

Write-Host "📦 Instalando Selenium, WebDriver Manager y undetected-chromedriver..." -ForegroundColor Green
pip install selenium==4.26.1 webdriver-manager==4.0.2 undetected-chromedriver==3.5.5

Write-Host "📦 Instalando BeautifulSoup4 para parsing HTML..." -ForegroundColor Green
pip install beautifulsoup4==4.12.3

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error instalando dependencias" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Dependencias instaladas correctamente" -ForegroundColor Green
Write-Host ""

# Verificar si existe .env
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creando archivo .env desde .env.example..." -ForegroundColor Cyan
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Archivo .env creado" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANTE: Edita .env y agrega tus credenciales:" -ForegroundColor Yellow
    Write-Host "   ACM_USERNAME=tu_usuario" -ForegroundColor White
    Write-Host "   ACM_PASSWORD=tu_contraseña" -ForegroundColor White
    Write-Host "   SAGE_USERNAME=tu_usuario" -ForegroundColor White
    Write-Host "   SAGE_PASSWORD=tu_contraseña" -ForegroundColor White
    Write-Host ""
    Write-Host "   Si no tienes credenciales, déjalas vacías." -ForegroundColor Gray
} else {
    Write-Host "✅ Archivo .env ya existe" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 Instalación completada!" -ForegroundColor Green
Write-Host ""
Write-Host "📚 Próximos pasos:" -ForegroundColor Cyan
Write-Host "   1. Edita .env con tus credenciales (si las tienes)" -ForegroundColor White
Write-Host "   2. Lee SELENIUM_SETUP.md para instrucciones detalladas" -ForegroundColor White
Write-Host "   3. Prueba con: python test_selenium_scraper.py" -ForegroundColor White
Write-Host ""
Write-Host "💡 Para debugging visual, en .env cambia:" -ForegroundColor Yellow
Write-Host "   SELENIUM_HEADLESS=false" -ForegroundColor White
Write-Host ""