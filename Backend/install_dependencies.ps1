# Script para instalar todas las dependencias del proyecto
# Análisis de Algoritmos - Backend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Instalando Dependencias del Backend  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que Python esté instalado
Write-Host "Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "OK Python encontrado: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "X Error: Python no esta instalado o no esta en PATH" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host ""
Write-Host "Instalando dependencias desde requirements.txt..." -ForegroundColor Yellow
python -m pip install -r requirements.txt

Write-Host ""
Write-Host "Descargando modelos de spaCy..." -ForegroundColor Yellow
python -m spacy download en_core_web_sm

Write-Host ""
Write-Host "Descargando datos de NLTK..." -ForegroundColor Yellow
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  OK Instalacion completada con exito  " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Para iniciar el servidor, ejecuta:" -ForegroundColor Cyan
Write-Host "  python main.py" -ForegroundColor White
Write-Host ""
