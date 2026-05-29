<#
start-project-check.ps1
Wrapper para iniciar el proyecto de forma segura.
- Verifica que exista `.venv` y que `uvicorn` esté instalado en ese entorno.
- Si `uvicorn` falta, muestra instrucciones (no instala automáticamente) y permite iniciar solo el Frontend.
#>

Write-Host "Inicio seguro del proyecto — comprobando entorno..." -ForegroundColor Cyan

$projectRoot = $PSScriptRoot

# Verificar virtualenv
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "No se encontró el entorno virtual (.venv) en: $projectRoot\.venv" -ForegroundColor Yellow
    Write-Host "Crear el entorno e instalar dependencias con los siguientes comandos:" -ForegroundColor White
    Write-Host "  python -m venv .venv" -ForegroundColor Gray
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host "  pip install -r Backend/requirements.txt" -ForegroundColor Gray
    exit 1
}

# Comprobar si uvicorn está disponible en el venv
$uvicornInstalled = $false
try {
    & $venvPython -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('uvicorn') else 1)"
    if ($LASTEXITCODE -eq 0) { $uvicornInstalled = $true }
} catch {
    $uvicornInstalled = $false
}

if (-not $uvicornInstalled) {
    Write-Host "AVISO: 'uvicorn' no está instalado en .venv. El backend no podrá iniciarse." -ForegroundColor Yellow
    Write-Host "Instrucciones para instalar (opcional, no se instalará automáticamente):" -ForegroundColor White
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host "  pip install uvicorn[standard]" -ForegroundColor Gray
    Write-Host ""
    $answer = Read-Host "¿Deseas continuar e iniciar solo el Frontend? (y/N)"
    if ($answer -match '^[yY]') {
        Write-Host "Iniciando Frontend..." -ForegroundColor Green
        $frontendCmd = "cd `"$projectRoot\Frontend`"; npm run dev"
        Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd
        Write-Host "Frontend iniciado en una nueva ventana. Backend requiere uvicorn." -ForegroundColor Cyan
        exit 0
    } else {
        Write-Host "Cancelado. Instala 'uvicorn' en el venv y vuelve a ejecutar este script." -ForegroundColor Red
        exit 1
    }
}

# Si uvicorn existe, iniciar Backend y Frontend (comportamiento similar a start-project.ps1)
Write-Host "uvicorn detectado — iniciando Backend y Frontend..." -ForegroundColor Green

$backendCmd = "cd `"$projectRoot\Backend`"; `"$venvPython`" -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd

Start-Sleep -Seconds 3

Write-Host "Iniciando Frontend (Vite + React)..." -ForegroundColor Green
$frontendCmd = "cd `"$projectRoot\Frontend`"; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd

Write-Host "Proyecto iniciado (siempre en nuevas ventanas)." -ForegroundColor Cyan
Write-Host "Backend: http://localhost:8000" -ForegroundColor White
Write-Host "Frontend: http://localhost:5173" -ForegroundColor White
