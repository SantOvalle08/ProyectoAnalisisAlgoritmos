# Script para iniciar el proyecto completo
# Backend (FastAPI) + Frontend (Vite + React)

Write-Host "🚀 Iniciando Proyecto de Análisis de Algoritmos..." -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
$projectRoot = "C:\Users\MI PC\Desktop\CODE\ProyectoAnalisisAlgoritmos"
if (-not (Test-Path $projectRoot)) {
    Write-Host "❌ Error: No se encuentra el directorio del proyecto" -ForegroundColor Red
    exit 1
}

# Iniciar Backend
Write-Host "📦 Iniciando Backend (FastAPI)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\Backend'; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

# Esperar 3 segundos para que el backend inicie
Start-Sleep -Seconds 3

# Iniciar Frontend
Write-Host "🎨 Iniciando Frontend (Vite + React)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\Frontend'; npm run dev"

Write-Host ""
Write-Host "✅ Proyecto iniciado exitosamente!" -ForegroundColor Green
Write-Host ""
Write-Host "📌 URLs disponibles:" -ForegroundColor Cyan
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "   Frontend: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "⌨️  Presiona Ctrl+C en cada ventana para detener los servicios" -ForegroundColor Yellow
